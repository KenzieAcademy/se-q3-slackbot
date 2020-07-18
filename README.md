# seq3-slackbot
In this project we are going to explore how to use Python and Flask to integrate with the popular Slack API.  We will create a barebones starter [Slack App](https://api.slack.com/start) that uses the [Flask](https://palletsprojects.com/p/flask/) microframework.    Although the final application itself will be a simple message-echo, there is work behind the scenes to get things up and running.

## Objectives
- Learn how to read and understand API documenation
- Research topics on your own with Google-fu, Stack Overflow, Reddit
- Set up a private network tunnel
- Introduction to [Flask Web Application Framework](https://palletsprojects.com/p/flask/)
- Creating scoped tokens, Managing Secret Keys
- Understand webhooks
- Async vs Synchronous event processing

## Goals
At the end of this project, you should be able to demo a minimal slackbot that will reply only to messages directed at it, in the same Slack channel.  The reply message will simply echo the sender's message.  You may elect to extend your slackbot in creative ways that you can also demo.

## Setup Part 1: Virtual Environment
This project comes with a virtual environment recipe file named `requirements.txt`.  A good practice is to create the virtual environment as a separate local folder named `.venv` at the root of your project.  If you do this from within the VSCode integrated terminal, VSCode will immediately detect the new environment and ask to activate it as your workspace environment (say yes).  Please refer to your notes on how to set up a virtual environment using a utility like `venv` or `pipenv` or `poetry`.

## Setup Part 2: Minimal Flask Server
The Slack APIs (Events and WebClient) are designed around the concept of [webhooks](https://codeburst.io/what-are-webhooks-b04ec2bf9ca2).  Webhooks are the method that Slack uses to send events to your Slackbot App.  In order to receive these events, it is necessary to run a web server as part of your Slackbot.  Using [Flask](https://palletsprojects.com/p/flask/) is a super-easy way to implement these webhook endpoints and connect them to your Slackbot.

Using the [quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/) code as your guide, create a local file named `hello.py` and copy the code into it.  Run the Flask server as directed in the quickstart, and verify that you can reach the app root from your Chrome browser.  This file is used for experimenting with Flask only; it won't be part of your Slackbot app.

Make sure you finish the Flask quickstart lesson so that you become familiar with this important component of your Slackbot.  Flask contains it's own built-in web application server called [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/) to streamline development.  Werkzeug has its own internal debugger which is enabled by setting the `FLASK_ENV` variable from 'production' to 'development'. You should see a message like this when Flask is up and running:
```console
$ FLASK_APP=hello flask run
 * Serving Flask app "hello"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 ```


## Setup Part 3: Create Slack Account + App
- Create a new member account on one of these Slack workspaces.  Request `admin` privilege from the owner or another admin once you become a member.
    - [KenzieBot](https://join.slack.com/t/kenziebot/shared_invite/zt-6d43wfx3-tJ37Y2ff3ipl5~dZ_tq5AA)
    - [KenzieBot2](https://join.slack.com/t/kenziebot2/shared_invite/zt-6ccr4b5t-19RyiWDmI0zhH849hiagbw)
- Request `admin` permission from the Slack Team owner, or other admin.

- create a new Slack App on [api.slack.com](api.slack.com).  When the app is created, copy the secrets into your .env file:
    - SLACK_CLIENT_ID=<your slack client_id>
    - SLACK_CLIENT_SECRET=<your slack client_secret>
    - SLACK_SIGNING_SECRET=<your slack signing_secret>
- See the [tutorial](https://github.com/slackapi/python-slackclient/blob/master/tutorial/01-creating-the-slack-app.md#create-a-slack-app
- https://1d1bd80f4733.ngrok.io/slack/events
)
- To manage all your user-created slack apps, visit https://api.slack.com/apps
- No OAuth scopes for USER Token are needed.
- Add the following OAuth scopes to your BOT Token:
    - `app_mentions:read` (get event when someone mentions our app)
    - `chat:write` (post messages in channels)
    - `im:write` (post messages in DMs)
    - `im:history` (receive DMs)
    - `reactions:read` (get events when someone reacts)

You do not need to add a 'Redirect URL'.  After desired scopes are selected, then click **Install App to Workspace**!  You will receive a `Bot User OAuth Access Token` which you should copy and store as a key/value pair in local `.env` file like this:
>`BOT_TOKEN=<your bot_token>`

DO NOT put this token in your source code, or push it to github in any way.  That is called a `Token Leak` and you will get a warning from github.  They scan user repos for leaked tokens.

## Setup Part 4: Ngrok Tunnel
- create ngrok account
- Download the zip file using `wget` and unzip it
- Move ngrok binary to `/usr/local/bin`
- Initialize with user key from ngrok dashboard

## Setup Part 5: Enable Events
- Enable [Event Subscriptions](https://api.slack.com/events-api#subscriptions) for you Bot.  This will require URL verification (which is why you installed ngrok)
- Run the minimal flask app in terminal 1 `python app.py` - defaults to port 3000
- Run `ngrok` in second terminal `ngrok http 3000`.


# References
- [Python SlackClient tutorial](https://github.com/slackapi/python-slackclient/tree/master/tutorial)
- [Slack Events API with Python](https://github.com/slackapi/python-slack-events-api#slack-events-api-adapter-for-python)
- [Events to choose from](https://api.slack.com/events-api#subscriptions)