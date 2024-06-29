import tomllib
import requests
import functions_framework
from dog_facts_api import DogFactsAPI
from dog_img_api import DogImageAPI


def read_toml(filepath: str) -> dict:
    with open(filepath, "rb") as f:
        config = tomllib.load(f)
    return config


class LineNotifier:
    def __init__(self, config: dict):
        self.line_token = config["LINE"]["token"]

    def send_line_notify(self, message, img_url):
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {self.line_token}"}
        data = {
            "message": message,
            "imageThumbnail": img_url,
            "imageFullsize": img_url,
        }
        response = requests.post(url, headers=headers, data=data)
        return response

    def create_message(
        self, fact: str, fact_zh_text: str, breed: str
    ) -> None:
        message = f"\n{fact_zh_text}\n\n({fact})\n\n(圖片狗狗品種: {breed.capitalize()})"
        return message

@functions_framework.http
def run(request):
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
        message = line_notifier.create_message(fact, fact_zh_text, breed)
        line_notifier.send_line_notify(message, img_url)
        return fact_zh_text
    else:
        return "No facts available!"
