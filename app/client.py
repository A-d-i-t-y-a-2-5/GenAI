import os

import pandas as pd
import streamlit as st

from scraper.extractor import get_linkedin_page
from scraper.llm import LanguageModel
from app.settings import AppSettings
from app.utils import copy_firefox_cookies, load_cookies_from_file

config = AppSettings()
llm = LanguageModel(config)

copy_firefox_cookies(config.os_username, os.curdir)
cookies = load_cookies_from_file(
    os.path.join(os.curdir, "copied_cookies.sqlite"), domain_name=".linkedin.com"
)


st.set_page_config(layout="wide")
num_rows = 25

col1, col2, col3 = st.columns(3)

with col1:
    title = st.text_input(
        "Keywords", placeholder="Specify keywords to search for in the LinkedIn profile"
    )
with col2:
    sort_by = st.selectbox(
        "Sort by",
        ["relevance", "date_posted"],
        format_func=lambda x: x.replace("_", " ").title(),
    )
with col3:
    date_posted = st.selectbox(
        "Date Posted",
        ["past-24h", "past-week", "past-month"],
        format_func=lambda x: x.replace("-", " ").title(),
    )

if st.button("Submit", type="primary", use_container_width=True):
    with st.spinner("Extracting job postings from LinkedIn...", show_time=True):
        doc = get_linkedin_page(
            f'https://www.linkedin.com/search/results/content/?keywords={title}&sortBy=["{sort_by}"]&datePosted=["{date_posted}"]',
            cookies=cookies,
            password=config.extractor.password,
            scroll_duration=config.extractor.scroll_duration,
        )

    with st.spinner("Generating structured data from job postings...", show_time=True):
        inputs = llm.split_document(doc)
        response = llm.generate_response(llm.generate_inputs(inputs))
        
    records = [job.model_dump() for job in response.jobs]
    df = pd.DataFrame(records)

    st.dataframe(df, height=(num_rows + 1) * 35 + 3)
    
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False),
        file_name="job_postings.csv",
        mime="text/csv"
    )
