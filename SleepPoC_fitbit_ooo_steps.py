import json
from datetime import datetime, timedelta

import pandas as pd

# %%
# Opening JSON files

# sleep data file
f = open('sleep-2022-09-11.json')

# steps evening date file
f0 = open('act_steps-2022-09-10.json')

# Steps morning date file
f1 = open('act_steps-2022-09-11.json')

# returns JSON object as a dictionary
sleep = json.load(f)
steps1 = json.load(f0)
steps2 = json.load(f1)

# %%
# determining sleep session
y = len(sleep["sleep"][0]["levels"]["data"])

sleep_s = []
date_s = []
time_s = []
level_s = []
length_s = []
i = 0
for i in range(0, y):
    if sleep["sleep"][0]["levels"]["data"][i]["level"] != "wake":
        date_s.append(sleep["sleep"][0]["levels"]["data"][i]["dateTime"][0:10])
        time_s.append(sleep["sleep"][0]["levels"]["data"][i]["dateTime"][11:19])
        level_s.append(sleep["sleep"][0]["levels"]["data"][i]["level"])
        length_s.append(sleep["sleep"][0]["levels"]["data"][i]["seconds"])

sleep_df = pd.DataFrame(columns=["date", "time", "stage", "length (s)"])
sleep_df["date"] = date_s
sleep_df["time"] = time_s
sleep_df["stage"] = level_s
sleep_df["length (s)"] = length_s

# Adding end time of last sleep stage to df

last_time = datetime.strptime(sleep_df["date"].iloc[-1] + " " + sleep_df["time"].iloc[-1],
                              '%Y-%m-%d %H:%M:%S') + timedelta(seconds=sleep_df["length (s)"].iloc[-1].item())
time_l = last_time.strftime("%m/%d/%Y, %H:%M:%S")[12:20]

k = len(sleep_df)

sleep_df.loc[k, "date"] = date_s[-1]
sleep_df.loc[k, "time"] = time_l

# %%
# Putting all evening date minutes where step count >= 15 into df
x = len(steps1['activities-steps-intraday']['dataset'])

day1 = steps1['activities-steps'][0]["dateTime"]

times = []
steps = []
i = 0
for i in range(0, x):
    if steps1['activities-steps-intraday']['dataset'][i]['value'] >= 15:
        times.append(steps1['activities-steps-intraday']['dataset'][i]['time'])
        steps.append(steps1['activities-steps-intraday']['dataset'][i]['value'])

date1 = [day1] * len(steps)
out = pd.DataFrame(columns=["date", "times", "steps"])
out["date"] = date1
out["times"] = times
out["steps"] = steps

# Adding all morning date minutes where step count >= 15 to df

y = len(steps2['activities-steps-intraday']['dataset'])
day2 = steps2['activities-steps'][0]["dateTime"]

i = 0
for i in range(0, y):
    z = len(out)
    if steps2['activities-steps-intraday']['dataset'][i]['value'] >= 15:
        out.loc[z, "date"] = day2
        out.loc[z, "times"] = steps2['activities-steps-intraday']['dataset'][i]['time']
        out.loc[z, "steps"] = steps2['activities-steps-intraday']['dataset'][i]['value']
# %%
# finding last minute before first sleep stage where steps >= 15

i = 0
y = len(out)

start_dt = datetime.strptime(sleep_df["date"].iloc[0] + " " + sleep_df["time"].iloc[0], '%Y-%m-%d %H:%M:%S')
start_steps = []
while i < y:
    comp_dt = datetime.strptime(out["date"].iloc[i] + " " + out["times"].iloc[i], '%Y-%m-%d %H:%M:%S')
    if comp_dt < start_dt:
        text = datetime.strftime(comp_dt, '%Y-%m-%d %H:%M:%S')
        start_steps.append(text)
    i += 1

ttb = start_steps[-1]

print("Time Entering Bed should be one minute after " + ttb)
# %%
# finding first minute after last sleep stage where steps >= 15

i = 0
y = len(out)

end_dt = datetime.strptime(sleep_df["date"].iloc[-1] + " " + sleep_df["time"].iloc[-1], '%Y-%m-%d %H:%M:%S')
end_steps = []
while i < y:
    comp_dt = datetime.strptime(out["date"].iloc[i] + " " + out["times"].iloc[i], '%Y-%m-%d %H:%M:%S')
    if comp_dt > end_dt:
        text = datetime.strftime(comp_dt, '%Y-%m-%d %H:%M:%S')
        ttg = text
        i = y + 1

    i += 1

print("Time of Final Bed Exit should be one minute before " + ttg)
