import requests

BAMBOO_HR_API_URL = "https://api.bamboohr.com/api/gateway.php/{}/v1"
HEADER_ACCEPT_JSON = "Accept: application/json"
DATA_TYPE = "json"


class BambooHRApi:
    def __init__(self, sub_domain, api_key):

        if not sub_domain:
            raise ValueError("Please pass a valid 'subdomain'")

        if not api_key:
            raise ValueError("Please pass a valid 'apikey'")

        # json only for now
        self.data_type = DATA_TYPE

        self.headers = {"Accept": "application/json"}

        self.base_url = BAMBOO_HR_API_URL.format(sub_domain)

        self.api_key = api_key

    def get_list_of_employees(self):
        data = self.__get("/employees/directory")
        return data['employees']

    def get_employee(self, employee_id):
        return self.__get("/employees/{}".format(employee_id))

    def get_employee_time_offs(self, employee_id, start_date=None, end_date=None, type=None):

        if not employee_id:
            raise ValueError("Please pass an employee id")

        params = {'employeeId': employee_id}

        if start_date:
            params['start'] = start_date.strftime("%Y-%m-%d")

        if end_date:
            params['end'] = end_date.strftime("%Y-%m-%d")

        if type:
            params['type'] = type

        return self.__get("/time_off/requests", params=params)

    def __get(self, url, params=None):
        r = requests.get(self.base_url + url, params=params, headers=self.headers, auth=(self.api_key, 'X'))
        r.raise_for_status()
        return r.json()
