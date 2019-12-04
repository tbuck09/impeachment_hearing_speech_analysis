# Import dependencies
import os
import re
import json

import requests
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Custom imports
from util import scrape_transcript, transcript_to_df

# Read JSON
Speaker_dict= json.load(open("speaker_info.json"))


# URLs
url_list= [
    "https://www.rev.com/blog/impeachment-hearings-first-day-transcript-bill-taylor-george-kent-testimony-transcript",
    "https://www.rev.com/blog/impeachment-hearing-transcript-day-2-marie-yovanovitch-testimony",
    "https://www.rev.com/blog/impeachment-hearing-day-3-transcript-alexander-vindman-jennifer-williams-testify",
    "https://www.rev.com/blog/impeachment-hearing-day-3-transcript-kurt-volker-tim-morrison-testify",
    "https://www.rev.com/blog/impeachment-hearing-day-4-transcript-gordon-sondland-testifies",
    "https://www.rev.com/blog/impeachment-hearing-day-5-transcript-fiona-hill-and-david-holmes-testimony"
]

hearings_df= pd.DataFrame()
for url in url_list:
    hearing= input("Which hearing is this? ")
    section,time_stamp,speaker_name,speaker_text= scrape_transcript(url)
    hearings_df= transcript_to_df(
        hearings_df,
        hearing,
        section,
        time_stamp,
        speaker_name,
        speaker_text
    )

print(len(hearings_df))