
import json
API_KEY="tSrxJpt9AO67"
Project_Token="ty6iAqARazfq"
Run_token="thhTrqrevWfu"

import requests
import json



class Data:
    def __init__(self,api_key,project_token):
        self.api_key=api_key
        self.project_token=project_token
        self.params={
            "api_key":self.api_key
        }
        self.get_data()
    def get_data(self):
        response= requests.get(f'https://www.parsehub.com/api/v2/projects/{Project_Token}/last_ready_run/data',params={"api_key":API_KEY})
        self.data = json.loads(response.text)

    def get_total_cases(self):
        data= self.data['total']

        for content in data:
            if content['name'] =="Coronavirus Cases:":
                return content['value']
        return "0"

    def get_total_deaths(self):
        data= self.data['total']

        for content in data:
            if content['name'] == "Deaths:":
                return content['value']


    def get_country_data(self,country):
        data= self.data['country']

        for content in data:
            if content['name'].lower() == country.lower():
                return content

        return "0"



data= Data(API_KEY,Project_Token)

print(data.get_country_data("india")["total_cases"])


