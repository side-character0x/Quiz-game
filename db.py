import sqlite3

class Database:
    def __init__(self):
        self.conn=sqlite3.connect("quiz.db")
        self.conn.row_factory=sqlite3.Row
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS auth(id INTEGER PRIMARY KEY, username TEXT, pin TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS quiz_data(username TEXT, coins NUMBER, high_score NUMBER)")
    def add_user(self,username,pin):
        self.cur.execute("INSERT INTO auth(username,pin) VALUES(?,?)",(username,pin))
        self.cur.execute("INSERT INTO quiz_data(username,coins,high_score) VALUES(?,?,?)",(username,0,0))
        self.conn.commit()
        self.conn.close()
    def check_user(self,username,pin):
        db_pin=self.cur.execute("SELECT pin FROM auth WHERE username=?",(username,)).fetchone()
        self.conn.close()
        return db_pin["pin"]==pin
    def add_coins(self,username,coins):
        self.cur.execute("UPDATE quiz_data SET coins=coins+? WHERE username=?",(coins,username))
        self.conn.commit()
        self.conn.close()
    def add_highscore(self,username,high_score):
        self.cur.execute("UPDATE quiz_data SET high_score=? WHERE username=?",(high_score,username))
        self.conn.commit()
        self.conn.close()
    def get_coins(self,username):
        coins=self.cur.execute("SELECT coins FROM quiz_data WHERE username=?",(username,)).fetchone()
        self.conn.close()
        return coins["coins"]
    def get_highscore(self,username):
        high=self.cur.execute("SELECT high_score FROM quiz_data WHERE username=?",(username,)).fetchone()
        self.conn.close()
        return high["high_score"] 