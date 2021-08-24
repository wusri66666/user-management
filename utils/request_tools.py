import requests


def server_requests(method, url, data=None, files=None, multipart=False, root_path=None):
    upper_method = method.upper()
    absolute_url = root_path + url
    if multipart:
        response = requests.request(method=upper_method, url=absolute_url, data=data, files=files,
                                    headers={'service': 'True'})
    else:
        response = requests.request(method=upper_method, url=absolute_url, json=data, headers={'service': 'True'})
    return response
