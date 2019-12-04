# Scrape website for transcript
def scrape_transcript(url):
    # Import dependencies (just in case)
    import requests
    from bs4 import BeautifulSoup
    import re
    # Get response and content
    response= requests.get(url)
    soup= BeautifulSoup(response.content, 'html.parser')
    # Get paragraphs from the page
    paragraphs= soup.find_all("p")
    # Compile regex patterns
    split_pattern= re.compile('\(*(\d*\:*\d\d\:\d\d)\)*', re.UNICODE)
    # time_pattern= re.compile('\: \((\d*\:*\d\d\:\d\d)\)', re.UNICODE)
    # Create and return lists to add to DF
    time_stamp= []
    speaker_name= []
    speaker_text= []
    section= []
    section_counter= 0
    for i in range(len(paragraphs)):
        try:
            name, time, text= re.split(split_pattern, paragraphs[i].text, maxsplit= 1)
            speaker_name.append(name.replace(":","").strip())
            time_stamp.append(time)
            speaker_text.append(text.strip())
            section.append("Section_"+str(section_counter))
            if re.findall(split_pattern, paragraphs[i].text)[0] == "00:00":
                section_counter+= 1
        except Exception:
            print("ERROR: "+str(i)+" provided no match")
            print(paragraphs[i].text)
    return (section, time_stamp, speaker_name, speaker_text)
    

# Take the scraped transcripts and add them to the bottom of a given df
def transcript_to_df(df, hearing, section, time_stamp, speaker_name, speaker_text):
    # Import dependencies (just in case)
    import pandas as pd
    # Create df to append
    transcript_df= pd.DataFrame({
        "Section": section,
        "Timestamp": time_stamp,
        "Speaker": speaker_name,
        "Text": speaker_text
    })
    transcript_df["Hearing"]= hearing
    new_df= df.append(transcript_df)
    return new_df


# Add a new field to all keys in a given dictionary (assuming value for key is another dict; Ex: Speaker_dict)
def add_new_field_to_dict(dictionary, json_file= False):
    import json

    new_dictionary= dictionary
    print("What field are you adding?")
    field= input("Field: ")
    for key in new_dictionary.keys():
        print(f"What is the value for {key}'s {field}?")
        value= input("Value: ")
        new_dictionary[key][field]= value
    if json_file != False:
        with open(json_file, 'w') as dict_file:
            json.dump(new_dictionary, dict_file, indent= 4)
    return new_dictionary


Alias_dict= {
    "Alexander Vindman": ["A. Vindman", "Lt Col Vindman", "Lt. Col.Vindman","Lt.Col. Vindman"],
    "Adam Schiff": ["Adan Schiff", "Chairman Schiff", "Mr. Chairman", "Mr. Schiff"],
    "Andre Carson": ["André Carson", "Mr. Carson"],
    "Announcer": [],
    "Bill Taylor": [],
    "Brad Wenstrup": ["Dr. Wenstrup"],
    "Camille": [],
    "Chris Stewart": [],
    "Counsel": [],
    "Dan Goldman": ["Goldman", "Mr. Goldman"],
    "Daniel Goldman": [],
    "David Holmes": [],
    "Denny Heck": ["Mr. Heck"],
    "Devin Nunes": ["Mr Nunez", "Mr. Nunes", "Nunes"],
    "Elise Stefanik": ["E. Stefanik", "Ms. Stefanik"],
    "Eric Swalwell": [],
    "Fiona Hill": ["Dr. Fiona Hill"],
    "George Kent": ["Mr. Kent"],
    "Gordon Sondland": ["Sondland"],
    "Jennifer Williams": ["J. WIlliams", "J. Williams", "Ms. Williams"],
    "Jackie Speier": [],
    "Jim Himes": ["Mr. Himes", "Rep Jim Himes"],
    "Jim Jordan": ["Mr. Jordan", "Rep Jim Jordan"],
    "Joaquin Castro": ["Mr. Castro"],
    "John Ratcliffe": ["Mr. Ratcliffe"],
    "Kurt Volker": [],
    "Marie Yovanovitch": ["M. Yovanovitch"],
    "Michael Turner": ["Mr. Turner", "Turner"],
    "Michael Volkov": [],
    "Mike Conaway": ["M. Conaway", "Mr. Conaway"],
    "Mike Quigley": [],
    "Mick Mulvaney": ["Mr. Mulvaney"],
    "Patrick Maloney": [],
    "Peter Welch": ["Mr. Welch"],
    "Pilar Arias": [],
    "Raja Krishnamoorthi": ["Raja K."],
    "Sean Maloney": ["Sean Patrick M."],
    "Speaker 1": [],
    "Speaker 10": [],
    "Speaker 11": [],
    "Speaker 2": [],
    "Speaker 3": [],
    "Speaker 4": [],
    "Speaker 5": [],
    "Speaker 8": [],
    "Steve Castor": ["Caster", "Mr. Caster", "Mr. Castor"],
    "Terri Sewell": ["Ms. Sewell"],
    "Tim Morrison": ["Morrison"],
    "Val Demings": [],
    "Will Hurd": ["Mr. Hurd"]
}

def change_name(pd_Series):
    new_pd_Series= pd_Series
    for df_speaker in new_pd_Series:
        if df_speaker not in Alias_dict.keys():
            for dict_speaker in Alias_dict.keys():
                if df_speaker in Alias_dict[dict_speaker]:
                    print(f"Changing {df_speaker} to {dict_speaker}")
                    df_speaker= dict_speaker
                    break
    return new_pd_Series

def timestamp_to_int(timestamp):
    try:
        timestamp_list= timestamp.split(":")
        hours= 0
        minutes= 0
        seconds= 0
        if len(timestamp_list) == 2:
            minutes= int(timestamp_list[0])
            seconds= int(timestamp_list[1])
        elif len(timestamp_list) == 3:
            hours= int(timestamp_list[0])
            minutes= int(timestamp_list[1])
            seconds= int(timestamp_list[2])
        minutes *= 60
        hours *= (60 * 60)
        print(f"Hours= {hours}\nMinutes= {minutes}\nSeconds= {seconds}")
        time= seconds + minutes + hours
        return time
    except Exception as e:
        print("*"*20)
        print(f"Failed: {timestamp}")
        print(e)
        print("*"*20)