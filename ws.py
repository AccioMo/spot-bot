from websocket import create_connection
import requests
import dotenv
import json

TELEGRAM_TOKEN = dotenv.get_key('.env', 'TELEGRAM_TOKEN')

url = "wss://profile.intra.42.fr/cable"
cookie = "intra=v2; user.id=MTU1Nzc3--a330df6d8483a177fae18bb1b6bdf945158e7d18; locale=en"
header = {
	"Cookie": cookie
}
LocationChannel = {
	"command":"subscribe",
	"identifier":"{\"channel\":\"LocationChannel\",\"user_id\":155777}"
}

def sendToTelegran(msg, chat_id):
	apiURL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
	r = requests.post(apiURL, json={'chat_id': chat_id ,'text': msg}, timeout=10)
	if r.status_code != 200:
		sendToTelegran(r.status_code, 5223066980)
		print(r.status_code)
		exit()

ws = create_connection(url, header=header)
ws.send(json.dumps(LocationChannel))
sendToTelegran("Launching...", 5223066980)
while True:
	try:
		result = ws.recv()
		formatted_result = json.loads(result)
		if "type" in formatted_result and formatted_result["type"] == "ping":
			continue
		if "message" in formatted_result and "location" in formatted_result["message"] and "campus_id" in formatted_result["message"]["location"]:
			if (formatted_result["message"]["location"]["campus_id"] == 16):
				# sendToTelegran(formatted_result["message"]["location"]["host"] + " changed in Khouribga campus", 5223066980)
				if (formatted_result["message"]["location"]["host"].find("e3") != -1):
					msg = "New spot in Khouribga campus: " + formatted_result["message"]["location"]["host"]
					sendToTelegran(msg, 5223066980)
					msg = "Available since: " + (formatted_result["message"]["location"]["end_at"] if formatted_result["message"]["location"]["end_at"] else "mn3rf") + " from " + formatted_result["message"]["location"]["login"]
					sendToTelegran(msg, 5223066980)
	except Exception as e:
		print(e)
# ws.close()