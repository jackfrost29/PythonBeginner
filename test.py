import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

_reg_no = '2015-816-782'

con = sqlite3.connect("database.db")
con.row_factory = dict_factory
cur = con.cursor()
x = "select * from user where reg_no='" +_reg_no+ "';"
cur.execute(x)
dic = cur.fetchall

print(dic)
print(x)