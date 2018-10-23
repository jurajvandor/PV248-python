import sqlite3
import json
import sys


def db_fetch():
    db = sqlite3.connect("scorelib.dat")
    cursor = db.cursor()
    cursor.execute("select name, born, died from (select composer from score_author where score = (select score from edition where edition.id = (select edition from print where id = ?))) inner join person on composer = person.id", (int(sys.argv[1]),))
    list = cursor.fetchall()
    cursor.close()
    db.close()
    return list


def create_json(list):
    res = []
    for item in list:
        dict = {}
        dict["name"] = item[0]
        if item[1] is not None:
            dict["born"] = item[1]
        if item[2] is not None:
            dict["died"] = item[2]
        res.append(dict)
    json.dump(res, sys.stdout, indent=4, ensure_ascii=False)
    print()


create_json(db_fetch())
