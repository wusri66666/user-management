import base64

from utils.exceptions import DecodeException


def get_encode_user(data):
    byte_data = bytes(str(data), encoding="utf-8")
    base64_token = base64.b64encode(byte_data)
    return base64_token


def get_decode_user(data):
    try:
        data = base64.b64decode(data)
        data = str(data, encoding="utf8")
        return data
    except Exception as e:
        raise DecodeException


