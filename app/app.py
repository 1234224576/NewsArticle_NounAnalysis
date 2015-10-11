# -*- coding: utf-8 -*-
from flask import Flask,render_template,Response, json,request
from flask.ext.mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MiyamoriLab'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3360
app.config['MYSQL_UNIX_SOCKET'] = '/Applications/MAMP/tmp/mysql/mysql.sock'
mysql.init_app(app)

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
		cur.execute('SELECT id,noun,sum FROM Noun ORDER BY sum DESC')
	else:
		cur.execute('SELECT DISTINCT Noun.id,Noun.noun,Noun.sum FROM (NewsArticle JOIN News_Noun ON NewsArticle.id = News_Noun.newsArticleId) INNER JOIN Noun ON News_Noun.nounId = Noun.id WHERE NewsArticle.genre =  \"%s\" ORDER BY Noun.sum DESC'%genre)
	rv = cur.fetchall()
	data = [{"noun":r[1],"sum":r[2]} for r in rv]
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route('/tfidfrank', methods = ['GET'])
def tfidfrank():
	key = request.args.get("keyword")
	cur = mysql.connection.cursor()
	if key != "":
		print key
		key = "%" + key + "%"
		cur.execute('SELECT DISTINCT NewsArticle.title,NewsArticle.content,NewsArticle.genre,Noun.noun,News_Noun.tfidf FROM (NewsArticle JOIN News_Noun ON NewsArticle.id = News_Noun.newsArticleId) INNER JOIN Noun ON News_Noun.nounId = Noun.id WHERE NewsArticle.content LIKE  \"%s\" OR NewsArticle.title LIKE  \"%s\" ORDER BY News_Noun.tfidf DESC'%(key,key))
		rv = cur.fetchall()
		data = [{"title":r[0],"content":r[1],"genre":r[2],"noun":r[3],"tfidf":r[4]} for r in rv]
	else:
		data = []
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

if __name__ == "__main__":
	app.debug = True
	app.run()


