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
        except KeyError:
            name = 'Unknown Name ' + str(LPIList.index(LPI) + 1)
        namesAndIdentifiers[name] = LPI

    return namesAndIdentifiers


namesAndIdentifiers = getNamesandIdentifiers(listOfLPIs, baseUrl, header)


# Returns a dictionary Ex. {NameOfCustomer: [ListOfCheckingAccounts]}
def getAllChecking(namesAndIdentifiers, baseUrl, header):
    for user in namesAndIdentifiers.keys():
        params = {'LegalParticipantIdentifier': namesAndIdentifiers[user]}
        url = baseUrl + '/user/accounts'
        accountDetailsList = requests.post(url, data=params, headers=header).json()['AccessibleAccountDetailList']
        print(user)
        for details in accountDetailsList:
            redactedAccountNumber = details['BasicAccountDetail']['RedactedAccountNumber']
            categoryDescription = details['BasicAccountDetail']['Codes']['CategoryDescription']
            if categoryDescription == 'CHECKING':
                print(categoryDescription + ': ' + redactedAccountNumber)
        print()


getAllChecking(namesAndIdentifiers, baseUrl, header)


dict = {'Status': {'StatusCode': '0', 'Severity': 'Info', 'StatusDescription': 'Success'}, 'AccessibleAccountDetailList': [{'_id': '5d9434b7d0d221896f62d052', 'OperatingCompanyIdentifier': '642', 'ProductCode': 'BCD', 'PrimaryIdentifier': '00000004718240071486366', 'LegalParticipantIdentifier': '913996201744144603', 'BasicAccountDetail': {'BranchIdentifier': '907', 'RedactedAccountNumber': '*******471824******6366', 'Codes': {'CategoryCode': 'CCRD', 'CategoryDescription': 'CR CARD', 'RelationshipCode': 'INO', 'SubProductCode': 'AO', 'AccountStatusCode': '99', 'StatusDescription': 'OPEN'}, 'Balances': {'CurrentBalanceAmount': '0.0', 'AvailableBalanceAmount': '49945.0', 'PayoffBalanceAmount': '0.0', 'CreditAvailableBalanceAmount': '0.0', 'InvestmentBalanceAmount': '0.0', 'AccessibleBalanceAmount': '0.0'}}}, {'_id': '5d943ce2d0d221896f639954', 'OperatingCompanyIdentifier': '52', 'ProductCode': 'CCD', 'PrimaryIdentifier': '00000004037670240271147', 'LegalParticipantIdentifier': '913996201744144603', 'BasicAccountDetail': {'BranchIdentifier': '907', 'RedactedAccountNumber': '*******403767******1147', 'Codes': {'CategoryCode': 'CCRD', 'CategoryDescription': 'CR CARD', 'RelationshipCode': 'IND', 'SubProductCode': 'D7', 'AccountStatusCode': '99', 'StatusDescription': 'OPEN'}, 'Balances': {'CurrentBalanceAmount': '4592.28', 'AvailableBalanceAmount': '0.0', 'PayoffBalanceAmount': '4592.28', 'CreditAvailableBalanceAmount': '0.0', 'InvestmentBalanceAmount': '0.0', 'AccessibleBalanceAmount': '0.0'}, 'Entitlement': {'ViewBalanceEntitlementSwitch': 'true', 'ViewTransactionEntitlementSwitch': 'true', 'WithdrawFundsEntitlementSwitch': 'true', 'DepositFundsEntitlementSwitch': 'true', 'MaintainAccountEntitlementSwitch': 'true', 'TransactOrTradeEntitlementSwitch': 'true'}}}, {'_id': '5d95e131d0d221896f8e62f0', 'OperatingCompanyIdentifier': '300', 'ProductCode': 'CCD', 'PrimaryIdentifier': '00000000000104778493791', 'LegalParticipantIdentifier': '913996201744144603', 'BasicAccountDetail': {'BranchIdentifier': '262', 'RedactedAccountNumber': '*******000010******3791', 'Codes': {'CategoryCode': 'CHCK', 'CategoryDescription': 'CHECKING', 'RelationshipCode': 'JOO', 'SubProductCode': 'MN', 'AccountStatusCode': '03', 'StatusDescription': 'INACTIVE'}, 'Balances': {'CurrentBalanceAmount': '5304.74', 'AvailableBalanceAmount': '5304.74', 'PayoffBalanceAmount': '0.0', 'CreditAvailableBalanceAmount': '0.0', 'InvestmentBalanceAmount': '0.0', 'AccessibleBalanceAmount': '5304.74'}}}, {'_id': '5d96074bd0d221896f929544', 'OperatingCompanyIdentifier': '448', 'ProductCode': 'DDA', 'PrimaryIdentifier': '00000000000151701798143', 'LegalParticipantIdentifier': '913996201744144603', 'BasicAccountDetail': {'BranchIdentifier': '262', 'RedactedAccountNumber': '*******000015******8143', 'Codes': {'CategoryCode': 'CHCK', 'CategoryDescription': 'CHECKING', 'RelationshipCode': 'IND', 'SubProductCode': 'GS', 'AccountStatusCode': '99', 'StatusDescription': 'OPEN'}, 'Balances': {'CurrentBalanceAmount': '126821.76', 'AvailableBalanceAmount': '126821.76', 'PayoffBalanceAmount': '0.0', 'CreditAvailableBalanceAmount': '0.0', 'InvestmentBalanceAmount': '0.0', 'AccessibleBalanceAmount': '134921.77'}}}, {'_id': '5d96088fd0d221896f92ba97', 'OperatingCompanyIdentifier': '52', 'ProductCode': 'EXL', 'PrimaryIdentifier': '00000004037670174120740', 'LegalParticipantIdentifier': '913996201744144603', 'BasicAccountDetail': {'BranchIdentifier': '907', 'RedactedAccountNumber': '*******403767******0740', 'Codes': {'CategoryCode': 'CLNE', 'CategoryDescription': 'CR LINE', 'RelationshipCode': 'IND', 'SubProductCode': 'PL', 'AccountStatusCode': '99', 'StatusDescription': 'OPEN'}, 'Balances': {'CurrentBalanceAmount': '-0.01', 'AvailableBalanceAmount': '7100.01', 'PayoffBalanceAmount': '-0.01', 'CreditAvailableBalanceAmount': '7100.01', 'InvestmentBalanceAmount': '0.0', 'AccessibleBalanceAmount': '0.0'}}}, {'_id': '5d9608a5d0d221896f92bcce', 'OperatingCompanyIdentifier': '454', 'ProductCode': 'INV', 'PrimaryIdentifier': '00000000000000025353723', 'LegalParticipantIdentifier': '913996201744144603', 'BasicAccountDetail': {'BranchIdentifier': '9406', 'RedactedAccountNumber': '*******000000******3723', 'Codes': {'CategoryCode': 'OTHR', 'CategoryDescription': 'SUNDRY ACC', 'RelationshipCode': 'IND', 'SubProductCode': 'NR', 'AccountStatusCode': '99', 'StatusDescription': 'OPEN'}, 'Balances': {'CurrentBalanceAmount': '0.0', 'AvailableBalanceAmount': '0.0', 'PayoffBalanceAmount': '0.0', 'CreditAvailableBalanceAmount': '0.0', 'InvestmentBalanceAmount': '0.0', 'AccessibleBalanceAmount': '0.0'}}}, {'_id': '5d961c95d0d221896f94eb4a', 'OperatingCompanyIdentifier': '448', 'ProductCode': 'LOC', 'PrimaryIdentifier': '00000000000151701798143', 'LegalParticipantIdentifier': '913996201744144603', 'BasicAccountDetail': {'BranchIdentifier': '2601', 'RedactedAccountNumber': '*******000015******8143', 'Codes': {'CategoryCode': 'CLNE', 'CategoryDescription': 'CR LINE', 'RelationshipCode': 'IND', 'SubProductCode': 'PL', 'AccountStatusCode': '99', 'StatusDescription': 'OPEN'}, 'Balances': {'CurrentBalanceAmount': '0.0', 'AvailableBalanceAmount': '1000.0', 'PayoffBalanceAmount': '0.0', 'CreditAvailableBalanceAmount': '0.0', 'InvestmentBalanceAmount': '0.0', 'AccessibleBalanceAmount': '0.0'}}}]}
