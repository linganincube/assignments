import json
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

nltk.download('punkt')
nltk.download('wordnet')


class NLPProcessor:
    def __init__(self, knowledge_base_path):
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(tokenizer=self.normalize, stop_words='english')
        self.load_knowledge_base(knowledge_base_path)
        self.train_vectorizer()

    def load_knowledge_base(self, path):
        with open(path, 'r') as file:
            self.knowledge_base = json.load(file)

        self.questions = []
        self.answers = []
        self.categories = []
        self.keywords = []

        for category, qa_pairs in self.knowledge_base.items():
            for pair in qa_pairs:
                self.questions.append(pair['question'])
                self.answers.append(pair['answer'])
                self.categories.append(category)
                self.keywords.append(pair.get('keywords', []))

    def train_vectorizer(self):
        self.vectorizer.fit(self.questions)
        self.question_vectors = self.vectorizer.transform(self.questions)

    def normalize(self, text):
        tokens = word_tokenize(text.lower())
        return [self.lemmatizer.lemmatize(token) for token in tokens]

    def get_response(self, user_input):
        # Check for direct keyword matches first
        keyword_response = self.check_keywords(user_input)
        if keyword_response:
            return keyword_response

        # Vectorize user input
        input_vector = self.vectorizer.transform([user_input])

        # Calculate similarity
        similarities = cosine_similarity(input_vector, self.question_vectors)
        max_index = np.argmax(similarities)

        # Return best match if similarity is above threshold
        if similarities[0, max_index] > 0.5:
            return {
                "response": self.answers[max_index],
                "category": self.categories[max_index],
                "confidence": float(similarities[0, max_index])
            }
        else:
            return {
                "response": "I'm not sure I understand. Could you rephrase your question? For admissions, say 'admissions'. For programs, say 'programs'. For student services, say 'services'.",
                "category": "unknown",
                "confidence": 0.0
            }

    def check_keywords(self, user_input):
        user_words = set(self.normalize(user_input))
        for idx, keyword_list in enumerate(self.keywords):
            if any(keyword in user_words for keyword in keyword_list):
                return {
                    "response": self.answers[idx],
                    "category": self.categories[idx],
                    "confidence": 1.0,
                    "matched_keywords": True
                }
        return None