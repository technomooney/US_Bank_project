import requests
import os

apiKey = os.environ['USBANK_APIKEY']   # TODO set this environment variable in PyCharm or for your OS
print(apiKey)

# Example fetching data from ATM location API

url = 'https://alpha-api.usbank.com/innovation-locations/v1/StringQuery?application=parasoft&transactionid=afae903d-8946-4f88-a958-4bdbcf0bed6f&output=json&searchtype=A&stringquery=55403&branchfeatures=BOP'

header = {'apiKey': apiKey}
response = requests.get(url, headers=header).json()
#
# reply = response['GetListATMorBranchReply']
# atmList = reply['ATMList']  # Todo extract specific location data needed
#
# for atm in atmList:
#     print(atm)

# Example fetching data from Loan Rates API

autoloan = 'https://alpha-api.usbank.com/innovation-rate/v1/GetAutoLoanRates?application=RIB&output=json&branchnumber=1&zipcode=80130&regionid=1&loanamount=24000&loantermmonths=12&loanproduct=NEW'
header = {'apiKey': apiKey}

rateResponse = requests.get(autoloan, headers=header).json()
rate = rateResponse['AutoLoanRates']['RateTier']['Rate']
print('The rate is ', rate)


## How to get data from accounts and users?????

# users_url = 'https://alpha-api.usbank.com/innovation/v1/user/accounts'
# users_url = 'https://jcm-bank-43157.appspot.com/v1/user/accounts'
# users_url = 'https://alpha-api.usbank.com/innovations/v1/user/accounts'
base_url = 'https://alpha-api.usbank.com/innovations/v1/'
# json_data=

users_url = base_url+'users'
ids = requests.get(users_url, headers=header).json()
# ids = requests.post(users_url,json=)
print(ids)

## TODOs for Users:
"""
Make sure server is up, figure out URL
Make GET request to get all users id    or all account int   -- these should have list of IDs for users or accounts

Make  POST request about specific user 
Make POST request about specific account   


response = requests.post(url, data= {"whatever":"whatever"} ).json()

Use a Python OAuth library if you need to authenticate with OAuth 

# Requests docs at https://requests.kennethreitz.org/en/master/user/quickstart/#make-a-request

"""

# Hypothetical OAuth request to server
# from requests_oauthlib import OAuth1Session
# usbank = OAuth1Session(apiKey,
#                             client_secret='todoreplace_with_real_secret',
#                        )
# r = usbank.get(accounts_url)
# print(r.text)
# url = 'https://alpha-api.usbank.com/innovation/v1/user/accounts'
# url = 'https://jcm-bank-43157.appspot.com/innovation/v1/user/accounts'
identify = '000995928731567433'
data = {'LegalParticipantIdentifier': {identify}}  # find this out from query to /users endpoint
account_info = requests.post(base_url+'user/accounts', headers=header, data=data).json()
print(account_info)





