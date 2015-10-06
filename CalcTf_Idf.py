# -*- coding: utf-8 -*-
import MeCab
import math
import MySQLdb

mt = MeCab.Tagger("mecabrc")

connect = MySQLdb.connect(unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock",db="MiyamoriLab", host="localhost", user="root", passwd="root")
cursor = connect.cursor(MySQLdb.cursors.DictCursor)

def calcTfIdf():
	cursor.execute("select * from News_Noun inner join Noun on News_Noun.nounId = Noun.id")
	result = cursor.fetchall()
	for row in result:
		tfidf = float(row['idf']) * float(row['tf'])
		tfidf_genre = row['idf_genre'] * row['tf']
		cursor.execute("update News_Noun set tfidf = %e,tfidf_genre = %e where id = %d"%(tfidf,tfidf_genre,row['id']))
		connect.commit()

if __name__ == "__main__":
	cursor.execute("select * from Noun")
	result = cursor.fetchall()
	for row in result:
		cursor.execute("select count(*) from News_Noun where nounId = %d"%row['id'])
		r = cursor.fetchall()
		count = r[0]['count(*)']
		idf = math.log(300.0/float(count))
		idf_genre = math.log(100.0/float(count))
		cursor.execute("update Noun set idf = %e,idf_genre = %e where id = %d"%(idf,idf_genre,row['id']))
		connect.commit()
	calcTfIdf()