import sqlite3

con = sqlite3.connect("Tozen.sqlite")
c = con.cursor()


def new_player(ID, name, gender):
    c.execute("INSERT INTO character(level, playerid, race, experience, name, gender, hp, curhp, ad, ap, spd, atspd, mana, curmana, boss, curfloor, highestfloor, statpoints, gold, titleequipped, inventory, titleavailable, actskills, passskills, experiencereq) VALUES('1',:ID,'Human',1000,:name,:gender,100,100, 25,25,100,1,100,100,'Orc Chef',1,1,5, 0, 'Beginner', '', 'None', '', '', 1000)", {"ID": ID, "name": name, "gender": gender})
    con.commit()

def exists(ID):
    return c.execute("SELECT playerid FROM character WHERE playerid=:n", {"n": ID}).fetchone()

def update(table,type, ID, new_info):
    c.execute(f"UPDATE {table} SET {type}=:new_info WHERE playerid=:n", {"new_info": new_info, "n": ID})
    con.commit()

def select(table, type, ID):
    c.execute(f"SELECT {type} FROM {table} WHERE playerid=:n", {"n": ID})
    return c.fetchone()[0]

def update_list(table,type,ID, new_info):
    to_string = "|".join(new_info)
    c.execute(f"UPDATE {table} SET {type}=:new_info WHERE playerid=:n", {"new_info": to_string, "n": ID})
    con.commit()

def select_list(table, type, ID):
    string = c.execute(f"SELECT {type} FROM {table} WHERE playerid=:n", {"n": ID}).fetchone()
    to_list = string[0].split("|")
    return to_list

def new_monster(name, id, hp, dmg, atspd):
    c.execute("INSERT INTO monster(name, playerid, hp, dmg, atspd) VALUES(:a, :b, :c, :d, :e)", {"a": name, "b": id, "c": hp, "d": dmg, "e": atspd})
    con.commit()

def new_boss(name, id, welcome, hp1, dmg1, atspd1, hp2, dmg2, atspd2):
    c.execute("INSERT INTO boss(name, playerid, welcome, hp1, dmg1, atspd1, hp2, dmg2, atspd2, mode) VALUES(:a, :b, :c, :d, :e,:f,:g,:h,:i, 1)", {"a": name, "b": id, "c": welcome, "d": hp1, "e": dmg1, "f": atspd1, "g": hp2, "h": dmg2, "i": atspd2})
    con.commit()

def del_monster(ID):
    c.execute("DELETE FROM monster WHERE playerid=:n", {"n": ID})
    con.commit()

def del_boss(ID):
    c.execute("DELETE FROM boss WHERE playerid=:n", {"n": ID})
    con.commit()





