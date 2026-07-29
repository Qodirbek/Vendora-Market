import requests
import os


API_URL = "https://sotuvchi.com/api/v2"


def get_offers():

    data = {
        "api_key":
        os.getenv("SOTUVCHI_KEY")
    }


    response = requests.post(
        API_URL + "/getOffers",
        data=data
    )


    return response.json()



def send_order(
        offer_id,
        phone,
        name,
        stream=None,
        region_id=None
):

    data = {

        "api_key":
        os.getenv("SOTUVCHI_KEY"),

        "offer_id":
        offer_id,

        "phone":
        phone,

        "name":
        name
    }


    if stream:
        data["stream"] = stream


    if region_id:
        data["region_id"] = region_id


    response = requests.post(
        API_URL + "/order",
        data=data
    )


    return response.json()