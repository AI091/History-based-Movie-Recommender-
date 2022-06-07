import pandas as pd

class clean():
    """
    Clean dataset and categorize some features to produce clean dataset used in movie reccommendation system model 
    """
    
    def __init__(self, lst):
        """
        Clean class constructor 

        Parameters
        ----------
        path : str
            path pf dataset to be cleaned.

        Returns
        -------
        None.

        """
        self.lst = lst
        self.df = pd.DataFrame(lst)

    def categorize_rating(self, rating):
        """
        Categorize rating into three groups

        Parameters
        ----------
        rating : int
            rating of movie or series.

        Returns
        -------
        str
            rating group(low - medium - high).

        """
        rating = float(rating)
        if(rating <= 5):
            return "low"
        elif(rating <= 7):
            return "medium"
        else:
            return "high"

    def convert_raters_to_numbers(self, raters):
        """
        Convert number of raters from compact short format
        into numeric format(10k -> 10000)

        Parameters
        ----------
        raters : str
            number of raters in compact short format(10k).

        Returns
        -------
        int
            number of raters in numeric format(10000).

        """
        if(raters.lower()[-1] == "k"):
            return int(float(raters[:-1])*1000)
        elif(raters.lower()[-1] == "m"):
            return int(float(raters[:-1])*1e6)
        else:
            return int(raters)

    def convert_list_to_string(self,lst):
        """
        Convert list of strings into compact lowered format of strings

        Parameters
        ----------
        list : list
            list of strings.

        Returns
        -------
        str
            compact format of string.

        """
        names = ""
        for name in lst:
            names += "".join(name.lower().split())
            names += " "
        return names

    def categorize_length(self, length):
        """
        Convert length(movie-series) from short compact format into numeric format(1h -> 60)
        Categorize length(movie-series episode) into three groups

        Parameters
        ----------
        length : str
            compact format of (movie-series episode) length.

        Returns
        -------
        str
            length group(short-medium-long).

        """
        if length == "" or length == None or "-" in length:
            return ""
        length = length.split(" ")
        length_in_minutes = 0
        for time in length:
            if(time[-1] == "m"):
                length_in_minutes += int(time[:-1])
            else:
                length_in_minutes += int(time[:-1]) * 60
        if length_in_minutes <= 90:
            return "short"
        elif length_in_minutes <= 150:
            return "medium"
        else:
            return "long"

    def categorize_year(self, year):
        """
        Categorize publish time of movie into two groups.

        Parameters
        ----------
        year : int
            Publish time of movie-series.

        Returns
        -------
        str
            Publish group(old-new).

        """
        year = int(year)        
        if(year < 2014):
            return "old"
        else:
            return "new"

    def is_series(self, title):
        """
        Define if title is series or movie

        Parameters
        ----------
        title : str
            Title of movie or series.

        Returns
        -------
        str
            Type of title(movie-series).

        """
        if title:
            return "series"
        else:
            return "movie"
    
    def run(self):
        """
        Apply all functions to the dataset to provide features used in model

        Returns
        -------
        None.

        """
        
        # Categorize rating
        self.df['rating'] = self.df['rating'].apply(self.categorize_rating)
        
        # Truncate movies with number of raters less than 10k
        self.df['new_raters'] = self.df['number'].apply(self.convert_raters_to_numbers)
        self.df = self.df[self.df['new_raters'] > 1e5]
        self.df = self.df.drop(columns=['new_raters', "number"], axis=1)
        # Categorize movie/series
        self.df['series'] = self.df['series'].apply(self.is_series)
        # Convert genres to dtring
        self.df['genres'] = self.df['genres'].apply(self.convert_list_to_string)
        # Convert writers to string
        self.df['writers'] = self.df['writers'].apply(self.convert_list_to_string)
        # Convert directors to string
        self.df['directors'] = self.df['directors'].apply(self.convert_list_to_string)
        # Convert cast to string
        self.df['cast'] = self.df['cast'].apply(self.convert_list_to_string)
        # Convert languages to string
        self.df['languages'] = self.df['languages'].apply(self.convert_list_to_string)
        # Categorize length
        self.df['length'] = self.df['length'].apply(self.categorize_length)
        # Categorize year
        self.df['year'] = self.df['year'].apply(self.categorize_year)
        columns = self.df.columns[1:]
        self.df['features'] = self.df['length'].apply(lambda x: "")
        for column in columns:
            if column == "poster":
                continue
            self.df["features"] += self.df[column] + " "
        self.df["features"] = self.df["features"].apply(lambda x: x.replace("  ", " "))
        
        
    def save_to_dict(self):
        """
        Save data into dictinary

        Parameters
        ----------
        out : dict
            Dictionary of data .

        Returns
        -------
        None.

        """
        self.out = self.df.to_dict("record")
        return self.out






