import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import nltk

nltk.download('punkt')
nltk.download('stopwords')

class TravelRecommender:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.preprocess_data()

    def preprocess_data(self):
        self.df['attractions'] = self.df['attractions'].fillna('')
        self.df['user_preferences'] = self.df['user_preferences'].fillna('')

        scaler = MinMaxScaler()
        self.df['normalized_budget'] = scaler.fit_transform(self.df[['budget']])


        self.tfidf = TfidfVectorizer(stop_words='english')
        self.attractions_matrix = self.tfidf.fit_transform(self.df['attractions'])

    def recommend(self, preferences, budget_range, top_n=5):
        preferences = preferences.lower() 
        filtered_df = self.df[self.df['user_preferences'].str.contains(preferences, case=False, na=False)]

        if filtered_df.empty:
            return {'error': f'No destinations found matching your preferences: {preferences}'}

        user_vec = self.tfidf.transform([preferences])
        scores = cosine_similarity(user_vec, self.attractions_matrix)[0]


        budget_mask = (filtered_df['budget'] >= budget_range[0]) & (filtered_df['budget'] <= budget_range[1])
        recommendations = filtered_df[budget_mask].copy()

        if recommendations.empty:
            return {'error': 'No destinations found matching your budget range'}

        recommendations['score'] = scores[budget_mask.index[budget_mask]]

        return recommendations.sort_values(by='score', ascending=False).head(top_n).to_dict(orient='records')
