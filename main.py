#Flask app
from flask import Flask, render_template, request, make_response, session
import os
import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
import time
from datetime import datetime
app = Flask(__name__)
postgres_str = "dbname='USER_DATABASE' user='spandy' host='localhost' " + \
                  "password='sandy@123'"
conn = psycopg2.connect(postgres_str)
cur = conn.cursor()

@app.route('/login', methods=['GET','POST'])
def logging_in():
	username = str(request.form['uname'])
	password = str(request.form['pswd'])
	print(username)
	print(password)
	cur.execute("SELECT user_name,password FROM user_table where user_name=%s and password=%s;",(username,password))
	row = cur.fetchone()
	print(row)
	if(row==None):
		return render_template("login.html")
	else:
		now1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		cur.execute("UPDATE user_table SET last_login = %s, logged_in = %s WHERE user_name = %s;", (now1,'t',username))
		conn.commit()
		cur.execute("SELECT * FROM user_table where logged_in=%s;",('t',))
		q = cur.fetchall()
		df1 = pd.DataFrame(q)
		row_list1 = []
		row_list2 = []
		cur.execute("SELECT count(*) FROM user_table where logged_in=%s;",('t',))
		q1 = cur.fetchone()
		df2 = pd.DataFrame(q1)
		count = df2[0][0]
		
		for i in range(0,count):
			my_list1 = []
			my_list2 = []
			tm = (datetime.now() - df1.iloc[i][4]).total_seconds()/60
			tm = str(round(tm)) +' minutes ago'
			
			my_list1=[df1.iloc[i][1]]
			my_list2=[tm]
			row_list1.append(my_list1)
			row_list2.append(my_list2)
		
		return render_template("application.html",data1 = row_list1,data2 = row_list2,count = count,plus = count-5)
    


@app.route('/register', methods=['GET'])
def registration():
	return render_template("register.html")


@app.route('/', methods=['GET'])
def show_index():
	return render_template("login.html")  

	












if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False,threaded=True)
