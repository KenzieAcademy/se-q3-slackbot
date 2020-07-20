#!/usr/bin/env python3
"""
Slackbot that uses Flask and Slack Events API under the hood
"""
import os
from flask import Flask
from slackeventsapi import SlackEventAdapter

__author__ = '???'

# Create Flask app & events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.environ['SLACK_SIGNING_SECRET'],
    "/slack/events",
    app
    )

# Add remainder of your Flask App code here
