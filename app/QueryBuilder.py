# -*- coding: utf-8 -*-
class QueryBuilder:
	def getAllFrequency(self):
		return 'SELECT id,noun,sum FROM Noun ORDER BY sum DESC'
	def getGenreFrequency(self,genre):
		return """SELECT DISTINCT Noun.id,Noun.noun,Noun.sum 
		FROM (NewsArticle JOIN News_Noun 
		ON NewsArticle.id = News_Noun.newsArticleId) 
		INNER JOIN Noun ON News_Noun.nounId = Noun.id 
		WHERE NewsArticle.genre =  \"%s\" ORDER BY Noun.sum DESC"""%genre

	def appendWhere(self,keys):
		w = "WHERE "
		orFlag = False
		for i in range(0,len(keys)):
			isNext = True if (i+1 < len(keys)) else False
			if keys[i] == "OR":
				continue
			if isNext:
				w += "NewsArticle.content LIKE " + "\"%"+keys[i]+"%\""
				if keys[i+1] == "OR":
					w += " OR "
				else:
					w += " AND "
			else:
				w += "NewsArticle.content LIKE " + "\"%"+keys[i]+"%\""
		return w
		# NewsArticle.content LIKE  \"%s\" OR NewsArticle.title LIKE  \"%s\" ORDER BY News_Noun.tfidf DESC"""%(key,key)

	def getSearchTfidfRank(self,keys):
		query = """SELECT DISTINCT NewsArticle.title,NewsArticle.content,NewsArticle.genre,Noun.noun,News_Noun.tfidf 
		FROM (NewsArticle JOIN News_Noun 
		ON NewsArticle.id = News_Noun.newsArticleId) 
		INNER JOIN Noun ON News_Noun.nounId = Noun.id """
		query += self.appendWhere(keys)
		print query
		return query

	