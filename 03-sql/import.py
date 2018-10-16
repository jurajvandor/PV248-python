import sqlite3
import scorelib
import sys


def create_db(filename):
    conn = sqlite3.connect(filename)
    conn.execute("create table person ( id integer primary key not null, born integer, died integer,name varchar not null );")
    conn.execute("create table score ( id integer primary key not null, name varchar, genre varchar, key varchar, incipit varchar, year integer );")
    conn.execute("create table voice ( id integer primary key not null, number integer not null, score integer references score( id ) not null, range varchar, name varchar );")
    conn.execute("create table edition ( id integer primary key not null, score integer references score( id ) not null, name varchar, year integer );")
    conn.execute("create table score_author( id integer primary key not null, score integer references score( id ) not null, composer integer references person( id ) not null );")
    conn.execute("create table edition_author( id integer primary key not null, edition integer references edition( id ) not null, editor integer references person( id ) not null );")
    conn.execute("create table print ( id integer primary key not null, partiture char(1) default 'N' not null, edition integer references edition( id ) );")
    conn.commit()
    return conn


def insert_to_db(prints, conn):
    c = conn.cursor()
    com_author_ids = []
    ed_author_ids = []
    for p in prints:
        for person in p.edition.composition.authors:
            com_author_ids.append(int(insert_person(person, c)))
        for person in p.edition.authors:
            ed_author_ids.append(int(insert_person(person, c)))
        com_id = insert_composition(p.edition.composition, c)
        for i, voice in enumerate(p.edition.composition.voices):
            insert_voice(voice, c, i+1, com_id)
        ed_id = insert_edition(p.edition, c, com_id)
        insert_composition_authors(com_id, com_author_ids, c)
        insert_edition_authors(ed_id, ed_author_ids, c)
        insert_print(p, ed_id, c)
        com_author_ids = []
        ed_author_ids = []
    c.close()
    conn.commit()


def insert_person(person, c):
    c.execute("select * from person where name IS ?", (person.name,))
    res = c.fetchone()
    if res is None:
        c.execute("insert into person(born, died, name) values (?, ?, ?)", (person.born, person.died, person.name))
        return c.lastrowid
    else:
        if person.born is not None and res[1] is None:
            c.execute("update person set born = ? where id = ?", (person.born, res[0]))
        if person.died is not None and res[2] is None:
            c.execute("update person set died = ? where id = ?", (person.died, res[0]))
        return res[0]


def insert_composition(com, c):
    composition_id = check_voices_and_authors(com, c)
    if composition_id == -1:
        c.execute("insert into score(name, genre, key, incipit, year) values (?, ?, ?, ?, ?)", (com.name, com.genre, com.key, com.incipit, com.year))
        return c.lastrowid
    return composition_id


def check_voices_and_authors(com, c):
    c.execute("select * from score where name IS ? and genre IS ? and key IS ? and incipit IS ? and year IS ?", (com.name, com.genre, com.key, com.incipit, com.year))
    res = c.fetchall()
    if len(res) > 0:
        for item in res:
            c.execute("select * from (select composer from score_author where score IS ?) inner join person on composer = person.id", (item[0],))
            authors_ok = compare_persons(com.authors, c.fetchall())
            c.execute("select * from voice where score IS ?", (item[0],))
            voices_ok = compare_voices(com.voices, c.fetchall())
            if authors_ok and voices_ok:
                return item[0]
    return -1


def compare_voices(list_voices, list_tuples):
    if len(list_tuples) != len(list_voices):
        return False
    list_tuples.sort(key=sorting_fun)
    for item in list_tuples:
        if str(list_voices[item[1]-1].name) != str(item[4]) or str(list_voices[item[1]-1].range) != str(item[3]):
            return False
    return True


def sorting_fun(item):
    return item[1]


def insert_voice(voice, c, number, com_id):
    if voice is None:
        voice = scorelib.Voice(None, None)
    c.execute("select * from voice where name IS ? and range IS ? and number IS ? and score IS ?", (voice.name, voice.range, number, com_id))
    res = c.fetchone()
    if res is None:
        c.execute("insert into voice(number, score, range, name) values (?, ?, ?, ?)", (number, com_id, voice.range, voice.name))
        return c.lastrowid
    return res[0]


def insert_edition(ed, c, com_id):
    c.execute("select * from edition where score IS ? and name IS ?", (com_id, ed.name))
    res = c.fetchone()
    authors_ok = True
    if res is not None:
        c.execute("select * from ((select editor from edition_author where edition IS ?) natural inner join person)", (res[0],))
        authors_ok = compare_persons(ed.authors, c.fetchall())
    if res is None or not authors_ok:
        c.execute("insert into edition(score, name, year) values (?, ?, ?)", (com_id, ed.name, None))
        return c.lastrowid
    return res[0]


def compare_persons(list_persons, list_tuples):
    b1 = True
    if len(list_tuples) != len(list_persons):
        return False
    for item in list_tuples:
        b2 = False
        for person in list_persons:
            b2 = b2 or person.name == item[4]
        b1 = b1 and b2
    return b1


def insert_composition_authors(com_id, com_author_ids, c):
    for author in com_author_ids:
        c.execute("select * from score_author where score IS ? and composer IS ?", (com_id, author))
        res = c.fetchone()
        if res is None:
            c.execute("insert into score_author(score, composer) values (?, ?)", (com_id, author))


def insert_edition_authors(ed_id, ed_author_ids, c):
    for author in ed_author_ids:
        c.execute("select * from edition_author where edition IS ? and editor IS ?", (ed_id, author))
        res = c.fetchone()
        if res is None:
            c.execute("insert into edition_author(edition, editor) values (?, ?)", (ed_id, author))


def insert_print(p, ed_id, c):
    partiture = 'N'
    if p.partiture:
        partiture = 'Y'
    c.execute("select * from print where id IS ? and partiture IS ? and edition IS ?", (p.print_id, partiture, ed_id))
    res = c.fetchone()
    if res is None:
        c.execute("insert into print(id, partiture, edition) values (?, ?, ?)", (p.print_id, partiture, ed_id))
        return c.lastrowid
    return res[0]


prints = scorelib.load(sys.argv[1])

conn = create_db(sys.argv[2])

insert_to_db(prints, conn)
