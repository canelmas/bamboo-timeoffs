from base_api import BaseApi

BAMBOO_HR_API_URL = "https://api.bamboohr.com/api/gateway.php/{}/v1"


class BambooHRApi(BaseApi):
    def __init__(self, sub_domain, api_key):

        if not sub_domain:
            raise ValueError("Please pass a valid 'subdomain'")

        if not api_key:
            raise ValueError("Please pass a valid 'apikey'")

        super().__init__(BAMBOO_HR_API_URL.format(sub_domain), api_key=api_key)

    def get_list_of_employees(self):
        data = self.get("/employees/directory")
        return data['employees']

    def get_employee(self, employee_id):
        return self.get("/employees/{}".format(employee_id))

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

        return self.get("/time_off/requests", params=params)
