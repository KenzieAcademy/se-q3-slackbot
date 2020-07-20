<img height="120px" src="img/slack_api_200.png" />

# seq3-slackbot
### _Instructor-guided activity_
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

Make sure you finish the Flask quickstart lesson so that you become familiar with this important component of your Slackbot.  To streamline development, Flask contains it's own built-in web application server which is a component of the [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/) WSGI utilities library.  Werkzeug has its own internal debugger which is enabled by setting the `FLASK_ENV` variable from 'production' to 'development'. You should see a message like this when Flask is up and running:
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

- create a new Slack App on [api.slack.com](api.slack.com).  When the app is created, copy the secrets into your `.env` file:
    ```
    SLACK_CLIENT_ID=<your slack client_id>
    SLACK_CLIENT_SECRET=<your slack client_secret>
    SLACK_SIGNING_SECRET=<your slack signing_secret>
    ```
- See the [python-slackclient tutorial](https://github.com/slackapi/python-slackclient/blob/master/tutorial/01-creating-the-slack-app.md#create-a-slack-app)

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
- Create [ngrok](https://ngrok.com/) account
- From terminal window, download the zip file using `wget` and unzip it
- Move ngrok binary to `/usr/local/bin`
- Initialize with user key from ngrok dashboard

## Setup Part 5: Enable Events
- Enable [Event Subscriptions](https://api.slack.com/events-api#subscriptions) for you Bot.  This will require URL verification (which is why you installed ngrok)
- Run the minimal flask app in terminal 1 `python app.py` - defaults to port 3000
- Run `ngrok` in second terminal `ngrok http 3000`.

# Coding the App
Whew!  After all this setup, it's finally time to write some code for the App!   In the app, Flask will do the heavy lifting.  There are just a few functions to write, to do the work of receiving and responding to Slack events.

### Environment
Use the `load_dotenv` function to make sure all the secrets that you stored in the `.env` file are available in Python.  When .env is correctly loaded, you should be able to do this in your code without raising a KeyError exception:
```python
import os
token = os.environ['SLACK_BOT_TOKEN']
```

### Flask app, events adapter, and web client
 - Create a global (module scope) instance of a `Flask` application and name it `app`.  
 - Create a global instance of the `SlackEventAdapter` object which is found in the `slackeventsapi` library.  This library should already be installed into your virtual environment.  You will need to provide the **Slack Signing Secret**, a routing url for the incoming event stream, and the Flask app instance itself.  The SlackEventAdapter is used to receive the incoming event stream, and dispatch events to various handlers that you will create.
 - Create a global instance of the `WebClient` object which is found in the `slack` library (already installed). You will need to provide the **Bot Token**.  The WebClient is used to send outgoing messages to Slack.

### Root Path
Add a Flask route to handle the root path of your webservice, otherwise known as `/`  Write a function to handle the request, and use a standard Flask decorator to assign the route `/` to this handler function.  It's good to have a root path so you know your Flask app is up and running when you visit the URL for it.

### Event Handlers
 - Create an event handler function for the `message` event.  This event will be received through the Slack Events Adapter.  Use the events adapter decorator notation to bind your handler function to the adapter's event dispatcher.  Your app will receive the "message" event when someone is talking in its app_home space. 
 - Extract the text portion of the incoming message, as well as the user_id and channel_id.  Then send a message back to the same channel with the same text, and mention which user_id it came from e.g. `f"Received via message from {user_id}: {text}"`
 - WATCH OUT: It's easy to get into an infinite message loop here, because every time you post a message you will get another message event and you will post another reply and get another event and so on.  To prevent this, think of a way to detect NOT RESPOND to your own reply message! You will need to experiment with this.
 - Create another similar event handler function for the `app_mention` event.  Remember when you gave your app the `app_mentions:read` scope in Setup Part 3?  That enables this event.  This allows your app to respond to anyone who @-mentions your app by name in other channels or DMs.  Use the decorator notation again to bind this handler to the event dispatcher.  This event is a little easier, it should not require the echo suppression that the "message" event needs.

## Debugging
Remember that Flask has a built-in debugger which is served in a web page.  If your code raises an exception, you can view this by visiting the Flask root page.

The Flask app comes with a logger that you can use in your code, you don't have to setup your own logger
```python
app.logger.debug("This is a debug message")
app.logger.info("Here an INFO-level message")
```

To peek inside the data received from any incoming request, use this code snippet.  NOTE that you will only see this if you have the `FLASK_DEBUG` environment variable set to 1. 
```python
# Uncomment to log body of incoming requests when FLASK_DEBUG=1
@app.before_request
def log_request():
    app.logger.debug("Request JSON:\n %s", json.dumps(request.json, indent=4))
```

Here is a VSCode debugging configuration that you can copy-paste into your `launch.json` file
```json
{
    "name": "Slackbot Debug",
    "type": "python",
    "request": "launch",
    "module": "flask",
    "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "development",
        "FLASK_DEBUG": "1"
    },
    "args": [
        "run",
        "--no-debugger",
        "--no-reload",
        "--port", "3000"
    ],
    "jinja": true
}

```

## Async Event Handlers
We have implemented synchronous event handlers.  That means that when each handler's code is running, no other events will be handled.  OK for 1995-era web pages, but not anymore.  Users expect fast loading and fast responses to API queries.

Research project:  How would you implement Async handlers for these events?

## Conclusion
We hope you enjoyed this brief guided activity to explore Slack Apps.  Slack has a rich ecosystem of APIs, tutorials, design elements and code libraries specifically for app developers.  The APIs are well-documented.  You may even consider developing your own Slack App and marketing it in the Slack App Directory!

Here's a [case study](https://pawelurbanek.com/profitable-slack-bot-rails), in case you were wondering.

# References
- [Python SlackClient tutorial](https://github.com/slackapi/python-slackclient/tree/master/tutorial)
- [Slack Events API with Python](https://github.com/slackapi/python-slack-events-api#slack-events-api-adapter-for-python)
- [Events to choose from](https://api.slack.com/events-api#subscriptions)