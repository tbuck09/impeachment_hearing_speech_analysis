import os
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import nltk

from util import timestamp_to_int


# Establish paths and variables
cwd= os.getcwd()
plot_path= os.path.join(cwd,"plots")
transcript_filename= "Hearings_data.csv"


# Read JSON
speaker_dict= json.load(open('speaker_info.json'))


# Create df
transcript_df= pd.read_csv(transcript_filename, encoding='latin1')


# Append columns to df
## Integer-ized timestamps
transcript_df["int_timestamp"]= transcript_df.Timestamp.apply(timestamp_to_int)
## Speaker Duration
## At this time I don't have a way to mitigate when the timestamp resets to 00:00 within a hearing (such as a Hearing or Section change).
## These values are np.nan for now.
transcript_df["duration"]= 0
for i in range(len(transcript_df) - 1):
    duration= transcript_df.int_timestamp[i + 1] - transcript_df.int_timestamp[i]
    if duration < 0:
        transcript_df.duration[i]= np.nan
    else:
        transcript_df.duration[i]= duration


# Plots
## Speaker (approximate) total time
def create_speaker_duration_plot():
    total_duration_by_speaker= transcript_df.groupby("Speaker")["duration"].sum().sort_values(ascending= False).reset_index()
    fig, ax= plt.subplots(figsize= (15,7.5))
    plt.gcf().subplots_adjust(bottom= .55)
    ypos= np.arange(len(total_duration_by_speaker.Speaker))
    ax.bar(ypos, total_duration_by_speaker.duration)
    ax.set_title("(Approximate) Duration of Speaking by Speaker")
    ax.set_xticks(ypos)
#
    def ticklabel_string(speaker):
        try:
            if speaker_dict[speaker]['Position'] == 'Rep.':
                ticklabel= f"{speaker} ({speaker_dict[speaker]['Position']} - {speaker_dict[speaker]['Party']})"
            else:
                ticklabel= f"{speaker} ({speaker_dict[speaker]['Position']})"
        except Exception:
            ticklabel= speaker
        finally:
            return ticklabel
#
    ticklabel_list= total_duration_by_speaker.Speaker.apply(ticklabel_string)
    ax.set_xticklabels(ticklabel_list, rotation= 270)
    ax.set_xlabel("Speaker")
    ax.set_ylabel("Duration in Seconds")
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path,"Speaker_Duration.jpg"))
    plt.show()