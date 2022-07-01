from decimal import Decimal
import nltk, spacy, gensim
from nltk.corpus import stopwords
from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from ask_chip.constants.general_constants import MAX_SUMMARY_LEN


def preprocess_text(word):
  if word is None:
    word = ""
  preprocessed_word = ''.join(ch for ch in word if ch.isalnum() or ch.isspace())
  return preprocessed_word

def get_summarized_text(result):
  return result['content'][0:MAX_SUMMARY_LEN] if result is not None and len(result['content']) > MAX_SUMMARY_LEN else result['content']

def preprocess_query(query):
  if query is None:
    query = ""

  sw_nltk = stopwords.words('english')
  words = [word for word in query.split() if word.lower() not in sw_nltk]

  new_text = " ".join(words)

  en = spacy.load('en_core_web_sm')
  sw_spacy = en.Defaults.stop_words

  words_1 = [word for word in new_text.split() if word.lower() not in sw_spacy]
  new_text_1 = " ".join(words_1)
  new_text_2 = remove_stopwords(new_text_1)

  words_2 = [word for word in new_text_2.split() if word.lower() not in ENGLISH_STOP_WORDS]
  new_text_final = " ".join(words_2)

  return new_text_final
