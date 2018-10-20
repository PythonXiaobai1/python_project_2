

from bs4 import BeautifulSoup
import expanddouban
import csv
import requests
import codecs

#任务一

def getMovieUrl(category, location):
	"""
	return a string corresponding to the URL of douban movie lists given category and location.
	"""
	url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}".format(category,location)
	
	return url


#任务二
url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影"
response = requests.get(url)
html = expanddouban.getHtml(url)


#任务三
#定义电影类
class Movie:
	def __init__(self, name, rate, location, category, info_link, cover_link):
		self.name = name
		self.rate = rate
		self.location = location
		self.category = category
		self.info_link = info_link
		self.cover_link = cover_link

	def m(self):
		return [self.name, self.rate, self.location, self.category, self.info_link, self.cover_link]


#任务四


def getMovies(category, location):
	"""
	return a list of Movie objects with the given category and location.
	"""
	movies = []
	for loc in location:
		html = expanddouban.getHtml(getMovieUrl(category,loc),True)
		soup = BeautifulSoup(html,'html.parser')
		content_1 = soup.find(id='content').find(class_='list-wp').find_all('a', recursive=False)
		for element in content_1:
			movie_name = element.find(class_='title').string
			movie_rate = element.find(class_='rate').string
			movie_location = loc
			movie_category = category
			movie_info_link = element.get('href')
			movie_cover_link = element.find('img').get('src')
			movies.append(Movie(movie_name,movie_rate,movie_location,movie_category,movie_info_link,movie_cover_link).m())
	return movies

#任务五

category_list = ['喜剧', '科幻' ,'灾难']
location_list = ['中国大陆', '美国', '香港', '台湾', '日本', '韩国', '英国', '法国', '德国', '意大利', '西班牙', '印度', 
'泰国', '俄罗斯', '伊朗', '加拿大', '澳大利亚', '爱尔兰', '瑞典', '巴西', '丹麦']


list_1 = getMovies('喜剧', location_list)
list_2 = getMovies('科幻', location_list)
list_3 = getMovies('灾难', location_list)


#将结果输出到movies.csv中（此处借鉴Mentor的codes）
f = codecs.open('movies.csv','w', encoding='utf_8_sig')
writer = csv.writer(f)
writer.writerows(list_1)
writer.writerows(list_2)
writer.writerows(list_3)
f.close()


#任务六
#统计每个类别电影个数
#统计每个类别所有地区电影个数


with open("movies.csv", 'r', encoding='utf_8_sig' ) as f:
	reader = csv.reader(f)
	texts = list(reader)

list1 = []
list2 = []
list3 = []

for movie in texts:
	if movie[3] == "喜剧":
		list1 += movie
		
	elif movie[3] == "科幻":
		list2 += movie
		
	else:
		list3 += movie


	
def movie_result(movie_type_list):
	i = 0
	movie_list_dict = {}
	counts = 0
	while i < len(location_list):
		movie_list_dict[location_list[i]] = 0
		i = i + 1
	for movie in movie_type_list:
		for loc in location_list:
			if loc in movie:
				movie_list_dict[loc] += 1
				counts += 1
	for count in movie_list_dict:
		movie_list_dict[count] = round((movie_list_dict[count] / counts)*100, 2)

	return sorted(movie_list_dict.items(), key=lambda x:x[1], reverse=True)[:3]



type1_result = str(movie_result(list1))
type2_result = str(movie_result(list2))
type3_result = str(movie_result(list3))

#将结果输出到output.txt中
with open('output.txt', 'w', encoding='utf-8') as f:
	f.write("{}电影排名前三的地区和比例分别是：{}。\n".format(category_list[0], type1_result))
	f.write("{}电影排名前三的地区和比例分别是：{}。\n".format(category_list[1], type2_result))
	f.write("{}电影排名前三的地区和比例分别是：{}。\n".format(category_list[2], type3_result))




	

	
	
