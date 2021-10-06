#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import datetime
from urllib.parse import urlencode
import base64


# In[5]:


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    #acquire from spotify
    client_id = None
    client_secret = None
    user_id = None
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = None
        self.client_secret = None
        self.user_id = None
    def get_client_credentials(self):
        """
        return base 64 encoded string 
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_secret == None:
            raise Exception("You must enter client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode() 
    
    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"  
        }
        
    def get_token_data(self):
        return {
    "grant_type": "client_credentials"
        }
        
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        #make sure request has correct status code
        
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client")
            #return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] #seconds 
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        #check if token is expired
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now: 
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
        "Authorization": f"Bearer {access_token}"
        }
        return headers
    
    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        print(lookup_url)
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}  
        return r.json()
      
    def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator == "not":
                operator = operator.upper()
            if isinstance(operator_query, str):
                query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query,"type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)

    def search_reccomendations_clear(self, market, target_danceability, min_energy, pop):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/recommendations"
        data = urlencode({"market": "US", "target_danceability": "0.9","min_energy": "0.9", "seed_genres": "pop"})
        lookup_url = f"{endpoint}?{data}"
        print(lookup_url)
        r = requests.get(lookup_url, headers = headers)
        if r.status_code not in range(200,299):
            return {}
        print(r.json())
    
    def search_reccomendations_clouds(self, market, target_danceability, max_energy, pop):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/recommendations"
        data = urlencode({"market": "US", "target_danceability": "0.5","max_energy": "0.5", "seed_genres": "pop"})
        lookup_url = f"{endpoint}?{data}"
        print(lookup_url)
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        print(r.json())
    
    def search_reccomendations_thunderstorm(self, market, target_danceability, max_energy, pop):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/recommendations"
        data = urlencode({"market": "US", "target_danceability": "0.2","max_energy": "0.7", "seed_genres": "pop"})
        lookup_url = f"{endpoint}?{data}"
        print(lookup_url)
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        print(r.json())
    
    def search_reccomendations_rain(self, market, target_danceability, max_energy, pop):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/recommendations"
        data = urlencode({"market": "US", "target_danceability": "0.1","max_energy": "0.2", "seed_genres": "pop"})
        lookup_url = f"{endpoint}?{data}"
        print(lookup_url)
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        print(r.json())
    
    def search_reccomendations_drizzle(self, market, target_danceability, max_energy, pop):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/recommendations"
        data = urlencode({"market": "US", "target_danceability": "0.4","max_energy": "0.3", "seed_genres": "pop"})
        lookup_url = f"{endpoint}?{data}"
        print(lookup_url)
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        print(r.json())
class OpenWeatherApi():
    
    def __init__(self):
        self.baseurl = "https://api.openweathermap.org/data/2.5/weather?"
        self.apiKey = None
    
    def __formRequest(self, query, lsParams):
        qPar = ",".join(lsParams)
        argurl = "{base}{q}={qP}&appid={key}".format(base=self.baseurl, q=query, qP=qPar, key=self.apiKey)
        return argurl
    
    def sendRequest(self, query, lsParams):
        '''
        Returns weather of location or the empty string if invalid arguments
        
        :param str query: "q" for cityname, "zip" for zipcode
        :param list[str] lsParams: a list of query parameters
        '''
        argurl = self.__formRequest(query, lsParams)
        response = requests.get(argurl)
        if response.status_code != 200:
            print(response.json())
            return ""
        else:
            return response.json()["weather"][0]["main"]

def main():
    weatherApi = OpenWeatherApi()
    spotify = SpotifyAPI(client_id, client_secret, user_id)
    count = 0
    while count < 1:
        locType = input('Press 1 for City Name, 2 for Zip Code, or 3 to terminate')
        if locType == "1":
            query = "q"
            params = input("Enter city name: ")
        elif locType == "2":
            query = "zip"
            params = input("enter zipcode")
        elif locType == "3":
            break
        count += 1
        weather = weatherApi.sendRequest(query, params.split(" "))
        print("The weather in {p} is {w}".format(p=params, w=weather))  
    if weather == "Clear":
        spotify.search_reccomendations_clear("US", "0.5", "0.5", "pop")
    elif weather == "Clouds":
         spotify.search_reccomendations_clouds("US", "0.5", "0.5", "pop")
    elif weather == "Thunderstorm ":
         spotify.search_reccomendations_thunderstorm("US", "0.2", "0.7", "pop")
    elif weather == "Rain":
         spotify.search_reccomendations_rain("US", "0.1", "0.2", "pop")
    elif weather == "Drizzle":
         spotify.search_reccomendations_drizzle("US", "0.4", "0.3", "pop")
    else:
         spotify.search_reccomendations_clear("US", "0.7", "0.4", "pop")
if __name__ == "__main__": main()


# In[ ]:





# In[ ]:




