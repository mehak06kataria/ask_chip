from decimal import Decimal
from lemminflect import getAllInflections, getInflection
from lemminflect import getAllLemmas, getLemma

from ask_chip.utils import preprocess_text


class ScoreWordContext:
    def __init__(self, query_sentance, context):
        self.query_sentance = query_sentance
        self.query_words = preprocess_text(query_sentance).split()
        self.context = preprocess_text(context)
        self.sematic_query_words = self.get_all_token_similar_words_via_nlp_model(self.query_words)

    def get_all_token_similar_words_via_nlp_model(self, words):
        all_semantic_words = []
        if len(words) == 0 or (len(words) == 1 and words[0] == ''):
            return all_semantic_words
        for word in words:
            semantic_words = self.get_each_token_similar_words_via_nlp_model(word)
            for semantic_word in semantic_words:
                all_semantic_words.append(semantic_word)
        unique_semantic_words = set(all_semantic_words)
        return unique_semantic_words

    def get_each_token_similar_words_via_nlp_model(self, word):
        all_similar_words = []
        if word is None or word == '':
            return []
        all_inflections = getAllInflections(word)
        all_lemmas = getAllLemmas(word)

        for inflections in all_inflections.values():
            for each_word in inflections:
                all_similar_words.append(each_word)
        for lemmas in all_lemmas.values():
            for each_word in lemmas:
                all_similar_words.append(each_word)
        return all_similar_words

    def get_matching_score(self):
        score = Decimal('0.0')
        summation_token_lengths = 0
        matching_token_lengths = 0

        all_context_token = self.context.split()
        if len(self.query_words) == 0 or (len(self.query_words) == 1 and self.query_words[0] == ''):
            return matching_token_lengths, score
        if len(all_context_token) == 0 or (len(all_context_token) == 1 and all_context_token[0] == ''):
            return matching_token_lengths, score
        for context_token in all_context_token:
            summation_token_lengths += len(context_token)
            if context_token in self.sematic_query_words:
                matching_token_lengths += len(context_token)
                # print(context_toxken)

        if summation_token_lengths == 0:
            return matching_token_lengths, score
        score = Decimal(matching_token_lengths / summation_token_lengths)
        # print(matching_token_lengths, summation_token_lengths, score)
        # print(self.sematic_query_words)
        return matching_token_lengths, score
