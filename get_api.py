import json
import tomllib
import requests
import googletrans


def read_toml(filepath: str) -> dict:
    with open(filepath, "rb") as f:
        config = tomllib.load(f)
    return config


def get_ifttt_config(config: dict) -> tuple:
    ifttt_config = config["IFTTT"]
    ifttt_applet = ifttt_config["applet"]
    ifttt_key = ifttt_config["key"]
    return ifttt_applet, ifttt_key


def get_dog_facts_api_url(config: dict) -> str:
    facts_api_url = config["DogAPI"]["api_url"] + config["DogAPI"]["facts"]
    return facts_api_url


def get_fact(url: str) -> str:
    resp = requests.get(url)
    fact_json = json.loads(resp.text)
    fact = fact_json["data"][0]["attributes"]["body"]
    return fact


def translate_fact(fact: str) -> str:
    translator = googletrans.Translator()
    fact_zh = translator.translate(fact, dest="zh-tw")
    fact_zh_text = fact_zh.text
    return fact_zh_text


def send_line_msg(
    ifttt_applet: str, ifttt_key: str, fact: str, fact_zh_text: str
) -> None:
    trigger_url = (
        f"https://maker.ifttt.com/trigger/{ifttt_applet}/with/key/{ifttt_key}?"
    )
    trigger_url += f"value1={fact_zh_text}"
    trigger_url += f"&value2={fact}"
    tmp_img_url = "https://media-cldnry.s-nbcnews.com/image/upload/rockcms/2022-01/210602-doge-meme-nft-mb-1715-8afb7e.jpg"
    trigger_url += f"&value3={tmp_img_url}"
    requests.get(trigger_url)


def run():
    config = read_toml("config.toml")
    facts_api_url = get_dog_facts_api_url(config)
    ifttt_applet, ifttt_key = get_ifttt_config(config)
    fact = get_fact(facts_api_url)
    fact_zh_text = translate_fact(fact)
    if fact_zh_text:
        print(fact)
        print(fact_zh_text)
        send_line_msg(ifttt_applet, ifttt_key, fact, fact_zh_text)


if __name__ == "__main__":
    run()
