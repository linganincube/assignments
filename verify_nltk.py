import nltk
from nltk.tokenize import word_tokenize, PunktSentenceTokenizer

# Test punkt
text = "This is a test sentence."
print(word_tokenize(text))

# Test wordnet
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize("running"))