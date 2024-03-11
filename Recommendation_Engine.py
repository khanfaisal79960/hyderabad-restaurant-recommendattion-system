import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class Recommender:
    def __init__(self):
        self.df = pd.read_csv('Data/Restaurant names and Metadata.csv')
        self.vector = TfidfVectorizer()
        self.df['Collections'] = self.df['Collections'].fillna("")
        self.tfid = self.vector.fit_transform(self.df['Collections'])
        self.cosine_matrix = linear_kernel(self.tfid, self.tfid)
        self.indices = pd.Series(self.df['Name'].index, index=self.df['Name'])

    def get_recommendations(self, title):
        idx = self.indices[title]
        sim_scores = enumerate(self.cosine_matrix[idx])
        sorted_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)
        sorted_scores = sorted_scores[1:6]
        index = [i[0] for i in sorted_scores]
        data = self.df.iloc[index]
        results = {
            'Names': list(data['Name']),
            'Links': list(data['Links']),
            'Cuisines': list(data['Cuisines']),
            'Collections': list(data['Collections']),
            # 'Timings': list(data['Timings'])
        }
        return results

    def food_based_recommend(self, title):
        data = self.df[self.df['Cuisines'].str.contains(title)]
        return data.to_dict()
    
    def create_data_frame(self):
        return self.df.to_html()
    
    # def check_entry(self, title):
    #     if self.df['Name'].str.contains(title):
    #         return 'Name'
    #     elif self.df['Cuisines'].str.contains(title):
    #         return 'Cuisines'
    #     else:
    #         return 'Not Found'


# test = Recommender()
# print(test.check_entry('Biryani'))