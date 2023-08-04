import streamlit as st
from src.components.data_ingesion import DataIngesion
from src.components.web_scrapper import InitiateScrapping
from src.utils import download
from datetime import datetime as dt
DataIngesion()

tab1, tab2, tab3 = st.tabs([
    'Data Viewer', 'Data Downloader', 'Data Updater'
])
with tab1:
    selection = st.selectbox(
        'Select data',
        ('Websites List', 'Website Contents')
    )
    data = DataIngesion().get_data(content=selection)
    st.dataframe(data, hide_index=True)
    st.caption('Hover on the data and tap extend on right top for full screen view')
with tab2:
    download()
with tab3:
    with st.form('Form'):
        submitted = st.form_submit_button('Update Website Contents Data')
        st.caption('*Note: Updating of data will take near to 30 min')
        if submitted:
            InitiateScrapping(dt.now()).get_insights()
