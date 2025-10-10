#This log parser will provide
# 1. Counts of error logs and uses FastAPI to provide the results
# 2. save error logs into a csv & json files
# 3. check th error counts > 10 in 1 hour - Send alert to the email
from fastapi import FastAPI
from App.parser import log_parse

app = FastAPI()


#FastApi to serve logs_count,number_of_errors
@app.get("/logs/", summary = "Get log counts and recent errors")
def read_logs():
    logs_count,number_of_errors = log_parse()
    return {"Logs": logs_count,
            "ErrorsLastHours":number_of_errors}

