# Gets metadata from passport and creates TR on provider

import requests
import os
import xml.etree.ElementTree as ET



class TrCreator():
    def __init__(self):
        try:
            self.idp_host = os.environ['PROVIDER_HOST']
            self.passport_host = os.environ['PASSPORT_HOST']
            self.idp_api_client_id = os.environ['API_CLIENT_ID']
            self.idp_api_secret = os.environ['API_CLIENT_SECRET']
            self.provider_id = os.environ['PROVIDER_ID']
        except KeyError as error:
            print("ERROR! Looks like ENV variables are not set correctly!")
            raise error




    def parseMetaData(self):
        url = "https://"+self.passport_host+"/passport/auth/meta/idp/"+self.provider_id
        # url = "https://"+self.passport_host+"/passport/auth/meta/idp/gluu-two-saml"
        response = requests.get(url, verify=False)
        print("Getting metadata for from passport saml provider...")
        file = open(self.provider_id+"metadata.xml", "w")
        file.write(response.text)
        file.close()




trc = TrCreator()
trc.parseMetaData()

