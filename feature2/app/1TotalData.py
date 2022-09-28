import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date

from feature2.app.service.pandas_service import get_quality_control, get_anonymous, get_flow_steps, \
    get_subject_flow_history

# %%
# Reading in the data
ids = pd.read_csv("IDs.csv")
qc = get_quality_control()
anonymous = get_anonymous()
flow_steps = get_flow_steps()
subject_flow_history = get_subject_flow_history()
# %%
subject_id = ids["subject_id"]
startdates = ids["study_start_date"]
upload_date = qc["date"]
# %%
# Matching subject_participant_id and to Subject ID and subject's start date

i = 0
s_id_list = []
s_date_list = []
while i < len(qc):
    sp2_id = qc["study_participant_id"][i]
    boolkey = sp2_id == ids["study_participant_id"]
    id_key = [j for j, x in enumerate(boolkey) if x]
    if id_key != []:
        s_id = subject_id[id_key[0]]
        s_id_list.append(s_id)
        s_sd = startdates[id_key[0]]
        s_date_list.append(s_sd)
    else:
        s_id = "N/A"
        s_id_list.append(s_id)
        s_sd = "1990-01-01"
        s_date_list.append(s_sd)
    i += 1

qc["subject_id"] = s_id_list
qc["sub_start_date"] = [datetime.date(datetime.strptime(b, '%Y-%m-%d')) for b in s_date_list]
qc["up_date"] = [datetime.date(datetime.strptime(c, '%Y-%m-%d')) for c in upload_date]
# %%
# Determining current subject status
anon_id = ids["anonymous_id"]
status_int_list = []
for a_id in anon_id:
    boolkey = a_id == anonymous["anonymous_id"]
    id_key = [j for j, x in enumerate(boolkey) if x]
    if id_key != []:
        status_int = anonymous["current_subject_flow_step_id"][id_key[0]]
        status_int_list.append(status_int)
    else:
        status_int = "N/A"
        status_int_list.append(status_int)

status_list = []
for stat_int in status_int_list:
    boolkey = stat_int == flow_steps["id"]
    id_key = [j for j, x in enumerate(boolkey) if x]
    if id_key != []:
        status_code = flow_steps["code"][id_key[0]]
        status_list.append(status_code)
    else:
        status_code = "N/A"
        status_list.append(status_code)
# %%
# Determining current study day from IDs table
today = date.today()
date_list = []
for date in ids["study_start_date"]:
    start_dt = datetime.strptime(date, '%Y-%m-%d')
    start_date = datetime.date(start_dt)
    delta = today - start_date
    if len(str(delta)) == 14:
        delta_int = 1
    elif len(str(delta)) == 7:
        delta_int = 0
    else:
        delta_int = int(str(delta)[0:-14])
    if delta_int > 14:
        delta_int = 14
    if delta_int < 0:
        delta_int = " "
    date_list.append(delta_int)
# %%
# Making two rows (one per week) for each subject ID, subject status, and study day
subject_id = [val for val in subject_id for _ in (0, 1)]
status_list = [val0 for val0 in status_list for _ in (0, 1)]
date_list = [val1 for val1 in date_list for _ in (0, 1)]
# %%
# Creating column headers and Subject ID rows + populating current status and study day data
totaldata = pd.DataFrame(
    columns=["Subject", "Week", "Current Subject Status", "Current Subject Study Day", "Fitbit - Sleep",
             "Fitbit - Heart Rate", "Fitbit - Steps", "Withings - Sleep Summary", "Withings - Sleep Detailed",
             "Study App - NB", "Study App - ISI", "Study App - EMA - BM", "Study App - EMA - Morning",
             "Study App - EMA - Evening", "Study App - Sleep Diary"])
totaldata["Subject"] = subject_id
totaldata["Week"] = [1, 2] * int((len(subject_id) / 2))
totaldata["Current Subject Status"] = status_list
totaldata["Current Subject Study Day"] = date_list
totaldata["Fitbit - Sleep"] = [0] * len(subject_id)
totaldata["Fitbit - Heart Rate"] = [0] * len(subject_id)
totaldata["Fitbit - Steps"] = [0] * len(subject_id)
totaldata["Withings - Sleep Summary"] = [0] * len(subject_id)
totaldata["Withings - Sleep Detailed"] = [0] * len(subject_id)
totaldata["Study App - NB"] = [0] * len(subject_id)
totaldata["Study App - ISI"] = [0] * len(subject_id)
totaldata["Study App - EMA - BM"] = [0] * len(subject_id)
totaldata["Study App - EMA - Morning"] = [0] * len(subject_id)
totaldata["Study App - EMA - Evening"] = [0] * len(subject_id)
totaldata["Study App - Sleep Diary"] = [0] * len(subject_id)
# %%
# Populating table from QC data
i = 0
while i < len(qc):
    # filtering for data files marked as successfully uploaded
    if qc["status"][i] == "SUCCESS":
        sub_id = qc["subject_id"][i]
        strm = qc["stream"][i]
        typ = qc["type"][i]
        # finding matching subject ID from total data df
        if sub_id != "N/A":
            boolkey = sub_id == totaldata["Subject"]
            id_key = [j for j, x in enumerate(boolkey) if x]
            # determining which week the data file was uploaded during
            week12 = qc["up_date"][i] - qc["sub_start_date"][i]
            if len(str(week12)) == 14:
                week_int = 1
            elif len(str(week12)) == 7:
                week_int = 0
            else:
                week_int = int(str(week12)[0:-14])
            # determining data file type and adding to current tally of files for that file type and week per subject
            if week_int < 8:
                if strm == "sleep" and typ == "fitbit":
                    totaldata.loc[id_key[0], "Fitbit - Sleep"] = totaldata["Fitbit - Sleep"][id_key[0]] + 1
                elif strm == "hr" and typ == "fitbit":
                    totaldata.loc[id_key[0], "Fitbit - Heart Rate"] = totaldata["Fitbit - Heart Rate"][id_key[0]] + 1
                elif strm == "activities" and typ == "fitbit":
                    totaldata.loc[id_key[0], "Fitbit - Steps"] = totaldata["Fitbit - Steps"][id_key[0]] + 1
                elif strm == "summary" and typ == "withings":
                    totaldata.loc[id_key[0], "Withings - Sleep Summary"] = totaldata["Withings - Sleep Summary"][
                                                                               id_key[0]] + 1
                elif strm == "sleep" and typ == "withings":
                    totaldata.loc[id_key[0], "Withings - Sleep Detailed"] = totaldata["Withings - Sleep Detailed"][
                                                                                id_key[0]] + 1
                elif strm == "nb" and typ == "app":
                    totaldata.loc[id_key[0], "Study App - NB"] = totaldata["Study App - NB"][id_key[0]] + 1
                elif strm == "isi" and typ == "app":
                    totaldata.loc[id_key[0], "Study App - ISI"] = totaldata["Study App - ISI"][id_key[0]] + 1
                elif strm == "ema_morning" and typ == "app":
                    totaldata.loc[id_key[0], "Study App - EMA - Morning"] = totaldata["Study App - EMA - Morning"][
                                                                                id_key[0]] + 1
                elif strm == "ema_evening" and typ == "app":
                    totaldata.loc[id_key[0], "Study App - EMA - Evening"] = totaldata["Study App - EMA - Evening"][
                                                                                id_key[0]] + 1
                elif strm == "sleep_diary" and typ == "app":
                    totaldata.loc[id_key[0], "Study App - Sleep Diary"] = totaldata["Study App - Sleep Diary"][
                                                                              id_key[0]] + 1
                else:
                    totaldata.loc[id_key[0], "Study App - EMA - BM"] = totaldata["Study App - EMA - BM"][id_key[0]] + 1
            else:
                if strm == "sleep" and typ == "fitbit":
                    totaldata.loc[id_key[1], "Fitbit - Sleep"] = totaldata["Fitbit - Sleep"][id_key[1]] + 1
                elif strm == "hr" and typ == "fitbit":
                    totaldata.loc[id_key[1], "Fitbit - Heart Rate"] = totaldata["Fitbit - Heart Rate"][id_key[1]] + 1
                elif strm == "activities" and typ == "fitbit":
                    totaldata.loc[id_key[1], "Fitbit - Steps"] = totaldata["Fitbit - Steps"][id_key[1]] + 1
                elif strm == "summary" and typ == "withings":
                    totaldata.loc[id_key[1], "Withings - Sleep Summary"] = totaldata["Withings - Sleep Summary"][
                                                                               id_key[1]] + 1
                elif strm == "sleep" and typ == "withings":
                    totaldata.loc[id_key[1], "Withings - Sleep Detailed"] = totaldata["Withings - Sleep Detailed"][
                                                                                id_key[1]] + 1
                elif strm == "nb" and typ == "app":
                    totaldata.loc[id_key[1], "Study App - NB"] = totaldata["Study App - NB"][id_key[1]] + 1
                elif strm == "isi" and typ == "app":
                    totaldata.loc[id_key[1], "Study App - ISI"] = totaldata["Study App - ISI"][id_key[1]] + 1
                elif strm == "ema_morning" and typ == "app":
                    totaldata.loc[id_key[1], "Study App - EMA - Morning"] = totaldata["Study App - EMA - Morning"][
                                                                                id_key[1]] + 1
                elif strm == "ema_evening" and typ == "app":
                    totaldata.loc[id_key[1], "Study App - EMA - Evening"] = totaldata["Study App - EMA - Evening"][
                                                                                id_key[1]] + 1
                elif strm == "sleep_diary" and typ == "app":
                    totaldata.loc[id_key[1], "Study App - Sleep Diary"] = totaldata["Study App - Sleep Diary"][
                                                                              id_key[1]] + 1
                else:
                    totaldata.loc[id_key[1], "Study App - EMA - BM"] = totaldata["Study App - EMA - BM"][id_key[1]] + 1

    i = i + 1
# %%
# Write dataframe to Excel file
totaldata.to_csv("1TotalData.csv")