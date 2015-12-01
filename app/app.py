# -*- coding: utf-8 -*-
from flask import Flask,render_template,Response, json,request
from flask.ext.mysqldb import MySQL
import QueryBuilder as qb
import collections

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MiyamoriLab'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3360
app.config['MYSQL_UNIX_SOCKET'] = '/Applications/MAMP/tmp/mysql/mysql.sock'
mysql.init_app(app)

query = qb.QueryBuilder()

@app.route("/")
def index():
	return render_template('index.html')

#http://127.0.0.1:5000/frequencyrank
@app.route('/frequencyrank', methods = ['GET'])
def frequencyrank():
	genre = request.args.get("genre",type=str)
	print genre
	cur = mysql.connection.cursor()
	if genre == "all":
		cur.execute(query.getAllFrequency())
	else:
		cur.execute(query.getGenreFrequency(genre))
	rv = cur.fetchall()
	data = [{"noun":r[1],"sum":r[2]} for r in rv]
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route('/tfidfrank', methods = ['GET'])
def tfidfrank():
	keys = request.args.get("keyword").split(" ")
	cur = mysql.connection.cursor()
	if len(keys) != 0:
		cur.execute(unicode(query.getSearchTfidfRank(keys)))
		rv = cur.fetchall()
		data = [{"title":r[1],"content":r[2],"genre":r[3],"noun":r[4],"tfidf":r[5]} for r in rv]
	else:
		data = []
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route('/pagerank', methods = ['GET'])
def pageRank():
	keys = request.args.get("keyword").split(" ")
	cur = mysql.connection.cursor()
	if len(keys) != 0:
		cur.execute(unicode(query.getSearchTfidfRank(keys)))
		rv = cur.fetchall()

		hitTitles = {}
		# for r in rv:
		# 	hitTitles["title"] = r[0]
		#

		for r in rv:
			score = 0
			for key in keys:
				cur.execute(unicode(query.getScore(r[0],key)))
				for s in cur.fetchall():
					score += s[0]
			hitTitles[r[1]] = score

		hitTitles =	collections.OrderedDict(sorted(hitTitles.items(), key=lambda x:x[1],reverse=True))

		data = [{"title":k,"score":v} for k,v in hitTitles.items()]
	else:
		data = []
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp





if __name__ == "__main__":
	app.debug = True
	app.run()
