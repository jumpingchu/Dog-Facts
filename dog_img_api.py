import json
import random
import requests


class DogImageAPI:
    def __init__(self):
        self.api_url_by_breed = "https://dog.ceo/api/breed/{breed}/images/"
        self.api_url_random = "https://dog.ceo/api/breeds/image/random"
        self.breeds_dict = {
            "message": {
                "affenpinscher": [],
                "african": [],
                "airedale": [],
                "akita": [],
                "appenzeller": [],
                "australian": ["kelpie", "shepherd"],
                "bakharwal": ["indian"],
                "basenji": [],
                "beagle": [],
                "bluetick": [],
                "borzoi": [],
                "bouvier": [],
                "boxer": [],
                "brabancon": [],
                "briard": [],
                "buhund": ["norwegian"],
                "bulldog": ["boston", "english", "french"],
                "bullterrier": ["staffordshire"],
                "cattledog": ["australian"],
                "cavapoo": [],
                "chihuahua": [],
                "chippiparai": ["indian"],
                "chow": [],
                "clumber": [],
                "cockapoo": [],
                "collie": ["border"],
                "coonhound": [],
                "corgi": ["cardigan"],
                "cotondetulear": [],
                "dachshund": [],
                "dalmatian": [],
                "dane": ["great"],
                "deerhound": ["scottish"],
                "dhole": [],
                "dingo": [],
                "doberman": [],
                "elkhound": ["norwegian"],
                "entlebucher": [],
                "eskimo": [],
                "finnish": ["lapphund"],
                "frise": ["bichon"],
                "gaddi": ["indian"],
                "germanshepherd": [],
                "greyhound": ["indian", "italian"],
                "groenendael": [],
                "havanese": [],
                "hound": [
                    "afghan",
                    "basset",
                    "blood",
                    "english",
                    "ibizan",
                    "plott",
                    "walker",
                ],
                "husky": [],
                "keeshond": [],
                "kelpie": [],
                "kombai": [],
                "komondor": [],
                "kuvasz": [],
                "labradoodle": [],
                "labrador": [],
                "leonberg": [],
                "lhasa": [],
                "malamute": [],
                "malinois": [],
                "maltese": [],
                "mastiff": ["bull", "english", "indian", "tibetan"],
                "mexicanhairless": [],
                "mix": [],
                "mountain": ["bernese", "swiss"],
                "mudhol": ["indian"],
                "newfoundland": [],
                "otterhound": [],
                "ovcharka": ["caucasian"],
                "papillon": [],
                "pariah": ["indian"],
                "pekinese": [],
                "pembroke": [],
                "pinscher": ["miniature"],
                "pitbull": [],
                "pointer": ["german", "germanlonghair"],
                "pomeranian": [],
                "poodle": ["medium", "miniature", "standard", "toy"],
                "pug": [],
                "puggle": [],
                "pyrenees": [],
                "rajapalayam": ["indian"],
                "redbone": [],
                "retriever": ["chesapeake", "curly", "flatcoated", "golden"],
                "ridgeback": ["rhodesian"],
                "rottweiler": [],
                "saluki": [],
                "samoyed": [],
                "schipperke": [],
                "schnauzer": ["giant", "miniature"],
                "segugio": ["italian"],
                "setter": ["english", "gordon", "irish"],
                "sharpei": [],
                "sheepdog": ["english", "indian", "shetland"],
                "shiba": [],
                "shihtzu": [],
                "spaniel": [
                    "blenheim",
                    "brittany",
                    "cocker",
                    "irish",
                    "japanese",
                    "sussex",
                    "welsh",
                ],
                "spitz": ["indian", "japanese"],
                "springer": ["english"],
                "stbernard": [],
                "terrier": [
                    "american",
                    "australian",
                    "bedlington",
                    "border",
                    "cairn",
                    "dandie",
                    "fox",
                    "irish",
                    "kerryblue",
                    "lakeland",
                    "norfolk",
                    "norwich",
                    "patterdale",
                    "russell",
                    "scottish",
                    "sealyham",
                    "silky",
                    "tibetan",
                    "toy",
                    "welsh",
                    "westhighland",
                    "wheaten",
                    "yorkshire",
                ],
                "tervuren": [],
                "vizsla": [],
                "waterdog": ["spanish"],
                "weimaraner": [],
                "whippet": [],
                "wolfhound": ["irish"],
            },
            "status": "success",
        }

    def find_match_dog_breed(self, fact: str) -> str:
        breeds_dict_keys = self.breeds_dict["message"].keys()
        breeds_list = list(breeds_dict_keys)
        for breed in breeds_list:
            breed_lowercase = breed.lower()
            if breed_lowercase in fact.lower():
                return breed
        return breeds_list[random.randint(0, len(breeds_list))]

    def get_img_url_by_breed(self, breed: str) -> str:
        api_url_with_breed = self.api_url_by_breed.format(breed=breed)
        resp = requests.get(api_url_with_breed)
        img_url_list = json.loads(resp.text)["message"]
        random.shuffle(img_url_list)
        for img_url in img_url_list:
            img_resp = requests.get(img_url)
            if img_resp.ok:
                # return img_url
                return 
            else:
                img_url_list.remove(img_url)
        return
    
    def get_random_img_url_and_breed(self):
        resp = requests.get(self.api_url_random)
        img_url = json.loads(resp.text)["message"]
        img_resp = requests.get(img_url)
        if img_resp.ok:
            split_img_url = img_url.split("/")
            breed = split_img_url[-2]
            return img_url, breed
        return

