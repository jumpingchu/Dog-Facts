import json
import requests
import googletrans

api_url = "https://dogapi.dog/api/v2"
facts_endpoint = api_url + "/facts"

resp = requests.get(facts_endpoint)
fact_json = json.loads(resp.text)
fact = fact_json['data'][0]['attributes']['body']

translator = googletrans.Translator()
fact_translated = translator.translate(fact, dest='zh-tw')
print(fact_translated.text)
