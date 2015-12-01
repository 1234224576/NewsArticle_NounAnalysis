import operator
class JSONBuilder:
    def __init__(self):
        self.articles = []

    def setArticles(self,articles):
        self.articles = articles

    def sort(self):
        self.articles.sort(key=operator.attrgetter('score'))

    def build(self):
        self.sort()
        data = [{"title":r.title,"score":r.score} for r in articles]
        return data
