import json
import requests
import googletrans


class DogFactsAPI:
    def __init__(self):
        self.api_url = "https://dogapi.dog/api/v2/facts"

    def get_raw_fact(self) -> str:
        resp = requests.get(self.api_url)
        fact_json = json.loads(resp.text)
        fact = fact_json["data"][0]["attributes"]["body"]
        return fact

    def get_translated_fact(self, fact) -> str:
        translator = googletrans.Translator()
        fact_zh = translator.translate(fact, dest="zh-tw")
        return fact_zh.text

