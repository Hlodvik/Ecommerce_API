import os
from dotenv import load_dotenv

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/ecom_api_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

load_dotenv()  # Load .env variables

DM_API_URL = os.getenv("CSL_API_URL")# see readme: @TARIFFS
DM_API_KEY = os.getenv("CSL_API_KEY")# projects access to linked API  