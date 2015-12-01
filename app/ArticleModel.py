class ArticleModel:
    def __init__(self,title,content,nouns):
        self.title = title
        self.content = content
        self.nouns = nouns
        self.score = 0

    def calcScore(self,keywords):
        s = 0
        for n in self.nouns:
            if n.noun in keywords:
                s += n.tfidf
        self.score = s
