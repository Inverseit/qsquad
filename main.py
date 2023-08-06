"""
This is a simple project to run your bot on Telegram and receive requests for new events via webhook on your server
To be very practical, I am using the / lib flask module to create this project!
Where you just need to declare your bot's token and the code itself will import other things, like your host, Instructions:
- Declare your bot's token here;
- Run the script on your server;
- Access your host + webhookstart (example: https://mysite.com/webhookstart)
Note: If you don't have a public IP (host), like me, you can use ngrok (https://ngrok.com/download), just follow the guidelines below:
First, you must run it with the following command: ngrok http 8443;
Second, tell this code your bot's token;
Third, you will have to open the link created with https + webhookstart (example: https://aj21h3.ngrok.io/webhookstart)
The code is ready to receive new telegram requests from your bot
"""

import flask, requests, json
app = flask.Flask(__name__)
Token = '6599294503:AAHUctduTg5aukgVdTvVhoAquBq0XNTWS2g' # Define your bot's token
@app.errorhandler(404)
def server_error(errorhandler):
	"""
	If a 404 error occurs, the function below will be executed, 
	where we will return the status 200 to eliminate the request!
	Because? the webhook creates a type of loop, where it always repeats the request until it is treated as status 200, 
	that is, it only ends the loop when it receives a successful message that, by default, it has status 200, 
	basically this will solve the problem !
	"""
	return flask.Response(status=200)

@app.before_request
def handler():
	if (flask.request.method == 'GET') and (flask.request.path == "/webhookstart"): 
		"""
		From here, it will only be read if the request method is "GET" and if the path is equal to "/ webhookstart", 
		if these variables are true, this script will execute a functionality in the telegram API that will make your
		host is set as the default to receive new events from your bot, that is, all new requests will be sent only to 
		the host detectable by the "flask"
		"""
		BOT = dict(
			URL = f'https://api.telegram.org/bot{Token}/setWebhook',
			paramst = {
				"url": f"{flask.request.host}/webhook",
				'max_connections': 1,
				"allowed_updates": ["message"]
			})
		r = requests.get(BOT['URL'],params=BOT['paramst']).json()
		return Response(response=r['description'], status=200)

	if (flask.request.method == 'POST') and (flask.request.path == "/webhook"):
		"""From here, it will only be read if the request method is "POST" and if the path is equal to "/ webhook", 
		if these variables are true, the script will read the event and always respond with the word: PONG
		I am using this word just to know that the script is working, you can create new returns or commands,
		from this logic that I am using.
		"""
		msg = flask.request.get_json(silent=True, force=True)
		params = dict(
			method = "sendMessage", 
			text = "pong",
			chat_id = msg['message']['chat']['id']
			)
		return flask.Response(status=200, headers={"Content-Type": "application/json"}, response=json.dumps(params))
if __name__ == '__main__':
  app.run(debug=True, port=443, host='127.0.0.1') #Running app