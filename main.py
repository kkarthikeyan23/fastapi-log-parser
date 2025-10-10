#This log parser will provide
# 1. Counts of error logs and uses FastAPI to provide the results
# 2. save error logs into a csv & json files
# 3. check th error counts > 10 in 1 hour - Send alert to the email
from fastapi import FastAPI
import re
import pandas as pd
import json
from _datetime import timedelta, datetime as dt
import smtplib
from dotenv import load_dotenv
import os


print("🚀 FastAPI code version: NEW build loaded")

load_dotenv()

my_email = os.getenv("MY_EMAIL")
password = os.getenv("EMAIL_PASSWORD")
to_email = os.getenv("TO_EMAIL")



#Initialize log values
#count the number of errors

app = FastAPI()

# Open the file and read its contents
def log_parse():
    count_logs = { "notice": 0, "error": 0 }
    error_only_logs = []

    with open("Apache_2k.log", "r") as file:
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

    # Dataframe to csv file
    df.to_csv(f"error_filtered_logs_{now.strftime('%Y%m%d_%H%M%S')}.csv", index=False)

    #Dataframe to json
    json_data = df.to_json(orient="records", indent=4)


     #finding last one hour time value
    time_delta = now - timedelta(hours=1)
    print(time_delta)

    #Find the number of errors during last 1 hr
    number_of_errors = df[df["Timestamp"] >= time_delta].shape[0]

    print(f"Current time: {now}, Errors in last hour {number_of_errors}")

    #Write to an email if errors are >10 in last 1 hour
    if number_of_errors > 10:
            subject = "Critical Errors detected for app "
            body = f"Average Error rate's value {number_of_errors} was greater than the threshold value of 10 in 1 hour "
            message = f"Subject:{subject}\n{body}"
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email,
                                    to_addrs=to_email,
                                    msg=message.encode("utf-8"))
    else:
            print("The error count is under threshold")

    print(count_logs)
    return count_logs,number_of_errors

#FastApi to serve logs_count,number_of_errors
@app.get("/logs/", summary = "Get log counts and recent errors")
def read_logs():
    logs_count,number_of_errors = log_parse()
    return {"Logs": logs_count,
            "ErrorsLastHours":number_of_errors}

