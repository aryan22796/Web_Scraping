import json
import requests

import pyttsx3

import speech_recognition as sr
import re



API_KEY="tSrxJpt9AO67"
Project_Token="ty6iAqARazfq"
Run_token="thhTrqrevWfu"



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
    def get_list_of_country(self):
        countries=[]
        for country in self.data['country']:
            countries.append(country['name'].lower())

        return countries





def speak(text):
    engine=pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r= sr.Recognizer()
    with sr.Microphone()as source:
        audio = r.listen(source)
        said=""

        try:
            said=r.recognize_google(audio)
        except Exception as e:
            print("exception:",str(e))
    return said.lower()

def main():
    print("Start PROGRAM")
    data= Data(API_KEY,Project_Token)
    END_PHASE="stop"
    country_list=data.get_list_of_country()


    TOTAL_PATTERNS={
                    re.compile("[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
                    re.compile("[\w\s]+ total  cases"):data.get_total_cases,
                    re.compile("[\w\s]+ total [\w\s]+ deaths"):data.get_total_deaths,
                     re.compile("[\w\s]+ total deaths"):data.get_total_deaths,

                    }

    COUNTRY_PATTERNS = {
        re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
        re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],
                 
         }

    while True:
        print("I AM LISTENING...")
        text=get_audio()
        print(text)
        result=None
        

        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words=set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result=func(country)
                        break

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result=func()
                break

        if result:
            speak(result)

        if text.find(END_PHASE) != -1:
            print("EXIT")
            break


main()



