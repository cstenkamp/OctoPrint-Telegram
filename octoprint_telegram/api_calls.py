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


def post_command(url, command, method='POST', requestData=None):
	if not url.startswith('/'): url = '/'+url
	url = IP + url
	if command and not requestData:
		requestData = json.dumps({
			"command": command
		})
	else:
		requestData = json.dumps(requestData)
	if method == 'GET':
		reqres = requests.get(url, headers=requestHeaders, data=requestData)
	else:
		reqres = requests.post(url, headers=requestHeaders, data=requestData)
	result = ["CURL command: "+str(curlify.to_curl(reqres.request))]
	print("CURL command:", curlify.to_curl(reqres.request))
	if reqres.status_code != 200:
		result.append('Return code: '+str(reqres.status_code))
		result.append(reqres.text)
	else:
		result.append(str(reqres.json()))
	return result


def main():
	res = post_command('/api/plugin/psucontrol', "getPSUState", )
	print('\n'.join(res))


def connect():
	res = post_command('api/plugin/psucontrol', 'turnPSUOn')
	re2 = post_command('/api/connection', "connect", )
	print('\n'.join(res))
	print('\n'.join(re2))

def cancel_print():
	res = post_command('api/job', 'cancel')  #https://community.octoprint.org/t/repeat-last-printjob-with-physical-push-button/5741/4
	print('\n'.join(res))


def repeat_print():
	res = post_command('api/job', 'start')  #https://community.octoprint.org/t/repeat-last-printjob-with-physical-push-button/5741/4
	print('\n'.join(res))


def preheat():
	res = post_command('api/printer/tool', command='', method='POST', requestData={"command": "target", "targets": {"tool0": 200}})
	re2 = post_command('api/printer/bed', command='', method='POST', requestData={"command": "target", "target": 60})
	print('\n'.join(res))
	print('\n'.join(re2))




if __name__ == '__main__':
	main()


