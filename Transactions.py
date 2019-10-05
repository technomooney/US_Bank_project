import requests
import math

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
        except KeyError:
            name = 'Unknown Name ' + str(LPIList.index(LPI) + 1)
        namesAndIdentifiers[name] = LPI

    return namesAndIdentifiers


namesAndIdentifiers = getNamesandIdentifiers(listOfLPIs, baseUrl, header)


# Returns a dictionary Ex. {NameOfCustomer: [ListOfCheckingAccounts]}
def getAllChecking(namesAndIdentifiers, baseUrl, header):
    custAndAccounts = {}
    for user in namesAndIdentifiers.keys():
        accounts = []
        params = {'LegalParticipantIdentifier': namesAndIdentifiers[user]}
        url = baseUrl + '/user/accounts'
        accountDetailsList = requests.post(url, data=params, headers=header).json()['AccessibleAccountDetailList']
        print(user)
        for details in accountDetailsList:
            redactedAccountNumber = details['BasicAccountDetail']['RedactedAccountNumber']
            categoryDescription = details['BasicAccountDetail']['Codes']['CategoryDescription']
            if categoryDescription == 'CHECKING':
                print(categoryDescription + ': ' + redactedAccountNumber)
                accounts.append(redactedAccountNumber)
        custAndAccounts[user] = accounts
    print(custAndAccounts)


getAllChecking(namesAndIdentifiers, baseUrl, header)


def getAllTransactions(LPIList, url, header):
    for LPI in LPIList:
        allAccountsUrl = url + '/user/accounts'
        params = {'LegalParticipantIdentifier': LPI}
        AADL = requests.post(allAccountsUrl, data=params, headers=header).json()['AccessibleAccountDetailList']
        for item in AADL:
            if item['ProductCode'] == 'CCD' or item['ProductCode'] == 'BCD':
                pi = item['PrimaryIdentifier']
                pc = item['ProductCode']
                oci = item['OperatingCompanyIdentifier']
                data = {'PrimaryIdentifier': pi,
                        'ProductCode': pc,
                        'OperatingCompanyIdentifier': oci}
                transactionsUrl = baseUrl + '/account/transactions'
                transactions = requests.post(transactionsUrl, data=data, headers=header).json()
                if transactions['Status']['StatusCode'] == '404':
                    print('No Transactions')
                else:

                    transactionList = transactions['TransactionList']
                    getAccountTransactions(transactionList)


def getAccountTransactions(transactions):
    dates = []
    individualPinches = []
    cumulativePinches = []
    descriptions = []
    for transaction in transactions:
        try:
            print(transaction)
            initial = float(transaction['PostedAmount'])
            rounded = math.ceil(initial)
            pinch = rounded - initial
            descriptions.append(transaction['TransactionDescription'])
            dates.append(transaction['PostedDate'])
            individualPinches.append(pinch)
            cumulativePinches.append(sum(individualPinches))
        except KeyError:
            continue
    for index in range(len(dates)):
        print('{0:<15}{1:<50}${2:<6.2f}${3:<10.2f}'.format(dates[index], descriptions[index], individualPinches[index], cumulativePinches[index]))
    return dates, individualPinches, cumulativePinches, descriptions


getAllTransactions(listOfLPIs, baseUrl, header)


# getAccountTransactions(transactions)


