import nltk
from nltk import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer


def __init__(self, knowledge_base_path):
    # Ensure NLTK data is available
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    self.lemmatizer = WordNetLemmatizer()
    self.vectorizer = TfidfVectorizer(
        tokenizer=self.normalize,
        stop_words='english',
        token_pattern=None
    )
    self.load_knowledge_base(knowledge_base_path)
    self.train_vectorizer()