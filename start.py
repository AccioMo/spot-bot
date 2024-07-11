import requests
import dotenv
import json
import time
import datetime

spots = [
	"e3r1p1",
	"e3r1p2",
	"e3r1p3",
	"e3r1p4",
	"e3r1p5",
	"e3r1p6",
	"e3r1p7",
	"e3r1p8",
	"e3r1p9",
	"e3r1p10",
	"e3r1p11",
	"e3r1p12",
	"e3r1p13",
	"e3r1p14",
	"e3r1p15",
	"e3r1p16",
	"e3r1p17",
	"e3r1p18",
	"e3r2p1",
	"e3r2p2",
	"e3r2p3",
	"e3r2p4",
	"e3r2p5",
	"e3r2p6",
	"e3r2p7",
	"e3r2p8",
	"e3r2p9",
	"e3r2p10",
	"e3r2p11",
	"e3r2p12",
	"e3r2p13",
	"e3r2p14",
	"e3r2p15",
	"e3r2p16",
	"e3r2p17",
	"e3r2p18",
	"e3r3p1",
	"e3r3p2",
	"e3r3p3",
	"e3r3p4",
	"e3r3p5",
	"e3r3p6",
	"e3r3p7",
	"e3r3p8",
	"e3r3p9",
	"e3r3p10",
	"e3r3p11",
	"e3r3p12",
	"e3r3p13",
	"e3r3p14",
	"e3r3p15",
	"e3r3p16",
	"e3r3p17",
	"e3r3p18",
	"e3r4p1",
	"e3r4p2",
	"e3r4p3",
	"e3r4p4",
	"e3r4p5",
	"e3r4p6",
	"e3r4p7",
	"e3r4p8",
	"e3r4p9",
	"e3r4p10",
	"e3r4p11",
	"e3r4p12",
	"e3r4p13",
	"e3r4p14",
	"e3r4p15",
	"e3r4p16",
	"e3r5p1",
	"e3r5p2",
	"e3r5p3",
	"e3r5p4",
	"e3r5p5",
	"e3r5p6",
	"e3r5p7",
	"e3r5p8",
	"e3r6p1",
	"e3r6p2",
	"e3r6p3",
	"e3r6p4",
	"e3r6p5",
	"e3r6p6",
	"e3r6p7",
	"e3r6p8",
	"e3r7p2",
	"e3r7p3",
	"e3r7p4",
	"e3r7p5",
	"e3r7p6",
	"e3r7p7",
	"e3r7p8",
	"e3r7p9",
	"e3r7p10",
	"e3r7p11",
	"e3r7p12",
	"e3r7p13",
	"e3r7p14",
	"e3r7p15",
	"e3r7p16",
	"e3r7p17",
	"e3r7p18",
	"e3r8p1",
	"e3r8p2",
	"e3r8p3",
	"e3r8p4",
	"e3r8p5",
	"e3r8p7",
	"e3r8p8",
	"e3r8p9",
	"e3r8p10",
	"e3r8p11",
	"e3r8p12",
	"e3r8p13",
	"e3r8p14",
	"e3r8p15",
	"e3r8p16",
	"e3r8p17",
	"e3r8p18",
	"e3r9p1",
	"e3r9p2",
	"e3r9p3",
	"e3r9p4",
	"e3r9p5",
	"e3r9p6",
	"e3r9p7",
	"e3r9p8",
	"e3r9p9",
	"e3r9p10",
	"e3r9p11",
	"e3r9p12",
	"e3r9p13",
	"e3r9p14",
	"e3r9p15",
	"e3r9p16",
	"e3r9p17",
	"e3r9p18",
	"e3r10p1",
	"e3r10p2",
	"e3r10p3",
	"e3r10p4",
	"e3r10p5",
	"e3r10p6",
	"e3r10p7",
	"e3r10p8",
	"e3r10p9",
	"e3r10p10",
	"e3r10p11",
	"e3r10p12",
	"e3r10p13",
	"e3r10p14",
	"e3r10p15",
	"e3r10p16",
	"e3r10p17",
	"e3r10p18",
	"e3r11p1",
	"e3r11p2",
	"e3r11p3",
	"e3r11p4",
	"e3r11p5",
	"e3r11p6",
	"e3r11p7",
	"e3r11p8",
	"e3r11p9",
	"e3r11p10"
]

CLIENT_ID = dotenv.get_key('.env', 'CLIENT_ID')
CLIENT_SECRET = dotenv.get_key('.env', 'CLIENT_SECRET')

def get_access_token():
	response = requests.post('https://api.intra.42.fr/oauth/token', {
	'grant_type': 'client_credentials',
	'client_id': CLIENT_ID,
	'client_secret': CLIENT_SECRET,
	})
	response.raise_for_status()
	return response.json()['access_token']

def get_cluster_data(access_token, params):
	headers = {
	'Authorization': f'Bearer {access_token}',
	}
	response = requests.get(f'https://api.intra.42.fr/v2/campus/16/locations?{params}&page[size]=1', headers=headers)
	if (response.status_code == 200):
		return response.json()
	elif (response.status_code == 429):
		print("Slow the fuck down...")
	else:
		print(f"Error {response.status_code} at {params}.")
		return (None)


def main():
	all_data = []
	free_spots = []
	access_token = get_access_token()
	for i, spot in enumerate(spots):
		cluster_data = get_cluster_data(access_token, f"filter[host]={spot}")
		if cluster_data:
			if cluster_data[0]["end_at"]:
				free_spots.append(cluster_data[0])
				end_at = datetime.datetime.strptime(cluster_data[0]["end_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
				print("Free post at", cluster_data[0]["host"], "since", end_at)
				if end_at.day - datetime.datetime.now().day:
					print("Likely not working.")
			all_data.append(cluster_data[0])
		print(f"{i / len(spots) * 100:.2f}%", end="\r")
		time.sleep(0.5)
	print("\nWriting to file...")
	with open("e3.json", "w") as w:
		json.dump(all_data, w)
	with open("file.json", "w") as w:
		json.dump(free_spots, w)
	print("Done!")

if __name__ == '__main__':
	main()
	# p = get_cluster_data(get_access_token(), "filter[host]=e3r1p1")
	# print(p)