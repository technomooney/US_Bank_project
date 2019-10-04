import requests
import sys
import os


def main():
    url_dict = {
    'autoloan_url':'https://alpha-api.usbank.com/innovation-rate/v1/GetAutoLoanRates?application=RIB&output=json&branchnumber=1&zipcode=80130&regionid=1&loanamount=24000&loantermmonths=12&loanproduct=NEW',
    'atm_url':'https://alpha-api.usbank.com/innovation-locations/v1/StringQuery?application=parasoft&transactionid=afae903d-8946-4f88-a958-4bdbcf0bed6f&output=json&searchtype=A&stringquery=55403&branchfeatures=BOP'
    }
    # apiKey = os.environ['USBANK_APIKEY']  # TODO set this environment variable in PyCharm or for your OS
    header = {'apiKey': os.environ['USBANK_APIKEY']}
    base_url = 'https://alpha-api.usbank.com/innovations/v1/'
    if sys.argv[1] == 'users':
        users_list = get_user_list(base_url,header)
    # users_list=get_user_list(base_url,header)
    atm_list = get_atm_list(url_dict,header)
    print(users_list)
    arg1=sys.argv[1]
    print(arg1)

def get_atm_list(url_dict,header):
    response = requests.get(url_dict['atm_url'], headers=header).json()
    reply = response['GetListATMorBranchReply']
    atmList = reply['ATMList']  # Todo extract specific location data needed
    return atmList

def get_auto_rate(url_dict,header):
    rateResponse = requests.get(url_dict['autoloan_url'], headers=header).json()
    rate = rateResponse['AutoLoanRates']['RateTier']['Rate']
    return rate

def get_user_list(base_url,header):
    users_url = base_url + 'users'
    ids = requests.get(users_url, headers=header).json()
    users=ids['UserList']
    users_list = []
    for item in users:
        users_list.append(item[])
    file = open('user_list.txt',"w")
    file.write(str(users))
    file.close()
    return users


main()