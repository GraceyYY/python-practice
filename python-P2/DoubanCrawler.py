
import expanddouban
from bs4 import BeautifulSoup


def getMovieUrl(category, location):#Obtain the douban url based on the given category and location
    url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}'.format(category, location)
    return url

def getMovieHtml(category, location):
    #get the full html document by using expanddouban and BeautifulSoup
    html = expanddouban.getHtml(getMovieUrl(category,location),loadmore = True, waittime = 2)
    soup = BeautifulSoup(html, 'html.parser')

    #find movie infomation in the html document and turn it into string
    all_movie_info = str(soup.find_all("a", class_="item"))
    return all_movie_info

# def getMovies(category, location):#return a list of movies which can be found in the douban movie website under the given category and location
#
#     #use while loop to obstract movie title and put them in a list
#     movie_info = getMovieHtml(category, location)
#     movie_list = []
#     while "</a>" in movie_info:
#         title_info = movie_info[movie_info.find('<span class="title"') : ]
#         movie_list.append(title_info[(title_info.find(">") + 1) : title_info.find("</")])
#         movie_info = movie_info[(movie_info.find('</a>')+ 4) : ]
#
#     return movie_list

class Movie:#build a class to store all infomation every movie has

    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

    def movie_info(self):
        print('name = {}'.format(self.name))
        print('rate = {}'.format(self.rate))
        print('location = {}'.format(self.location))
        print('category = {}'.format(self.category))
        print('info_link = {}'.format(self.info_link))
        print('cover_link = {}'.format(self.cover_link))


location_list = ['大陆','美国','香港','台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦']
def movie_in_all_location(category):#Under the category, obtain movies from all locations and abstract all relevant infomation from the html document
    for element in location_list:
        i = 0
        m_html = getMovieHtml(category,element)
        movie_list = []
        while m_html.find('https',i) != -1:
            #locate info_link
                i = m_html.find('https',i)
                info_link = m_html[ i : m_html.find('"',i)]
            #locate cover_link
                i = m_html.find('https',i + 1)
                cover_link = m_html[ i : m_html.find('"',i)]
            #locate name
                i = m_html.find('<span class="title"',i)
                name = m_html[(m_html.find('"">',i) + 3): m_html.find("</",i)]
            #locate rate
                i = m_html.find('<span class="rate"',i)
                rate = m_html[ (m_html.find('"">',i) + 3): m_html.find("</",i)]
            #location
                location = element
                m_info = "\n{},{},{},{},{},{}".format(name,rate,location,category,info_link,cover_link)
            #output all infomation to movies.csv
                with open('movies.csv','a') as f:
                    f.write(m_info)

movie_in_all_location('科幻')
movie_in_all_location('喜剧')
movie_in_all_location('动作')

#read movies.csv and turn it into a list, at the same time remove '\n' which may impact the index of the list
with open('movies.csv', 'r') as f:
    mlist = f.readlines()[1:]

def category_movie_list(category):#build a list that contains movies from the category
    c_m_list = []
    for element in mlist:
        if category in element:
            c_m_list.append(element)
    return c_m_list

def most_movies(category):#output three locations that produce the most movies under the category and calculate the percentage each takes

    count_list = []
    total_number = len(category_movie_list(category))
    with open('output.txt','a') as f:
        f.write('\n在{}电影类别中，数量排名前三的地区有：'.format(category))
#based on the location list, build a new list to show the number of movies each country made
    for element in location_list:
        i = 0
        for movie in category_movie_list(category):
            if element in movie:
                i += 1
        count_list.append(i)
#calculate the percentage and output it into output.txt
    for index in range(3):
        percentage = round(max(count_list)/total_number * 100, 2)
        country = location_list[count_list.index(max(count_list))]
        with open('output.txt','a') as f:
            f.write('\n{}: {}%'.format(country,percentage))
        count_list[count_list.index(max(count_list))] = 0

most_movies('科幻')
most_movies('喜剧')
most_movies('动作')
