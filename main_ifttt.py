import tomllib
import requests
from dog_facts_api import DogFactsAPI
from dog_img_api import DogImageAPI


def read_toml(filepath: str) -> dict:
    with open(filepath, "rb") as f:
        config = tomllib.load(f)
    return config


class LineNotifier:
    def __init__(self, config: dict):
        ifttt_config = config["IFTTT"]
        self.ifttt_applet = ifttt_config["applet"]
        self.ifttt_key = ifttt_config["key"]
        self.trigger_base_url = f"https://maker.ifttt.com/trigger/{self.ifttt_applet}/with/key/{self.ifttt_key}?"

    def send_line_msg(
        self, fact: str, fact_zh_text: str, img_url: str, breed: str
    ) -> None:
        trigger_url = self.trigger_base_url
        trigger_url += f"value1={fact_zh_text}({fact})"
        trigger_url += f"&value2=圖片狗狗品種: {breed.capitalize()}"
        trigger_url += f"&value3={img_url}"
        requests.get(trigger_url)


def run():
    # Get dog facts
    dog_facts_api = DogFactsAPI()
    fact = dog_facts_api.get_raw_fact()
    fact_zh_text = dog_facts_api.get_translated_fact(fact)

    # Get dog images
    dog_img_api = DogImageAPI()
    breed = dog_img_api.find_match_dog_breed(fact)
    img_url = dog_img_api.get_img_url_by_breed(breed)
    while not img_url:
        img_url, breed = dog_img_api.get_random_img_url_and_breed()

    # Send LINE message
    config = read_toml("config.toml")
    line_notifier = LineNotifier(config)
    if fact_zh_text:
        print(fact)
        print(fact_zh_text)
        print(breed)
        print(img_url)
        line_notifier.send_line_msg(fact, fact_zh_text, img_url, breed)
        return fact_zh_text
    else:
        return "No facts available!"

# run()