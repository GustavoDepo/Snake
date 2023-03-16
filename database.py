import sqlite3

class dataBase():
    def __init__(self):
        self.db = sqlite3.connect('SnakeDB')
        self.sql = self.db.cursor()
        self.sql.execute("""CREATE TABLE IF NOT EXISTS USERS (
                            nickname VARCHAR,
                            score BIGINT    )""")
        self.db.commit()

    def getDb(self):
        self.arr = []
        self.i = 0
        for user in self.sql.execute("SELECT * FROM USERS ORDER BY score DESC"):
            self.arr.append(user)
            if len(self.arr) > 4:
                break
        return self.arr

    def reg(self, nickname, score):
        self.sql.execute(f"SELECT nickname FROM USERS WHERE nickname = '{nickname}'")
        if self.sql.fetchone() is None:
            self.sql.execute(f"INSERT INTO USERS VALUES (?, ?)", (nickname, score))
        else:
            self.sql.execute(f"UPDATE users SET score = {score} WHERE nickname = '{nickname}'" )
        self.db.commit()
        print("Зарегестрирован")

    def close(self):
        self.db.close()

