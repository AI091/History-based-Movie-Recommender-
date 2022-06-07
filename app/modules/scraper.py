import time
from bs4 import BeautifulSoup
import requests

class MovieScrap:
    def __init__(self,n_genres,n_pages):
        """[The class MovieScrap with parameters n_genres and n_pages has two attirvutes ,
        movie links and a dataset of their scraped date]

        Args:
            n_genres ([integer]): [the number of genres to be scraped ,max:15]
            n_pages ([type]): [the number of pages to scrape for each genre :max 5 ]
        """        
        self.n_genres=n_genres
        self.n_pages=n_pages
        self.movie_links=set()
        self.dataset=[]
        
    def parse_genre(self,page_link):
        """[takes in the link of a genre in IMDB and trturns the address of the
        pages within it to be scraped]

        Args:
            page_link ([string]): [link of IMDB Genre]

        Returns:
            [page_links]: [Links of pages of movies in this Genre]
        """        
        page_links=[page_link]
        for i in range(self.n_pages):
            res=requests.get(page_link).content
            soup = BeautifulSoup(res, 'html5lib')
            page_links.append('https://www.imdb.com/'+soup.find("a",attrs={"class":"lister-page-next next-page"})["href"])
        return page_links
    
    def parse_page(self,page_link):
        """[parsing a web page consisting a list of movies and 
        adds Individual movie links to the scrapper object]

        Args:
            page_link ([string]): [link of a page containing movie links]
        """        
        res=requests.get(page_link).content
        soup = BeautifulSoup(res, 'html5lib')
        movies=soup.findAll("h3",attrs={"class":"lister-item-header"})
        for k in movies:
            self.movie_links.add('https://www.imdb.com/'+k.a["href"])
            
    def parse_movie(self,link): 
        """[Given the movie links ,it's parsed into a dictionary containg 
        scraped data of the following keys : 
            {title , rating , number of raters, directors , writers , cast , 
             languages, genres ,  age group , TvSeries(bool)  , length ,
             year , poster link}

        Args:
            link ([string]): [link of a movie]
        """        
        try:
            res=res=requests.get(link).content
            soup = BeautifulSoup(res, 'html5lib')
            title=None
            directors=[]
            writers=[]
            cast=[]
            languages=[]
            series=None
            length=None
            age=None
            rating=None
            number=None
            year=None
            li=soup.findAll('li')
            rating=soup.find("span",attrs={"class":"AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"}).text ##use try except some movies dont have ratings
            number=soup.find("div",attrs={"class":"AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3 jkCVKJ"}).text #use try except some movies dont have ratings 
            title=soup.find("h1").text
            year=soup.find("li",attrs={'data-testid':"title-details-releasedate"}).text.split('(')[-2]
            year=''.join(year).split()[-1]
            lang=soup.find('li',attrs={'data-testid':"title-details-languages"})
            for i in lang.div.ul:
                languages.append(i.text)
            block=soup.find('ul',attrs={'data-testid':'hero-title-block__metadata'})
            lst=block.findAll('li')
            if len(block)==3:
                age=lst[1].span.text
                length=lst[2].text
                series=False
            elif len(block)==4:
                series=True
                age=lst[2].span.text
                length=lst[3].text
            for i in li:
                if(i.span ):
                    if(i.span.text=='Directors' or i.span.text=='Director'):
                        directors=i.findAll('a')
                        for i in range (len(directors)):
                            directors[i]=directors[i].text
                    elif(i.span.text=='Writers' or i.span.text=='Writer'):
                        writers=i.findAll('a')[:3]
                        for i in range (len(writers)):
                            writers[i]=writers[i].text
            cast=soup.findAll('a',attrs={'data-testid':'title-cast-item__actor'})[:3]
            genres=soup.findAll("span",attrs={"class":"ipc-chip__text"})[:3]
            for i in range(len(genres)):
                genres[i]=genres[i].text
            for i in range (len(cast)):
                cast[i]=cast[i].text
            poster=soup.find("img",attrs={"class":"ipc-image"})["src"]
            movie_data={'title':title,'rating':rating,'number':number,'directors':directors,'writers':writers,'cast':cast,'languages':languages,'genres':genres,'age_group':age,'series':series,'length':length,'year':year,"poster": poster}
            self.dataset.append(movie_data)
            return
        except AttributeError :
            return 
    
    def scrape(self):
        """[the scraping function that puts it all together , scrapes the 
        IMDB genres page then calls generates all movie links, scrapes them and
        adds to the data set ]

        Returns:
            [list]: [list of dictionaries which is the dataset to be used ]
        """        
        res=requests.get("https://www.imdb.com/feature/genre/").content
        soup = BeautifulSoup(res, 'html5lib')
        genre_links=[]
        widgets=soup.findAll('div',attrs={"class":"widget_image"})
        for i in widgets:
            genre_links.append(i.div.a["href"])
        print("reached genre links")
        page_links=[] 
        i=self.n_genres-15
        for link in genre_links[:i]:
            page_links.append(self.parse_genre(link))
        for pages in page_links:
            for page in pages:
                self.parse_page(page)
        print("movies links reached")
        for movie in self.movie_links:
            self.parse_movie(movie)
        print (self.dataset)
        return self.dataset