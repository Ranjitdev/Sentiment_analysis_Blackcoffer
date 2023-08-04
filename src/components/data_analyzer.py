from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
import os
import sys
from typing import List
from nltk.stem import WordNetLemmatizer, PorterStemmer
import nltk
import re
nltk.download('stopwords')
nltk.download('wordnet')
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


class TextProcessorAndCounter:
    def __init__(self, sentences: list):
        self.sentences = sentences

    @staticmethod
    def get_stopwords() -> tuple[List[str], List[str]]:
        try:
            folder = 'notebook/stopwords'
            custom_stopwords = []
            for i in os.listdir(folder):
                with open(os.path.join(folder, i), 'r') as file:
                    for word in file.readlines():
                        word = word.replace('\n', '').casefold()
                        try:
                            word0 = word.split('|')[0]
                            word1 = word.split('|')[1]
                            custom_stopwords.append(word0.strip())
                            custom_stopwords.append(word1.strip())
                        except:
                            custom_stopwords.append(word.strip())
            english_stopwords = nltk.corpus.stopwords.words('english')
            logging.info('Stopwords generated')
            return custom_stopwords, english_stopwords
        except Exception as e:
            raise CustomException(e, sys)

    # Clean sentences
    def clean_sentences(self) -> List[str]:
        try:
            custom_stopwords, english_stopwords = self.get_stopwords()
            clean_lines = []
            for sentence in self.sentences:
                line = re.sub('[^a-zA-Z]', ' ', sentence)
                new_line = nltk.word_tokenize(line.casefold())
                clean_words = []
                for word in new_line:
                    if word not in english_stopwords:
                        clean_words.append(word)
                clean_words = ' '.join(clean_words)
                clean_lines.append(clean_words)
            logging.info('Cleaned the sentences')
            return clean_lines
        except Exception as e:
            raise CustomException(e, sys)

    # AVG SENTENCE LENGTH
    def avg_sentence_length(self) -> int:
        try:
            length = 0
            for i in self.sentences:
                length += len(i)
            avg_length = int(np.round(length / len(self.sentences)))
            logging.info('Average length calculated')
            return avg_length
        except Exception as e:
            raise CustomException(e, sys)

    # COMPLEX WORD COUNT
    # PERCENTAGE OF COMPLEX WORDS
    # SYLLABLE PER WORD
    def complex_word(self) -> tuple[int, float, int]:
        try:
            sentence_list = self.clean_sentences()
            pattern = r'(es|ed)$'
            vowels = r'[aeiou]'
            complex_count = 0
            complex_words = []
            syllable = 0
            word_count = 0
            for sentence in sentence_list:
                words = nltk.word_tokenize(sentence)
                for word in words:
                    if not re.findall(pattern, word):
                        if re.findall(vowels, word):
                            vowel_count = len(re.findall(vowels, word))
                            syllable += vowel_count
                            word_count += 1
                            if vowel_count > 2:
                                complex_count += 1
                                complex_words.append(word)
            total_word_count = len(nltk.word_tokenize(' '.join(sentence_list)))
            complex_percentage = np.round((complex_count / total_word_count) * 100, 2)
            avg_syllable = int(np.round(syllable / word_count))
            logging.info('Calculated complex words')
            return complex_count, complex_percentage, avg_syllable
        except Exception as e:
            raise CustomException(e, sys)

    # FOG INDEX
    def fog_index(self) -> float:
        try:
            avg_length = self.avg_sentence_length()
            _, complex_percentage, _ = self.complex_word()
            value = np.round((avg_length + complex_percentage) * 0.4, 2)
            logging.info('Calculated fog index')
            return value
        except Exception as e:
            raise CustomException(e, sys)

    # PERSONAL PRONOUNS
    def personal_pronouns(self) -> str:
        try:
            pronouns_list = []
            pronouns = r'\b(I|we|my|ours|us|We|My|Ours|Us)\b'
            for sentence in self.sentences:
                found = re.findall(pronouns, sentence)
                pronouns_list.extend(found)
            pronouns_list = set(pronouns_list)
            logging.info('Counted personal pronouns')
            return ', '.join(pronouns_list)
        except Exception as e:
            raise CustomException(e, sys)

    # AVG NUMBER OF WORDS PER SENTENCE
    # WORD COUNT
    # AVG WORD LENGTH
    def sentences_words_count(self) -> tuple[int, int, int]:
        try:
            clean_sentences = self.clean_sentences()
            total_sentence_count = len(clean_sentences)
            word_count = len(nltk.word_tokenize(' '.join(clean_sentences)))
            total_char_count = len(''.join(nltk.word_tokenize(''.join(clean_sentences))))
            average_words = int(np.round(word_count / total_sentence_count))
            average_word_length = int(np.round(total_char_count / word_count))
            logging.info('Sentence and words counted')
            return average_words, word_count, average_word_length
        except Exception as e:
            raise CustomException(e, sys)


class Scores(TextProcessorAndCounter):
    def __init__(self, sentences: list):
        super().__init__(sentences)
        self.sentences = sentences

    @staticmethod
    def positive_lib() -> List[str]:
        try:
            folder = 'notebook/master_dictionary/positive-words.txt'
            positive_words = []
            with open(folder, 'r') as file:
                for word in file.readlines():
                    word = word.replace('\n', '')
                    positive_words.append(word)
            logging.info('Generated positive words')
            return positive_words
        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def negative_lib() -> List[str]:
        try:
            folder = 'notebook/master_dictionary/negative-words.txt'
            negative_words = []
            with open(folder, 'r') as file:
                for word in file.readlines():
                    word = word.replace('\n', '')
                    negative_words.append(word)
            logging.info('Generated negative words')
            return negative_words
        except Exception as e:
            raise CustomException(e, sys)

    # POSITIVE SCORE
    def positive_score(self) -> int:
        # used raw sentences
        positive_words = self.positive_lib()
        count = 0
        for sentence in self.sentences:
            words = nltk.word_tokenize(sentence)
            for word in words:
                if word in positive_words:
                    count += 1
        return count

    # NEGATIVE SCORE
    def negative_score(self) -> int:
        # used raw sentences
        negative_words = self.negative_lib()
        count = 0
        for sentence in self.sentences:
            words = nltk.word_tokenize(sentence)
            for word in words:
                if word in negative_words:
                    count += 1
        return count

    # POLARITY SCORE
    def polarity_score(self) -> float:
        pos_score = self.positive_score()
        neg_score = self.negative_score()
        score = np.round((pos_score - neg_score) / ((pos_score + neg_score) + 0.000001), 2)
        return score

    # SUBJECTIVITY SCORE
    def subjective_score(self) -> float:
        clean_sentences = self.clean_sentences()
        word_count = len(nltk.word_tokenize(' '.join(clean_sentences)))
        pos_score = self.positive_score()
        neg_score = self.negative_score()
        score = np.round((pos_score + neg_score) / (word_count + + 0.000001), 2)
        return score

    def get_all_scores(self):
        try:
            clean_sentences = self.clean_sentences()
            positive_words = self.positive_lib()
            negative_words = self.negative_lib()
            pos_score = 0
            neg_score = 0

            for sentence in self.sentences:
                words = nltk.word_tokenize(sentence)
                for word in words:
                    if word in positive_words:
                        pos_score += 1

            for sentence in self.sentences:
                words = nltk.word_tokenize(sentence)
                for word in words:
                    if word in negative_words:
                        neg_score += 1

            polarity_score = np.round((pos_score - neg_score) / ((pos_score + neg_score) + 0.000001), 2)

            word_count = len(nltk.word_tokenize(' '.join(clean_sentences)))
            subjective_score = np.round((pos_score + neg_score) / (word_count + + 0.000001), 2)

            logging.info('Generated all scores')
            return pos_score, neg_score, polarity_score, subjective_score
        except Exception as e:
            raise CustomException(e, sys)
