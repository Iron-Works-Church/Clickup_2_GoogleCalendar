#!/bin/env python
from __future__ import print_function
from datetime import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import *
from googleapiclient import sample_tools
import pprint
import boto3

ssm = boto3.client('ssm')
sns = boto3.client('sns')
sns_topic = ssm.get_parameter(Name='sns_darin')["Parameter"]["Value"]
google_calendar_id = ssm.get_parameter(Name='google_calendar_id')["Parameter"]["Value"]

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_google_calendar(entry):
    creds = None
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    service = build('calendar', 'v3', credentials=creds)
    calendar_list = service.calendarList().list().execute()
    start_date = int(entry["start_date"]) / 1000
    end_date = int(entry["due_date"]) / 1000
    start_date = datetime.fromtimestamp(start_date)
    start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S")
    end_date = datetime.fromtimestamp(end_date)
    end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S")

    event = {
  'summary': entry["name"],
  'location': "Iron Works Church",
  'description': entry["content"],
  'start': {
    'dateTime': start_date,
    'timeZone': 'Etc/UTC',
  },
  'end': {
    'dateTime': end_date,
    'timeZone': 'Etc/UTC',
  },


  'reminders': {
    'useDefault': False,
 
  },
}
    service = build('calendar', 'v3', credentials=creds)
    event = service.events().insert(calendarId=google_calendar_id, body=event).execute()
    sns.publish(TopicArn=sns_topic, Message=('Event created: %s' % (event.get('htmlLink'))))




#create_google_calendar("test")
