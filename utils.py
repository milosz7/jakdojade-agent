from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium import webdriver
import logging
import helium
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import random
from time import sleep

logger = logging.getLogger(__name__)


def init_calendar_service(credentials_path="credentials.json"):
    scopes = ["https://www.googleapis.com/auth/calendar.events"]
    try:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
        creds = flow.run_local_server(port=0)
        service = build("calendar", "v3", credentials=creds)
        return service
    except Exception as e:
        logger.error(f"Failed to initialize calendar service: {e}")
        return None


def init_browser_driver(*chrome_args):
    chrome_options = webdriver.ChromeOptions()
    for arg in chrome_args:
        chrome_options.add_argument(arg)

    driver = helium.start_chrome(headless=False, options=chrome_options)
    return driver


def build_query_url(url, date, time):
    scheme, netloc, path, query, fragment = urlsplit(str(url))
    params = dict(parse_qsl(query))
    new_params = {**params, "d": date, "h": time, "ia": "true"}
    new_query = urlencode(new_params, doseq=True, safe=":")
    safe_url = urlunsplit((scheme, netloc, path, new_query, fragment))
    return safe_url


def random_sleep():
    random_frac = random.random()
    min_sleep = 1.0
    added_sleep = 0.5
    sleep(min_sleep + added_sleep * random_frac)
