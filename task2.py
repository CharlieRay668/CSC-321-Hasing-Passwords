import nltk
from nltk.corpus import words

nltk.download('words')
word_list = words.words()
corpus = [word for word in word_list if 6 <= len(word) <= 10]