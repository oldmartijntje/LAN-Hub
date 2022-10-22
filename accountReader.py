import accounts_omac

configSettings = accounts_omac.configFileTkinter()
data = accounts_omac.defaultConfigurations.defaultLoadingTkinter(configSettings)
if data == False:
  exit()

# data sent from someone through server and the expected result
# the S behind means that u receive it as server and not as client
packetS = {'for':'accountID', 'from': 'accountID', 'serverKEY':420,'message':{'KEY':69,'request':['meep','meep1','kaas'],'meep':{"path":['achievements','UNO2byMarjinIDK','oopsie Woopsie','message']}, 'meep1':{"path":['achievements','UNO2byMarjinIDK','oopsie Woopsie','title']}, 'kaas':{"path":['name']}}}
packet = {'from': 'accountID','message':{'KEY':69,'request':['meep','meep1','kaas'],'meep':{"path":['achievements','UNO2byMarjinIDK','oopsie Woopsie','message']}, 'meep1':{"path":['achievements','UNO2byMarjinIDK','oopsie Woopsie','title']}, 'kaas':{"path":['name']}}}
receiptS = {'for':'accountID', 'from': 'accountID', 'serverKEY':1234,'message':{'KEY':69, 'requested':['meep','meep1','kaas'], 'meep': {'response': '200', 'data': 'OOPSIE WOOPSIE!!\nUwU We made a fucky wucky!!'}, 'meep1': {'response': '404'}, 'meep1': {'response': '401'}}}
receipt = {'from': 'accountID', 'message':{'KEY':69,'requested':['meep','meep1','kaas'], 'meep': {'response': '200', 'data': 'OOPSIE WOOPSIE!!\nUwU We made a fucky wucky!!'}, 'meep1': {'response': '404'}, 'meep1': {'response': '401'}}}

# less program specific templates
# in the message directry you need to add whatever is you want to send.
packetS = {'for':'accountID', 'from': 'accountID', 'serverKEY':420,'message':{'KEY':69}}
packet = {'from': 'accountID','message':{'KEY':69}}
receiptS = {'for':'accountID', 'from': 'accountID', 'serverKEY':1234,'message':{'KEY':69}}
receipt = {'from': 'accountID', 'message':{'KEY':69}}

# server: give key when key used
# your account is saved to your socket and username once you ask for the first KEY
# if you ask for too many new KEYS it will blacklist you from asking for a while
# if someone apparently has the same account on different socket, disconnect them if the old socket is still active (socket.close())
#or the account will be sent at the start
request = {'from':'accountID', 'for':'server', 'message': 'keyRequest()'}
receipt = {'from':'server', 'for':'accountID', 'message': 'KEY'}

# backgroundcheck request and response

def getThis():
  pass



while True:
  data = accounts_omac.saveAccount(data, configSettings)