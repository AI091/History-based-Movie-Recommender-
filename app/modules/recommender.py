from pandas import DataFrame
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class recommender:
    def __init__(self, data : list , features_label : str):
        """
        Initializes the data frame and prepares the the data for the model by using 
        Count Vectorizer 
        Args:
            data (DataFrame): [ Fetched from the database ]
            features_label (str): [the label of the features column in the dataframe ]
        """
        self.data = DataFrame(data)
        self.features_label = features_label
        self.count_vectorizer = CountVectorizer()
        self.count_matrix =self.vectorize()
        self.sim_matrix = self.fit()

    def vectorize(self):
        """
        applies the countVecctorizer mehtod
        Returns:
            [self.count_matrix]: a matriz with frequency of the words in each movie
        """
        self.count_matrix = self.count_vectorizer.fit_transform(self.data[self.features_label])
        return self.count_matrix

    def print_count_matrix(self):
        print("Count Matrix:", self.count_matrix.toarray())

        
    def fit(self):
        """Applies the cosine similarity model on the frequency matrix

        Returns:
          self.sim_matrix: a similarity score matrix between each movie and otheres 
        """
        self.sim_matrix = cosine_similarity(self.count_matrix)
        return self.sim_matrix
        
    def print_sim_matrix(self):
        """ 
        Prints the similarity matrix
        """
        print ("Sim Matrix:", self.sim_matrix)

    

    def recommend(self, id : str , n_recommendations : int = 1):
        """ Recommends either one or three movies based on the user's request

        Args:
            id (str): [description]
            n_recommendations (int, optional): [description]. Defaults to 1.

        Returns:
            [type]: [description]
        """
        self.data.index.name = 'id'
        z = pd.Series(self.data.index,index=self.data._id.values).to_dict() # dictionary between index and id  
        y = pd.Series(self.data._id.values,index=self.data.index).to_dict() # dictionary between id and index 
        m = list(enumerate(self.sim_matrix[z[id]])) # similarity score calculted according to the id 
        m.sort(key=lambda x:x[1], reverse=True)
        m = m[1:n_recommendations+1]
        return ( y[i[0]] for i in m) # returns the id of the movie for the database to fetch it 

