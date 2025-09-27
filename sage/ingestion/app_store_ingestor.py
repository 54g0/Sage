import requests
import sys
import os
import logging
import pandas as pd
from time import sleep
from typing import List
RAW_DATA_DIR = "data/raw"
RAPIDAPI_HOST = "appstore-scrapper-api.p.rapidapi.com"
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
class AppStoreIngestor:
    def __init__(self):
        self.headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "appstore-scrapper-api.p.rapidapi.com"
        }
        self.base_url = "https://appstore-scrapper-api.p.rapidapi.com/v1/app-store-api"

    def search_app(self, app_name:str, country:str="us",lang="en",num:int = 10):
        url = f"{self.base_url}/search"
        query_str ={"num":num,"lang":lang,"query":app_name,"country":country}
        response = requests.get(url,headers=self.headers,params=query_str)
        data = pd.json_normalize(response.json())
        file_path = os.path.join(RAW_DATA_DIR, "search_results.csv")
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        if not os.path.exists(file_path):
            data.to_csv(file_path,index=False,header=True)
        else:
            data.to_csv(file_path,mode="a",header=False,index=False)
        return data
    def get_app_details(self, app_id:str,country:str="us",lang="en"):
        url = f"{self.base_url}/detail"
        query_str ={"id":app_id,"lang":lang,"country":country}
        response = requests.get(url,headers=self.headers,params=query_str)
        data = pd.json_normalize(response.json())
        file_path = os.path.join(RAW_DATA_DIR, "app_details.csv")
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        if not os.path.exists(file_path):
            data.to_csv(file_path,index=False,header=True)
        else:
            data.to_csv(file_path,mode="a",header=False,index=False)
        return data
    def get_app_reviews(self,app_id:str,country:str="us",lang="en",num:int=10):
        url = f"{self.base_url}/reviews"
        query_str ={"id":app_id,"lang":lang,"country":country,"num":num}
        response = requests.get(url,headers=self.headers,params=query_str)
        data = pd.json_normalize(response.json())
        file_path = os.path.join(RAW_DATA_DIR, "app_reviews.csv")
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        if not os.path.exists(file_path):
            data.to_csv(file_path,index=False,header=True)
        else:
            data.to_csv(file_path,mode="a",header=False,index=False)
        return data
    def get_app_developers(self,developer_id:str,country:str="us",lang="en"):
        url = f"{self.base_url}/developer"
        query_str ={"country":country,"devId":developer_id,"lang":lang}
        response = requests.get(url,headers=self.headers,params=query_str)
        data = pd.json_normalize(response.json())
        file_path = os.path.join(RAW_DATA_DIR, "app_developers.csv")
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        if not os.path.exists(file_path):
            data.to_csv(file_path,index=False,header=True)
        else:
            data.to_csv(file_path,mode="a",header=False,index=False)
        return data
    def get_list_by_collections_genre(self,collection:str,category:str,country:str="us",lang="en",num:int=10):
        url = f"{self.base_url}/list"
        query_str ={"collection":collection,"category":category,"lang":lang,"country":country,"num":num}
        response = requests.get(url,headers=self.headers,params=query_str)
        data = pd.json_normalize(response.json())
        file_path = os.path.join(RAW_DATA_DIR, "app_collections.csv")
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        if not os.path.exists(file_path):
            data.to_csv(file_path,index=False,header=True)
        else:
            data.to_csv(file_path,mode="a",header=False,index=False)
        return data
    
if __name__ == "__main__":
    ingestor = AppStoreIngestor()
    ingestor.search_app("fitness app")
    ingestor.get_app_details("553834731")
    ingestor.get_app_reviews("553834731")
    ingestor.get_list_by_collections_genre("top-free","farming")
    ingestor.get_app_developers("526656015")