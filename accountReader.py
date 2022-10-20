import accounts_omac

configSettings = accounts_omac.configFileTkinter()
data = accounts_omac.defaultConfigurations.defaultLoadingTkinter(configSettings)
if data == False:
  exit()

response = ''

# data request and response
packet = {'KEY':'69','request':['meep','meep1','kaas'],'meep':{"path":['achievements','UNO2byMarjinIDK','oopsie Woopsie','message']}, 'meep1':{"path":['achievements','UNO2byMarjinIDK','oopsie Woopsie','title']}, 'kaas':{"path":['name']}}
receipt = {'KEY':'69', 'request':['meep','meep1','kaas'], 'meep': {'response': '200', 'data': 'OOPSIE WOOPSIE!!\nUwU We made a fucky wucky!!'}, 'meep1': {'response': '404'}, 'meep1': {'response': '401'}}

# server: give key when key used


# backgroundcheck request and response

def getThis():
  pass



while True:
  data = accounts_omac.saveAccount(data, configSettings)