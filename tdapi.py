"""

TD-Ameritrade API Connection
Option Chains

Josh Argraves
6/26/2019


"""

class tdapi:
    
    """
    Process Summary:
    1. Use splinter to launch a browser to retrieve authentication code
    2. Use authentication code to retrieve access token and refresh token
    3. Use access token to make requests
    4. Use refresh token to retrieve new access token

    """
    import datetime
    
    endpoint = r'https://api.tdameritrade.com/v1/oauth2/token'
    option_point = 'https://api.tdameritrade.com/v1/marketdata/chains'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
#------------------------------------------------------------------------------    
    def __init__(self, user, password, consumer_key, host, exec_path):
        self.user = user
        self.password = password
        self.consumer_key = consumer_key
        self.host = host
        self.client_id = self.consumer_key + "@AMER.OAUTHAP"
        self.exec_path = exec_path
#------------------------------------------------------------------------------    
    def authorization_code(self):
        
        from splinter import Browser
        import requests
        import urllib
        
        method = 'GET'
        url = 'https://auth.tdameritrade.com/auth?'
            
        payload = {
            'response_type': 'code',
            'redirect_uri': self.host,
            'client_id': self.client_id
            }

        executable_path = {'executable_path': self.exec_path}
        driver = Browser('chrome', **executable_path, headless = False)
        
        built_url = requests.Request(method, url, params = payload).prepare().url
    
        driver.visit(built_url)
        driver.find_by_id('username').first.fill(self.user)
        driver.find_by_id('password').first.fill(self.password)
        driver.find_by_id('accept').first.click()
        driver.find_by_id('accept').first.click()
    
        new_url = driver.url #authorization code is contained in the new url string 
        authorization = urllib.parse.unquote(new_url.split('code=')[1]) 
        driver.quit()
        
        return authorization    
#------------------------------------------------------------------------------
    def access_thru_refresh(self):
        
        import requests
                
        refresh_body = {'grant_type': 'refresh_token',
                        'refresh_token': self.refresh_token,
                        'client_id': self.client_id}  
  
        authReply = requests.post(tdapi.endpoint, headers = tdapi.headers, data = refresh_body)
        decoded_content = authReply.json()
        
        self.update_tokens(decoded_content)
        
        return    
#------------------------------------------------------------------------------
    def access_thru_auth(self):
        
        import requests
        
        auth_code = self.authorization_code()
        
        body = {'grant_type': 'authorization_code',
                'access_type': 'offline',
                'code': auth_code,
                'client_id': self.client_id,
                'redirect_uri': 'http://localhost/test'}

        authReply = requests.post(tdapi.endpoint, headers = tdapi.headers, data = body)
        decoded_content = authReply.json()
  
        
        self.update_tokens(decoded_content)
        self.refresh_token = decoded_content['refresh_token']
        
        return    
#------------------------------------------------------------------------------
    def update_tokens(self, content):
        
        import datetime
                
        self.access_token = content['access_token']        
        self.last_update = datetime.datetime.today()
        
        return
#------------------------------------------------------------------------------
    def retrieve_token(self):
        
        """
        Do you have a refresh token? (refresh token lasts 90 days)
        --> if yes: use it to get new access token
        --> if no: use long way to get authorization
        """
        
        if hasattr(self, 'refresh_token'):
            self.access_thru_refresh()
            return
        else:
            self.access_thru_auth()
            return
#------------------------------------------------------------------------------
    def option_chain(self, 
                     ticker,
                     fromDate = datetime.datetime.today().strftime('%Y-%m-%d'),
                     toDate = (datetime.datetime.today() + datetime.timedelta(days=365)).strftime('%Y-%m-%d'),
                     cp = 'ALL'):
        #If you enter just a ticker, default is all call and put option chains within the next 365 days
        
        import requests
        
        query = {'apikey': self.consumer_key,
                   'symbol': ticker,
                   'contractType': cp, # CALL, PUT, ALL
#                   'strikeCount': '5', # Number of Strikes above & below ATM price
#                   'includeQuotes': 'FALSE', # Include quotes in the option chain
#                   'strategy': 'SINGLE', # Single, Analytical, Covered, Strangle, Straddle, etc.
#                   'interval': None, #Strike interval for spread strategy chains
#                   'strike': None, #Specify strike price
#                   'range': 'ALL', #ITM, NTM, OTM, SAK, SBK, SNK, ALL (SAK = Strikes Above Market)
                   'fromDate': fromDate, # yyyy-mm-dd or yyyy-mm-dd'T'HH:mm:ssz
                   'toDate': toDate,
#                   'volatility': None,
#                   'underlyingPrice': None,
#                   'interestRate': None,
#                   'daysToExpiration': None,
#                   'expMonth': None,
#                   'optionType': 'ALL'
                   }
        
        self.retrieve_token()
        header = {'Authorization': 'Bearer {}'.format(self.access_token)}
        
        content = requests.get(url = tdapi.option_point, params = query, headers = header)
        data = content.json()    
        

        return data
    
    def option_unpack(self, data: dict, cpflag: int):
        
        import pandas as pd  
        import numpy as np

        if cpflag == 1:
            name = 'callExpDateMap'
        elif cpflag == 0:
            name = 'putExpDateMap'
        else:
            raise Exception('Enter a valid cpflag: 1 => Calls, 0 => Puts')
        
        df2 = pd.DataFrame()
        for key, value in data[name].items():
            df = pd.DataFrame()
            
            for strike in data[name][key].keys():
                
                temp = pd.DataFrame.from_dict([data[name][key][strike][0]])
                temp['Strike'] = float(strike)
                
                df = pd.concat([df, temp])
            
            df['Expiry'] = key
            df2 = pd.concat([df2, df])
        
        df2.index = np.arange(len(df2))    
        
        return df2
        
        
#------------------------------------------------------------------------------
#END---------------------------------------------------------------------------
#------------------------------------------------------------------------------