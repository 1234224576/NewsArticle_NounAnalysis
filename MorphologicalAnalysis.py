# -*- coding: utf-8 -*-
import MeCab
import os
import MySQLdb

mt = MeCab.Tagger("mecabrc")

connect = MySQLdb.connect(unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock",db="MiyamoriLab", host="localhost", user="root", passwd="root")
cursor = connect.cursor()

def insertDatabase(articleId,title,wordDic):
	sumWords = sum(wordDic.values())
	m = max(wordDic.values())
	for word in wordDic.keys():
		count = wordDic[word]
		tf = float(count)/sumWords
		cursor.execute("select id from Noun where noun = \"%s\"" % word)
		if len(cursor.fetchall()) == 0:
			cursor.execute("insert into Noun(noun,sum) values (\"%s\",%d)"%(word,count))
			connect.commit()	
		else:
			cursor.execute("update Noun set sum = sum + %d where noun = \"%s\""%(count,word))
			connect.commit()
		cursor.execute("select id from Noun where noun = \"%s\""%word)
		result = cursor.fetchall()
		cursor.execute("insert into News_Noun(newsArticleId,nounId,count,tf) values(%d,%d,%d,%e)"%(articleId,result[0][0],count,tf))
		connect.commit()

def nounExtraction(articleId,title,content):
	targetText = title + content
	wordDic = {}

	res = mt.parseToNode(targetText)
	while res:
		arr = res.feature.split(",")
		if arr[0] == "名詞":
			if res.surface in wordDic:
				wordDic[res.surface] += 1
			else:
				wordDic[res.surface] = 1
		res = res.next
	insertDatabase(articleId,title,wordDic)

if __name__ == "__main__":
	cursor.execute("select * from NewsArticle")
	result = cursor.fetchall()
	for row in result:
		articleId = row[0]
		title = str(row[1])
		content = str(row[3])
		nounExtraction(articleId,title,content)