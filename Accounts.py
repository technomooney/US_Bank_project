import requests

apiKey = 'GaS6ZkPffGZOxGZBAThMjnt9yyn9dZ28'
baseUrl = 'https://alpha-api.usbank.com/innovations/v1'
header = {'apiKey': apiKey}

url = 'https://alpha-api.usbank.com/innovations/v1/users'
response = requests.get(url, headers=header).json()['UserList']
listOfLPIs = []
for item in response:
    listOfLPIs.append(item['LegalParticipantIdentifier'])


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
            print(name)
        except KeyError:
            name = 'Unknown Name ' + str(LPIList.index(LPI) + 1)
        namesAndIdentifiers[name] = LPI

    return namesAndIdentifiers


getNamesandIdentifiers(listOfLPIs, baseUrl, header)


