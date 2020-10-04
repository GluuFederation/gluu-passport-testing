import requests
import json
import os
import dataset
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


db = dataset.connect('sqlite:///helper.db')
user_helper = db['user_helper']

USER_NAME = os.getenv('USER_NAME')
USER_PASSWORD = os.getenv('USER_PASSWORD')
USER_MAIL = os.getenv('USER_MAIL')
USER_GIVEN = os.getenv('USER_GIVEN')
USER_SUR = os.getenv('USER_SUR')
PROVIDER_HOST = os.getenv('PROVIDER_HOST')
API_CLIENT_ID = os.getenv('API_CLIENT_ID')
API_CLIENT_SECRET = os.getenv('API_CLIENT_SECRET')


class TestUser:

    def __init__(self):
        self.user_name = USER_NAME
        self.password = USER_PASSWORD
        self.email = USER_MAIL
        self.given_name = USER_GIVEN
        self.sur_name = USER_SUR
        self.base_url = 'https://' + PROVIDER_HOST
        self.api_client_id = API_CLIENT_ID
        self.api_client_secret = API_CLIENT_SECRET

    def get_token(self):
        url = self.base_url + "/oxauth/restv1/token"
        payload = 'grant_type=client_credentials'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        authentication = requests.auth.HTTPBasicAuth(
            self.api_client_id, self.api_client_secret)

        response = requests.request(
            "POST", url, auth=authentication, headers=headers, data=payload, verify=False).json()
        return response['access_token']

    def get_users(self, token):
        url = self.base_url + "/identity/restv1/api/v1/users"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token

        }
        response = requests.request("GET", url, verify=False, headers=headers)
        print(response.json())

    def create_user(self, token):
        url = self.base_url + "/identity/restv1/api/v1/users"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token

        }
        data = {
            'userName': self.user_name,
            'password': self.password,
            'surName': self.sur_name,
            'givenName': self.given_name,
            'email': self.email,
            'status': 'ACTIVE',
            'displayName': self.user_name,

        }

        json_data = json.dumps(data)

        response = requests.request(
            "POST", url, headers=headers, data=json_data, verify=False)

        if response.status_code == 201:
            print("User created with success via API...")
            print(response.content)
            json_resp = response.json()
            user_helper.insert(json_resp)
            time.sleep(1)
        else:
            print("Error creating user, please check.")
            print('response status: %s' % response.status_code)
            print('reponse: %s' % response.content)

        time.sleep(1)

        return response

    def delete_user(self, token):
        url = self.base_url + "/identity/restv1/api/v1/users"
        users = user_helper.all()

        # user = helper.find_one(userName=self.user_name)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token
        }

        users_deleted = True

        for user in users:
            response = requests.request(
                "DELETE", url + "/" + user['inum'], headers=headers, verify=False
            )

            if response.status_code != 200:
                users_deleted = False

        user_helper.drop()

        return users_deleted
