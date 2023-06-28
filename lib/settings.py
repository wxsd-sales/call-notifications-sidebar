import os
from dotenv import load_dotenv

load_dotenv()

class Settings(object):
	port = int(os.environ.get("MY_APP_PORT"))
	sf_client_id = os.environ.get("MY_SALESFORCE_CLIENT_ID")
	sf_client_secret = os.environ.get("MY_SALESFORCE_CLIENT_SECRET")
	sf_username = os.environ.get("MY_SALESFORCE_USERNAME")
	sf_password = os.environ.get("MY_SALESFORCE_PASSWORD")

	mockapi_url = os.environ.get("MY_MOCKAPI_URL")

