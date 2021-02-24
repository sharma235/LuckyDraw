import MySQLdb
import dbKey as key
con = MySQLdb.connect(key.sql["host"], key.sql["user"], key.sql["passwd"])
cur = con.cursor()
cur.execute("CREATE Database IF NOT EXISTS LuckyDraw")
cur.execute("use LuckyDraw")
cur.execute("CREATE TABLE IF NOT EXISTS token_info (token varchar(255),status INT)")
cur.execute("CREATE TABLE IF NOT EXISTS draw_winners (token varchar(255), prize varchar(255), date varchar(255))")
con.commit()
cur.close()
con.close()