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
    base_url = 'https://alpha-api.usbank.com/innovations/v1'
    if sys.argv[1]:
        if sys.argv[1] == 'names':
            users_list = get_user_list(base_url,header)
            namesDict= getNamesandIdentifiers(users_list,base_url,header)
            save('namesDict',namesDict)
        elif sys.argv[1] == 'accounts':
            users_list = get_user_list(base_url,header)
            account_info_dict = get_accounts(base_url,users_list,header)
            save('account_dict',account_info_dict)
    # users_list = get_user_list(base_url,header)
    # namesDict= getNamesandIdentifiers(users_list,base_url,header)
    # # save('namesDict',namesDict)
    # users_list = get_user_list(base_url,header)
    # account_info_dict = get_accounts(base_url,users_list,header)
    # # save('account_dict',account_info_dict)
    # print(account_info_dict)


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
    users_url = base_url + '/users'
    ids = requests.get(users_url, headers=header).json()
    users=ids['UserList']
    users_list = []
    for item in users:
        users_list.append(item['LegalParticipantIdentifier'])
    return users_list


def getNamesandIdentifiers(LPIList, baseUrl, header):
    namesAndIdentifiers = {}
    for LPI in LPIList:
        allAccountsUrl = baseUrl + '/user/accounts'
        params = {'LegalParticipantIdentifier': LPI}
        AADL = requests.post(allAccountsUrl, data=params, headers=header).json()['AccessibleAccountDetailList']
        pi = AADL[0]['PrimaryIdentifier']
        pc = AADL[0]['ProductCode']
        oci = AADL[0]['OperatingCompanyIdentifier']
        data = {'PrimaryIdentifier': pi,
                'ProductCode': pc,
                'OperatingCompanyIdentifier': oci}
        accountDetailsUrl = baseUrl + '/account/details'
        accountDetails = requests.post(accountDetailsUrl, data=data, headers=header).json()
        detail = accountDetails['Account']['AccountDetail']
        try:
            name = detail['AddressAndTitle']['AccountTitle']
        except KeyError:
            name = 'Unknown Name ' + str(LPIList.index(LPI) + 1)
        namesAndIdentifiers[name] = LPI

    return namesAndIdentifiers


def save(file_name,data):
    file = open(file_name,'w')
    file.write(str(data))
    file.close()


def get_user_list_arg(base_url,header):
    users_url = base_url + 'users'
    ids = requests.get(users_url, headers=header).json()
    print(ids)
    users=ids['UserList']
    users_id_list = []
    for item in users:
        users_id_list.append(item['LegalParticipantIdentifier'])
    file = open('user_list.txt',"w")
    return users_id_list


def get_accounts(base_url,users_list,header):
    account_info_dict = {}
    for ident in users_list:
        data = {'LegalParticipantIdentifier': f'{ident}'}  # find this out from query to /users endpoint
        account_info = requests.post(base_url + '/user/accounts', headers=header, data=data).json()
        account_info_dict[ident] = account_info
    return account_info_dict


main()