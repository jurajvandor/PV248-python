import json
import sqlite3
import sys


def db_fetch(db):
    cursor = db.cursor()
    name_to_find = "%" + sys.argv[1] + "%"
    cursor.execute("select * from ((((select id, name from person where name like ?) as people inner join score_author on people.id = composer) inner join score on score_author.score = score.id) inner join edition on score.id = edition.score) inner join print on print.edition = edition.id", (name_to_find,))
    list = cursor.fetchall()
    cursor.close()
    return list


def create_json(list, db):
    if len(list) == 0:
        return
    res = {}
    list.sort(key=lambda x: x[0])
    id = list[0][0]
    prints_of_one_author = []
    for item in list:
        if item[0] != id:
            res[item[1]] = prints_of_one_author
            prints_of_one_author = []
            id = item[0]
        dict = {}
        dict["Print Number"] = item[15]
        composers = fetch_composers(item[5], db)
        if len(composers) != 0:
            s = []
            for composer in composers:
                s.append(composer[0])
            dict["Composer"] = s
        if item[6] is not None:
            dict["Title"] = item[6]
        if item[7] is not None:
            dict["Genre"] = item[7]
        if item[8] is not None:
            dict["Key"] = item[8]
        if item[10] is not None:
            dict["Composition Year"] = item[10]
        if item[13] is not None:
            dict["Edition"] = item[13]
        editors = fetch_editors(item[12], db)
        if len(editors) != 0:
            s = []
            for i, editor in enumerate(editors):
                s.append(editor[0])
            dict["Editor"] = s
        voices = fetch_voices(item[5], db)
        for voice in voices:
            s = ""
            if voice[3] is not None:
                s += voice[3]
            if voice[4] is not None:
                if voice[3] is not None:
                    s += ", "
                s += voice[4]
            dict["Voice " + str(voice[1])] = s
        if item[16] == 'Y':
            dict["Partiture"] = True
        else:
            dict["Partiture"] = False
        if item[9] is not None:
            dict["Incipit"] = item[9]
        prints_of_one_author.append(dict)
    json.dump(res, sys.stdout, indent=4, ensure_ascii=False)


def fetch_voices(score_id, db):
    cursor = db.cursor()
    cursor.execute("select * from voice where score = ?", (score_id, ))
    return cursor.fetchall()


def fetch_editors(edition_id, db):
    cursor = db.cursor()
    cursor.execute("select person.name from (select * from edition_author where edition = ?) inner join person on editor = person.id", (edition_id, ))
    return cursor.fetchall()


def fetch_composers(score_id, db):
    cursor = db.cursor()
    cursor.execute("select person.name from (select * from score_author where score = ?) inner join person on composer = person.id", (score_id,))
    return cursor.fetchall()


db = sqlite3.connect("scorelib.dat")
create_json(db_fetch(db), db)
