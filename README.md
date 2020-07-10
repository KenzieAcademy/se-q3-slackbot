# seq3-slackbot

# Ngrok setup
- create ngrok account
- Download the zip file and unzip
- Move ngrok binary to /usr/local/bin
- Initialize with user key from ngrok dashboard

# Slack App Setup
- create a new Slack App on [api.slack.com](api.slack.com). You will need admin permission.  When the app is created, copy the secrets into your .env file:
    - SLACK_CLIENT_ID="421405103765.1232796640579"
    - SLACK_CLIENT_SECRET="388d4e362d02e975f0df89f52ef0e1eb"
    - SLACK_SIGNING_SECRET="373450f886319700990e7c40711bfa36"
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
>`BOT_TOKEN="xoxb-421405203735-1256443538144-MqrEC6h0ZXpkUJWSwoA5JHZ1"`

DO NOT put this token in your source code, or push it to github in any way.  That is called a `Token Leak` and you will get a warning from github.  They scan user repos for leaked tokens.

- Enable [Event Subscriptions](https://api.slack.com/events-api#subscriptions) for you Bot.  This will require URL verification (which is why you installed ngrok)
- Run the minimal flask app in terminal 1 `python app.py` - defaults to port 3000
- Run `ngrok` in second terminal `ngrok http 3000`.


# Set up environment:
- pipenv install --python python3.8 flask flake8 slackclient slackeventsapi


# References
- https://github.com/slackapi/python-slackclient/tree/master/tutorial
- https://github.com/slackapi/python-slack-events-api#slack-events-api-adapter-for-python
- [Events to choose from](https://api.slack.com/events-api#subscriptions)