require 'nokogiri'
require 'open-uri'
require 'mysql2'

$baseurl = "http://news.yahoo.co.jp/hl"
$articles = []

#データベースに書き込む

def writeData()
	#テーブル名
	table_name = 'NewsArticle'
	client = Mysql2::Client.new(:host => "localhost", :username => "root", :password => "root", :database => "MiyamoriLab",:socket => "/Applications/MAMP/tmp/mysql/mysql.sock",:port => "3360")

	for article in $articles do
		title = article["title"]
		content = article["main"]
		genre = article["genre"]

		id = 0
		client.query("SELECT id FROM #{table_name} WHERE title = '#{title}'").each do |col|
			unless col.nil?
				id=col["id"]
			end
		end
		if id == 0
			client.query("INSERT INTO #{table_name} (title,genre,content) VALUES ('#{title}','#{genre}','#{content}')")
		end
	end

end

#ニュース記事をパースして本文などの情報を返す
def parseNewsArticle(url,genre)
	doc = Nokogiri::HTML.parse(open(url),nil,'EUC-JP')
	begin
		mainText = doc.css('#main > div.mainBox > div.article > div.articleMain > div.paragraph > p').text
		mainText = mainText.gsub("\n","").gsub(" ","")
	rescue
		mainText = "error"
	end

	begin
		title = doc.css('#main > div.mainBox > div.article > div.hd > h1').text
	rescue
		title = "error"
	end
	puts title
	return {"title" => title,"main" => mainText,"genre" => genre}
end

def collectArticle(genre,page,articleCount)
	url = $baseurl + "?c=" + genre + "&p=" + page.to_s
	begin 
		doc = Nokogiri::HTML.parse(open(url))

		links = doc.css('#main > div.epCategory > div.articleList > ul > li > p.ttl > a')
		for i in 0..links.length-1 do
			$articles.push(parseNewsArticle(links[i].attribute('href'),genre))
			articleCount += 1
			if articleCount >= 100 then
				break
			end
		end
		page += 1
		if(articleCount < 100) then
			collectArticle(genre,page,articleCount)
		end
	end
end


if __FILE__ == $0
	genres = ["soci","pol","spo"] #社会、政治、スポーツ総合
	for g in genres do
		collectArticle(g,1,0)
	end
	writeData()
	puts "COMPLETED"
end
