import requests
import json
import os
from os.path import join

import curlify
import yaml



try:
	import credentials
	API_KEY = credentials.API_KEY
	IP = credentials.IP
except:
	IP = 'http://127.0.0.1'
	with open(join(os.environ['HOME'], '.octoprint', 'config.yaml'), 'r') as stream:
		confyaml = yaml.safe_load(stream)
		API_KEY = confyaml['api']['key']


requestHeaders = {
	"Content-Type": "application/json",
    "X-Api-Key": API_KEY,
}


def post_command(url, command):
	if not url.startswith('/'): url = '/'+url
	url = IP + url
	requestData = json.dumps({
		"command": command
	})
	reqres = requests.post(url, headers=requestHeaders, data=requestData)
	result = ["CURL command:", curlify.to_curl(reqres.request)]
	if reqres.status_code != 200:
		result.append(str(reqres.status_code))
		result.append(reqres.text)
	else:
		result.append(str(reqres.json()))
	return result


def main():
	res = post_command('/api/plugin/psucontrol', "getPSUState", )
	print('\n'.join(res))


if __name__ == '__main__':
	main()


