from websocket import create_connection
import requests
import os
import json

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
usrid = os.environ.get('USRID')

url = "wss://profile.intra.42.fr/cable"
cookie = f"intra=v2; user.id={usrid}; locale=en"
header = {
	"Cookie": cookie
}
LocationChannel = {
	"command":"subscribe",
	"identifier":"{\"channel\":\"LocationChannel\",\"user_id\":155777}"
}

def sendToTelegran(msg):
	uids = [5223066980, 1361005823]
	apiURL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
	for uid in uids:
		r = requests.post(apiURL, json={'chat_id': uid ,'text': msg}, timeout=10)
	if r.status_code != 200:
		sendToTelegran(r.status_code)
		sendToTelegran(r.status_code)
		print(r.status_code)
		exit()

ws = create_connection(url, header=header)
ws.send(json.dumps(LocationChannel))
sendToTelegran("Launching...")
while True:
	try:
		result = ws.recv()
		formatted_result = json.loads(result)
		if "type" in formatted_result and formatted_result["type"] == "ping":
			continue
		if "message" in formatted_result and "location" in formatted_result["message"] and "campus_id" in formatted_result["message"]["location"]:
			if (formatted_result["message"]["location"]["campus_id"] == 16):
				if (formatted_result["message"]["location"]["host"].find("e3") != -1):
					if formatted_result["message"]["location"]["end_at"] == None:
						msg = "Spot no longer available: " + formatted_result["message"]["location"]["host"]
					else:
						msg = "New spot available: " + formatted_result["message"]["location"]["host"] + " since " + formatted_result["message"]["location"]["end_at"]
					sendToTelegran(msg)
					# msg = "Available since: " + formatted_result["message"]["location"]["end_at"] + " from " + formatted_result["message"]["location"]["login"]
					# sendToTelegran(msg)
	except Exception as e:
		print(e)
