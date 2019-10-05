import requests

apiKey = 'GaS6ZkPffGZOxGZBAThMjnt9yyn9dZ28'
header = {'apiKey': apiKey}
base = 'https://alpha-api.usbank.com/innovation-rate/v1'


def getAutoLoanRates(url, key):

    ratesURL = url + '/HeartBeat?output=json'
    response = requests.get(ratesURL, headers=key).json()
    print(response)


getAutoLoanRates(base, header)

