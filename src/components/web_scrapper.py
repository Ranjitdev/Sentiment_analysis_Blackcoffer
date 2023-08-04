from src.exception import CustomException
from src.logger import logging
from src.components.data_ingesion import DataIngesion
import pandas as pd
import numpy as np
import os
import sys
import streamlit as st
from dataclasses import dataclass
from src.components.data_analyzer import TextProcessorAndCounter, Scores
import requests
from bs4 import BeautifulSoup
import json
from typing import List
from datetime import datetime as dt
import time
import warnings
warnings.filterwarnings('ignore')


@dataclass
class ScrappingConfig:
    input_data = r'artifacts/input.csv'
    output_data = r'artifacts/output.csv'


class InitiateScrapping:
    def __init__(self, cur_time):
        self.config = ScrappingConfig
        self._cur_time = cur_time

    def get_urls(self) -> List[str]:
        try:
            data = pd.read_csv(self.config.input_data)
            urls_list = []
            for i in range(len(data)):
                url = data.iloc[i, 1]
                urls_list.append(url)
            logging.info('Got the urls list')
            return urls_list
        except Exception as e:
            raise CustomException(e, sys)

    def get_texts(self):
        try:
            urls_list = self.get_urls()
            out_text = []
            total_size = len(urls_list)+1
            for url in urls_list:
                scrap_start = dt.now()
                script = requests.get(url)
                soup_obj = BeautifulSoup(script.content)
                paragraphs = soup_obj.find_all('p')
                for i in paragraphs:
                    out_text.append(i.text)
                st.caption(f'{total_size} {url} Text Extracted In {dt.now()-scrap_start}')
                logging.info(f'{total_size} {url} Text Extracted In {dt.now()-scrap_start}')
                total_size -= 1
                yield out_text
        except Exception as e:
            raise CustomException(e, sys)

    def get_insights(self):
        try:
            text_obj = self.get_texts()
            final_result = []
            raw_data = DataIngesion().get_data(content='Websites List')
            for sentence_list in text_obj:
                processor = TextProcessorAndCounter(sentence_list)
                # AVG SENTENCE LENGTH
                avg_sentence_len = processor.avg_sentence_length()
                # COMPLEX WORD COUNT
                # PERCENTAGE OF COMPLEX WORDS
                # SYLLABLE PER WORD
                complex_word, percentage_complex, syllable_avg = processor.complex_word()
                # FOG INDEX
                fog_index = processor.fog_index()
                # PERSONAL PRONOUNS
                personal_pronouns = processor.personal_pronouns()
                # AVG NUMBER OF WORDS PER SENTENCE
                # WORD COUNT
                # AVG WORD LENGTH
                average_words, word_count, average_word_length = processor.sentences_words_count()

                score_counter = Scores(sentence_list)
                # POSITIVE SCORE
                # NEGATIVE SCORE
                # POLARITY SCORE
                # SUBJECTIVITY SCORE
                p_score, n_score, pol_score, sub_score = score_counter.get_all_scores()

                result = {
                    'POSITIVE SCORE': p_score,
                    'NEGATIVE SCORE': n_score,
                    'POLARITY SCORE': pol_score,
                    'SUBJECTIVITY SCORE': sub_score,
                    'AVG SENTENCE LENGTH': avg_sentence_len,
                    'PERCENTAGE OF COMPLEX WORDS': percentage_complex,
                    'FOG INDEX': fog_index,
                    'AVG NUMBER OF WORDS PER SENTENCE': average_words,
                    'COMPLEX WORD COUNT': complex_word,
                    'WORD COUNT': word_count,
                    'SYLLABLE PER WORD': syllable_avg,
                    'PERSONAL PRONOUNS': personal_pronouns,
                    'AVG WORD LENGTH': average_word_length
                }
                final_result.append(result)

                st.caption(f':green[Total Time Count {dt.now()-self._cur_time}]')
                logging.info(f'Total Time Count {dt.now()-self._cur_time}')
            final_data = pd.DataFrame(final_result)
            data = pd.concat((raw_data, final_data), axis=1)
            data.to_csv(self.config.output_data, index=False)
            st.caption(f':blue[Website Contents Updated In {dt.now()-self._cur_time}]')
            logging.info(f'Website Contents Updated In {dt.now() - self._cur_time}')
        except Exception as e:
            raise CustomException(e, sys)
