"""
Slackbot that uses Flask and Slack Events API under the hood
Defaults to port 3000

When restarting the ngrok tunnel, remember to update this app's
Events Subscription URL over at at https://api.slack.com/apps:
Copy your ngrok tunnel URL, append the string `/slack/events`
e.g. https://f3f53b394217.ngrok.io/slack/events
"""

import os
import json

from flask import Flask, request
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv

__author__ = 'madarp'


# load up secrets from my `.env` file
load_dotenv()

# Create Flask app & events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.environ['SLACK_SIGNING_SECRET'],
    "/slack/events",
    app
    )

# Initialize a Web API client
slack_web_client = WebClient(
    token=os.environ['SLACK_BOT_TOKEN']
    )


# Uncomment to log body of incoming requests
@app.before_request
def log_request():
    app.logger.debug("Request JSON:\n %s", json.dumps(request.json, indent=4))


# Flask root page
@app.route("/")
def hello():
    return "You have found the homepage of Flasky Test"


# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    app.logger.info(emoji)


@slack_events_adapter.on("message")
def message_home(payload):
    """Respond with an echo"""
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    bot_id = event.get("bot_id")
    app.logger.info(f"Received message.app_home:{text}")

    # Beware of looping: don't respond to a bot_msg (including myself!)
    if bot_id:
        app.logger.info(f"Discarded message.app_home from bot_id:{bot_id}")
    else:
        app.logger.info("Replying to message")
        slack_web_client.chat_postMessage(
            channel=channel_id,
            text=f"Received via message.app_home from {user_id}: {text}",
            )


@slack_events_adapter.on("app_mention")
def app_mention(payload):
    """Someone mentioned this app in a message"""
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if text:
        slack_web_client.chat_postMessage(
            channel=channel_id,
            text=f"Received via app_mention from {user_id}: {text}",
            )


if __name__ == "__main__":
    # gets port num from environment variable
    app.run(port=os.environ['FLASK_RUN_PORT'])
