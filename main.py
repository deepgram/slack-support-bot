# -*- coding: utf-8 -*-

# This is a sample Python script.
import os
import json
import requests
from slackeventsapi import SlackEventAdapter

# Read the SLACK_SIGNING_SECRET environment variable from the host machine and initialize the event adapter at the endpoint you'd like to handle requests
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, endpoint="/slack/events")


# Create an event listener for "app_mention" events
@slack_events_adapter.on("app_mention")
# Define function to POST mention event data to Zendesk "Create Ticket" Zap
def zapier_zendesk_create(event_data):
  event_details = event_data["event"]
  url = "MENTION_EVENT_ZAP_URL"
  post_to_zap = requests.post(url, data=event_details)
  print(post_to_zap.content)


# Create an event listener for "reaction_added" events
@slack_events_adapter.on("reaction_added")
def zapier_zendesk_react_create(event_data):
  event_details = event_data["event"]
  item_details = event_details["item"]
  reaction = {"reaction": event_details["reaction"]}
  item_user = {"item_user": event_details["item_user"]}
  user = {"user":event_details["user"]}
  item_details.update(reaction)
  item_details.update(item_user)
  item_details.update(user)
  print(json.dumps(item_details))
  if event_details["reaction"] == "link":
    url = "LINK_EVENT_ZAP_URL"
  if event_details["reaction"] == "black_square_for_stop":
    url = "CLOSE_EVENT_ZAP_URL"
  if event_details["reaction"] == "mega":
    url = "MEGAPHONE_EVENT_ZAP_URL"
  post_to_zap = requests.post(url, data=item_details)
  print(post_to_zap.content)
  
# Create an event listener for "message.groups" events
@slack_events_adapter.on("message")
def zendesk_update_slack_reply(event_data):
  message = event_data["event"]
  print(message)
  if message.get("subtype") != "bot_message":
    url = "GROUP_EVENT_ZAP_URL"
    post_to_zap = requests.post(url, data=message)
    print(post_to_zap.content)

# Create an event listener for "channel_created" events
@slack_events_adapter.on("channel_created")
def zapier_zendesk_channel_create(event_data):
  event_details = event_data["event"]
  channel_info = event_details["channel"]
  print(json.dumps(event_details))
  url = "GROUP_EVENT_ZAP_URL"
  post_to_zap = requests.post(url, data=channel_info)
  print(post_to_zap.content)
  
# Start the server on port 3000
slack_events_adapter.start(host="0.0.0.0", port=5000)