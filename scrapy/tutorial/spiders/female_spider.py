import scrapy
import time  

# scrapy runspider first_spider.py -o actors.json

class IntroSpider(scrapy.Spider):
    name = "actor_spider"     # Name of the scraper
    start_urls = []

    for i in range(1, 500):
        start_urls.append("https://www.themoviedb.org/person?page=" + str(i))

    
    
    def parse(self, response):

        links = response.css('#main a::attr("href")').extract()
        for link in links:
            time.sleep(0.2)
            yield response.follow("https://www.themoviedb.org" + link, self.parse_actor)

    
    def parse_actor(self, response):

        name = response.css(".title a::text").get()
        gender = response.css("p:nth-child(3)::text").get().strip()
        biography = response.css(".initial p::text").get()
        birthdate = response.css(".full:nth-child(4)::text").extract()[1].strip()
        birthplace = response.css(".full:nth-child(5)::text").get().strip()

        acting_list, directing_list, writing_list = [], [], []
        if response.css(".zero::text").get() == 'Acting':
            acting_list = response.css(".zero+ .credits tr+ tr .credit_group bdi::text , .zero+ .credits tr+ tr .credit_group .year::text").extract()
        elif response.css(".zero::text").get() == 'Directing':
            directing_list = response.css(".zero+ .credits tr+ tr .credit_group bdi::text , .zero+ .credits tr+ tr .credit_group .year::text").extract()
        elif response.css(".zero::text").get() == 'Writing':
            writing_list = response.css(".zero+ .credits tr+ tr .credit_group bdi::text , .zero+ .credits tr+ tr .credit_group .year::text").extract()

        acting, directing, writing = {}, {}, {}

        # Creates dictionary with years and a list of movies acted by this actor during that year
        if len(acting_list) != 0:
            i = 0
            current_year = 0
            for data in acting_list:
                if i % 2 == 0: # the array is as follows: year, movie, year, movie,...
                    # we are looking at a year
                    if current_year != data: # the year has changed, so we set it as current
                        current_year = data
                        acting[current_year] = [] # creates new array for new year
                else:
                    # we are looking at a movie
                    acting[current_year].append(data) # add movie to array
                i+=1

        # Creates dictionary with years and a list of movies producted by this actor during that year
        if len(directing_list) != 0:
            i = 0
            current_year = 0
            for data in directing_list:
                if i % 2 == 0:
                    if current_year != data:
                        current_year = data
                        directing[current_year] = []
                else:
                    directing[current_year].append(data)
                i+=1
        
        # Creates dictionary with years and a list of movies written by this actor during that year
        if len(writing_list) != 0:
            i = 0
            current_year = 0
            for data in writing_list:
                if i % 2 == 0:
                    if current_year != data:
                        current_year = data
                        writing[current_year] = []
                else:
                    writing[current_year].append(data)
                i+=1

        yield {
            'link': response.url,
            'name': name,
            'gender': gender,
            'biography': biography,
            'birthdate': birthdate,
            'birthplace': birthplace,
            'acting': acting,
            'directing': directing,
            'writing': writing
        }
