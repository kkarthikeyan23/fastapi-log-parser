import re
import pandas as pd
import json
from _datetime import timedelta, datetime as dt
from App.email_alert import send_email
import os

print("🚀 FastAPI code version: NEW build loaded")



#Initialize log values
#count the number of errors
def log_parse():
    count_logs = { "notice": 0, "error": 0 }
    error_only_logs = []

    # 🔹 Ensure output folder exists
    output_dir = "out"
    os.makedirs(output_dir, exist_ok=True)

    # 🔹 Use absolute path for the log file
    log_file_path = os.path.join(os.getcwd(), "Apache_2k.log")

    # Open the file and read its contents

    with open(log_file_path, "r") as file:
        for eachline in file:
            for key, value in count_logs.items():
                if key in eachline:
                    count_logs[key] += 1
            if "error" in eachline:  # filter error only rows
                error_only_logs.append(eachline.strip())

    #pattern matching with re string
    pattern = r"""
        (?P<Timestamp>\[\w+\s+\w+\s+\d{2}\s+\d{2}:\d{2}:\d{2}\s+\d{4}\])  # timestamp
        \s*
        (?P<level>\[\w+\])                                               # log level
        \s*
        (?P<message>.*)                                                  # message   
        """
     #Create list of dictionary of errors matched
    error_list = []
    for error_line in error_only_logs:
        match = re.search(pattern, error_line, re.VERBOSE)
        if match:
            group = match.groupdict()
            error_list.append(group)
        else:
            print(f"this line failed to match regex:{error_line}")

    print(f"Total errors:{len(error_list)}")
    print(f"Sample Errors: {error_list[:5]}")

    #Write to a Dataframe
    df = pd.DataFrame(error_list)
    # print(df)
    now = dt.now()

    # remove [] from Timestamp and level columns
    df["Timestamp"] = df["Timestamp"].str.strip("[]")
    df["level"] = df["level"].str.strip("[]")

    #Change to dataframe time
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%a %b %d %H:%M:%S %Y", errors ="coerce")

    #removes incorrect timestamp values( NaT)  and saves back to df
    df = df.dropna(subset=["Timestamp"])

    # 🔹 Write outputs to /out folder
    csv_path = os.path.join(output_dir, f"error_filtered_logs_{now.strftime('%Y%m%d_%H%M%S')}.csv")
    json_path = os.path.join(output_dir, f"error_filtered_logs_{now.strftime('%Y%m%d_%H%M%S')}.json")

    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=4)


     #finding last one hour time value
    time_delta = now - timedelta(hours=1)
    print(time_delta)

    #Find the number of errors during last 1 hr
    number_of_errors = df[df["Timestamp"] >= time_delta].shape[0]

    print(f"Current time: {now}, Errors in last hour {number_of_errors}")

    #Write to an email if errors are >10 in last 1 hour
    if number_of_errors > 10:
            send_email(number_of_errors)
    else:
            print("The error count is under threshold")

    print(count_logs)
    return count_logs,number_of_errors
