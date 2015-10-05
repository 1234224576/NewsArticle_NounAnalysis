# -*- coding: utf-8 -*-
import MeCab
import os
import MySQLdb

mt = MeCab.Tagger("mecabrc")

connect = MySQLdb.connect(unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock",db="MiyamoriLab", host="localhost", user="root", passwd="root")
cursor = connect.cursor()
cursor.execute("select * from NewsArticle")
result = cursor.fetchall()
for row in result:
	articleId = row[0]
	content = str(row[3])
	res = mt.parseToNode(content)
	while res:
		arr = res.feature.split(",")
		if arr[0] == "名詞":
			print articleId
			print res.surface
		res = res.next
	# print "===== Hit! ====="
	# print "id   -- " + str(row[0]).encode('utf-8')
	# print "title-- " + str(row[1])
	# print "genre-- " + str(row[2])
	# print "main -- " + str(row[3])


# mt = MeCab.Tagger("mecabrc")
# res = mt.parseToNode(text)

# while res:
# 	arr = res.feature.split(",")

# 	if arr[0] == "名詞" or arr[0] == "動詞":
# 		if res.surface in wordCount:
# 			wordCount[res.surface] += 1
# 		else:
# 			wordCount[res.surface] = 1
# 	res = res.next

