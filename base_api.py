import requests
from requests.auth import HTTPBasicAuth

HEADER_ACCEPT_JSON = {"Accept": "application/json"}


class BaseApi:
    def __init__(self, base_url, api_key=None, basic_auth_token=None) -> None:
        if not base_url:
            raise ValueError("Base url is missing!")

        self.base_url = base_url
        self.headers = HEADER_ACCEPT_JSON
        self.api_key = api_key
        self.basic_auth_token = basic_auth_token

    def get(self, url, params=None):
        r = requests.get(self.base_url + url,
                         params=params,
                         headers=self.headers,
                         auth=self.__get_auth())
        r.raise_for_status()
        return r.json()

    def __get_auth(self):
        if self.api_key:
            return self.api_key, 'X'
        elif self.basic_auth_token:
            self.headers["Authorization"] = "Basic {}".format(self.basic_auth_token)

        return None
