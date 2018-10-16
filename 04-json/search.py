import json
import sqlite3
import sys


def db_fetch():
    db = sqlite3.connect("scorelib.dat")
    cursor = db.cursor()
    name_to_find = "%" + sys.argv[1] + "%"
    cursor.execute("select * from ((((select id, name from person where name like ?) as people inner join score_author on people.id = composer) inner join score on score_author.score = score.id) inner join edition on score.id = edition.score) inner join print on print.edition = edition.id", (name_to_find,))
    list = cursor.fetchall()
    cursor.close()
    db.close()
    return list


def create_json(list):
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
        prints_of_one_author.append(dict)
    json.dump(res, sys.stdout, indent=4, ensure_ascii=False)


create_json(db_fetch())
