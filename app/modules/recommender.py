from pandas import DataFrame
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class recommender:
    def __init__(self, data : list , features_label : str):
        """[summary]

        Args:
            data (DataFrame): [description]
            features_label (str): [description]
        """
        self.data = DataFrame(data)
        self.features_label = features_label
        self.count_vectorizer = CountVectorizer()
        self.count_matrix =self.vectorize()
        self.sim_matrix = self.fit()

    def vectorize(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        self.count_matrix = self.count_vectorizer.fit_transform(self.data[self.features_label])
        return self.count_matrix

    def print_count_matrix(self):
        print("Count Matrix:", self.count_matrix.toarray())

    def print_sim_matrix(self):
        """[summary]
        """
        print ("Sim Matrix:", self.sim_matrix)

    def fit(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        self.sim_matrix = cosine_similarity(self.count_matrix)
        return self.sim_matrix

    def recommend(self, id : str , n_recommendations : int = 1):
        """[summary]

        Args:
            id (str): [description]
            n_recommendations (int, optional): [description]. Defaults to 1.

        Returns:
            [type]: [description]
        """
        self.data.index.name = 'id'
        z = pd.Series(self.data.index,index=self.data._id.values).to_dict()
        y = pd.Series(self.data._id.values,index=self.data.index).to_dict()
        m = list(enumerate(self.sim_matrix[z[id]]))
        m.sort(key=lambda x:x[1], reverse=True)
        m = m[1:n_recommendations+1]
        return ( y[i[0]] for i in m)

