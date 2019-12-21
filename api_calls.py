import requests
import curlify
import json

import credentials


requestHeaders = {
	"Content-Type": "application/json",
    "X-Api-Key": credentials.API_KEY,
}


def post_command(url, command):
	if not url.startswith('/'): url = '/'+url
	url = credentials.IP+url
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


