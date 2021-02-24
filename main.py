from flask import request, jsonify, Flask
import uuid
import MySQLdb
import random
import datetime
import dbKey as key
draw = Flask(__name__)

# variable to establish database connection
global con
con = MySQLdb.connect(key.sql["host"], key.sql["user"], key.sql["passwd"])

# api to get ticket for lucky draw
@draw.route('/draw/ticket', methods=["GET"])
def drawTicket():
	cur = con.cursor()
	cur.execute("use LuckyDraw")
	# create unique key and insert into database with status=0
	token = str(uuid.uuid1().time_low);
	cur.execute('INSERT INTO token_info (token,status) VALUES(%s,%s)',(token,0))
	con.commit()
	cur.close()
	return jsonify({'status' : 1,"message":"request successful", "token": token}), 200

# api to takepart in event
@draw.route('/draw/takepart/<token>', methods=["POST"])
def takePart(token):
	cur = con.cursor()
	cur.execute("use LuckyDraw")
	token=str(token)
	# to check whether token is valid or not
	cur.execute("""SELECT * FROM token_info where token = (%s) and status = (%s)""",(token,0))
	if not cur.fetchall():
		return jsonify({'status' : 0,"message":"inactive"}), 403
	# to update the status, status=1 represent active token
	cur.execute('UPDATE token_info SET status = (%s) where token = (%s)',(1,token))
	con.commit()
	cur.close()
	return jsonify({'status' : 1,"message":"success"}), 200

#api to get list of winner from last 7 days
@draw.route('/draw/winners', methods=["GET"])
def winners():
	cur = con.cursor()
	cur.execute("use LuckyDraw")
	#to get winner list from last 7 days
	cur.execute("""SELECT * FROM draw_winners where date BETWEEN (NOW() - INTERVAL 7 DAY) AND NOW()""")
	info= cur.fetchall()
	con.commit()
	cur.close()
	return jsonify(info), 200

# api to know about the reward of particular day
@draw.route('/draw/rewards', methods=["GET"])
def rewards():
	info = {'Monday':'Washing Machine','Tuesday':'Television','Wednesday':'Refrigerator','Thursday':'Smart Phone','Friday':'Laptop', 'Saturday':'Car', 'Sunday':'Cooker'}
	x = datetime.datetime.now()
	day=x.strftime("%A")
	return jsonify({"Today's Gift":info[day]}), 200

#api to compute the winner
@draw.route('/draw/compute', methods=["GET"])
def compute():
	cur = con.cursor()
	cur.execute("use LuckyDraw")
	cur.execute("""SELECT token FROM token_info where status = (%s)  """,[1])
	info= cur.fetchall()
	n=len(info)
	if not n:
		return jsonify({'status' : 0,"message":"No Participant"}), 403
	#selecting a random token from the tokens
	nm=random.randint(0, n-1)
	x = datetime.datetime.now()
	cur.execute('INSERT INTO draw_winners (token,prize,date) VALUES(%s,%s,%s)',(info[nm],"television",x))
	#updating the status=2 to make tokens inactive
	cur.execute('UPDATE token_info SET status = (%s) where status = (%s)',(2,1))
	con.commit()
	cur.close()
	return jsonify({'status' : 1, "winner": info[0][nm]}), 200

if __name__== "__main__":
	draw.run(debug = True)