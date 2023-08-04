from src.exception import CustomException
from src.logger import logging
from src.components.data_ingesion import DataIngesion
from dataclasses import dataclass
import pandas as pd
import numpy as np
import streamlit as st
import os
import sys
import dill
import warnings
warnings.filterwarnings('ignore')


def save_obj(obj, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as file:
        dill.dump(obj, file)
        logging.info(f'File {path} saved successfully')


def load_obj(path: str):
    with open(path, 'rb') as file:
        file_obj = dill.load(file)
        logging.info(f'File {path} loaded successfully')
        return file_obj

def file_uploader():
    uploaded_file = st.file_uploader("Choose a file")

def download():
    try:
        col1, col2 = st.columns(2)
        with col1:
            option = st.selectbox(
                'Select data',
                ('Website Contents', 'Websites List')
            )
        with col2:
            st.caption('Download as csv')
            csv = DataIngesion().get_data(option).to_csv(index=False).encode('utf-8')
            st.download_button(label="Download", data=csv, file_name=option+'.csv', mime='text/csv')
        logging.info(f'Downloaded the {option} file')
    except Exception as e:
        raise CustomException(e, sys)
