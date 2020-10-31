#!/bin/env python
import requests
import json
import pprint
from googlecalendar import *
from datetime import datetime
import boto3

ssm = boto3.client('ssm')
sns = boto3.client('sns')
token = ssm.get_parameter(Name='clickup')["Parameter"]["Value"]
sns_topic = ssm.get_parameter(Name='sns_darin')["Parameter"]["Value"]
clickup_url = "https://api.clickup.com/api/v2/"
headers = {'Authorization': token}

def lambda_handler(event, context):
    lists = get_lists()
    get_tasks(lists)

def get_lists():
    url = ''.join([clickup_url, "space/10563530/list"])
    response = requests.get(url, headers=headers)
    response = response.json()
    return(response["lists"])

def get_tasks(lists):
    params = {"archived": False, "include_closed": False}
    for i in lists:    
        url = ''.join([clickup_url, "list/", i["id"], "/task"])
        response = requests.get(url, headers=headers, params=params)
        response = response.json()
        for i2 in response["tasks"]:
            try:
                if i2["tags"][0]["name"] == "add-to-google-calendar" and i2["status"]["status"] != "Closed":
                    create_google_calendar(i)
                    close_task(i2)
            except:
                exception = True



def close_task(task):
    payload = {"archived": False, "status": "Closed"}
    url = ''.join([clickup_url, "task/", task["id"]])
    response = requests.put(url, headers=headers, data=payload)
    response = response.json()
    pprint.pprint(response)

lambda_handler("test", "test")

