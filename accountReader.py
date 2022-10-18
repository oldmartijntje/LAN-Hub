import accounts_omac

configSettings = accounts_omac.configFileTkinter()
data = accounts_omac.defaultConfigurations.defaultLoadingTkinter(configSettings)
if data == False:
  exit()

splitString = '//CUT//'

response = ''

path = ''

def getThis():
  pass



while True:
  data = accounts_omac.saveAccount(data, configSettings)