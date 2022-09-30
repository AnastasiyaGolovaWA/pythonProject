import pandas as pd

from feature2.app.service.pandas_service import get_anonymous, get_flow_steps, get_subject_flow_history, \
    get_ids_user_interest


def get_user_interest_objective(filename: str):
    # Reading in the data
    ids = get_ids_user_interest()
    flow_steps = get_flow_steps()
    sfh = get_subject_flow_history()
    anonymous = get_anonymous()
    # %%
    # Setting detailed view and email lists
    detailed_ev = flow_steps["detailed_view"]
    email = ids["email"]
    # %%
    # Matching event name to detailed event name and adding to sfh dataframe

    i = 0
    code_list = []
    while i < len(sfh):
        # matching event name to numerical event code
        event = sfh["event_name"][i]
        boolkey2 = event == flow_steps["event_name"]
        ev_key = [k for k, x in enumerate(boolkey2) if x]
        if ev_key != []:
            detailed = detailed_ev[ev_key[0]]
            code_list.append(detailed)
        else:
            detailed = "N/A"
            code_list.append(detailed)
        i += 1

    sfh["detailed_view"] = code_list
    # %%
    # Determining email mask
    email_list = [" ", " "]
    ct = 0
    i = 0
    while i < len(ids):
        if ids["email"][i] != []:
            ct = ct + 1
            email = "Email" + str(ct)
        else:
            email = "N/A"

        email_list.append(email)
        i += 1
    # %%
    # Determining Subject ID list
    subject_ids = [" ", " "]
    i = 0
    while i < len(ids):
        if ids["subject_id"][i] != []:
            s_id = ids["subject_id"][i]
        else:
            s_id = "N/A"

        subject_ids.append(s_id)
        i += 1
    # %%
    # Determining current/last subject status
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

    status_list = [" ", " "]
    s_textlist = [" ", " "]
    for stat_int in status_int_list:
        boolkey = stat_int == flow_steps["id"]
        id_key = [j for j, x in enumerate(boolkey) if x]
        if id_key != []:
            status_code = flow_steps["code"][id_key[0]]
            status_list.append(status_code)
            status_text = flow_steps["detailed_view"][id_key[0]]
            s_textlist.append(status_text)
        else:
            status_code = "N/A"
            status_list.append(status_code)
            status_text = "N/A"
            s_textlist.append(status_text)
    # %%
    # Ordering flow_steps table by chronological study step
    fs_sorted = flow_steps.sort_values("id")
    sorted_series = fs_sorted["detailed_view"][1:-3]
    sorted_list = sorted_series.tolist()
    # %%
    # Creating anonymous id list
    series_a = ids["anonymous_id"][:]
    list_a = series_a.tolist()
    anon = [" ", " "] + list_a
    # %%
    # Setting up User Interest - Objective Table
    columns = ["First ts", "Anonymous ID", "Email", "Subject ID", "Current/Final Subject Status Code",
               "Current/Final Subject Status Text"]

    columns = columns + sorted_list

    user_int = pd.DataFrame(columns=columns)

    user_int["Anonymous ID"] = anon
    user_int["Email"] = email_list
    user_int["Subject ID"] = subject_ids
    user_int["Current/Final Subject Status Code"] = status_list
    user_int["Current/Final Subject Status Text"] = s_textlist

    # %%
    # Setting up User Interest - Objective Table pt 2

    sorted_codes = fs_sorted["code"][1:-3]
    s_codes_list = sorted_codes.tolist()
    summ = fs_sorted["simple_view"][1:-3]
    summ_list = summ.tolist()

    i = 0
    for col in sorted_list:
        user_int.loc[0, col] = s_codes_list[i]
        user_int.loc[1, col] = summ_list[i]
        i += 1

    # %%
    # Filling User Interest - Objective Table
    i = 1
    for anon_id in anon:
        if anon_id != " ":
            i += 1
            bkey = anon_id == sfh["anonymous_id"]
            id_keys = [j for j, x in enumerate(bkey) if x]
            if id_keys != []:
                for id_key in id_keys:
                    d_event = sfh["detailed_view"][id_key]
                    if d_event in user_int:
                        user_int.loc[i, d_event] = sfh["timestamp"][id_key]

    # %%
    user_int.to_csv(filename + ".csv")


if __name__ == '__main__':
    get_user_interest_objective("5UserInterestObjective")
