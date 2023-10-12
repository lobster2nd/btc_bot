import requests

import pydantic_models
from config import api_url


def update_user(user: dict):
    user = pydantic_models.User_to_update.model_validate(user)
    response = requests.put(f'{api_url}/user/{user.id}', data=user.model_dump_json())
    try:
        return response.json()
    except:
        return response.text


def delete_user(user_id: int):
    return requests.delete(f'{api_url}/user/{user_id}').json()


def create_user(user: pydantic_models.User_to_create):
    user = pydantic_models.User_to_create.model_validate(user)
    return requests.post(f'{api_url}/user/create', data=user.model_dump_json()).json()


def get_info_about_user(user_id):
    return requests.get(f'{api_url}/get_info_by_user_id/{user_id}').json()


def get_user_balance_by_id(user_id):
    response = requests.get(f'{api_url}/get_user_balance_by_id/{user_id}')
    try:
        return float(response.text)
    except:
        return f'Error: Not a Number\nResponce: {response.text}'


def get_total_balance():
    response = requests.get(f'{api_url}/get_total_balance')
    try:
        return float(response.text)
    except:
        return f'Error: Not a Number\nResponce: {response.text}'


def get_users():
    return requests.get(f"{api_url}/users").json()


def get_user_wallet_by_tg_id(tg_id):
    user_dict = get_user_by_tg_id(tg_id)
    return requests.get(f"{api_url}/get_user_wallet/{user_dict['id']}").json()


def get_user_by_tg_id(tg_id):
    return requests.get(f"{api_url}/user_by_tg_id/{tg_id}").json()


def create_transaction(tg_id, receiver_address: str,
                       amount_btc_without_fee: float):
    user_dict = get_user_by_tg_id(tg_id)
    payload = {'receiver_address': receiver_address,
               'amount_btc_without_fee': amount_btc_without_fee}
    response = requests.post(f"{api_url}/create_transaction/{user_dict['id']}",
                             json=payload)
    return response.text
