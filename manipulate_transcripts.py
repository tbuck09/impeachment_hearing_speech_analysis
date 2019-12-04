import os

import numpy as np
import pandas as pd
import nltk

from util import timestamp_to_int


# Establish paths and variables
transcript_filename= "Hearings_data.csv"


# Create df
transcript_df= pd.read_csv(transcript_filename, encoding='latin1')


# Append columns to df
## Integer-ized timestamps
transcript_df["int_timestamp"]= transcript_df.Timestamp.apply(timestamp_to_int)
## Speaker Duration
## At this time I don't have a way to mitigate when the timestamp resets to 00:00 within a hearing (such as a Section change).
## These values are np.nan for now.
transcript_df["duration"]= 0
for i in range(len(transcript_df) - 1):
    duration= transcript_df.int_timestamp[i + 1] - transcript_df.int_timestamp[i]
    if duration < 0:
        transcript_df.duration[i]= np.nan
    else:
        transcript_df.duration[i]= duration