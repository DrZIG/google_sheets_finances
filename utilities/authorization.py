import os
from typing import Optional

import gspread
import requests
from gspread import Client
from oauth2client.service_account import ServiceAccountCredentials
from requests import Session

_client: Optional[Client] = None
_session: Optional[Session] = None


def get_client() -> Client:
    global _client
    if not _client:
        current_file = os.path.abspath(os.path.dirname(__file__))
        secret = os.path.join(current_file, "..\\resources\\python-sheets-secret.json")
        _scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        _credentials = ServiceAccountCredentials.from_json_keyfile_name(secret, _scope)
        _client = gspread.authorize(_credentials)
    return _client


def get_session() -> Session:
    global _session
    if not _session:
        _session = requests.Session()
        _session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'})
    return _session


def close_session():
    global _session
    if _session:
        _session.close()
