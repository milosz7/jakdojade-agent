from utils import random_sleep, build_query_url
from smolagents import tool
from selenium.webdriver.common.by import By
import helium
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@tool
def write_text_to_input(placeholder: str, text: str) -> None:
    """
    Writes text to input on the page. Placeholder text is responsible for locating the element.
    Args:
        placeholder: The placeholder text to locate an element on the page.
        text: The text to write to the found element.
    """
    requested_input = helium.S(f'input[placeholder="{placeholder}"]')
    helium.write(text=text, into=requested_input)


@tool
def use_jakdojade_to_find_routes(
    start: str, dest: str, city: str, date: str, time: str
) -> None:
    """
    Navigates to the best route based on the parameters
    Args:
         start: Start location query
         dest: Destination location query
         city: City query
         date: Date query
         time: Time query
    """
    helium.go_to("jakdojade.pl")
    random_sleep()
    try:
        helium.click("PRZEJDŹ DO SERWISU")
        random_sleep()
    except LookupError:
        print("Rules already accepted. Going to browse cities")
        pass
    try:
        helium.click("Browse available cities")
        random_sleep()
        write_text_to_input("Search city…", city)
        search_results = helium.S('ul[role="listbox"]')
        best_result = search_results.web_element.find_element(
            By.TAG_NAME, "app-city-list-item"
        )
        helium.click(best_result)
        random_sleep()
    except LookupError:
        print("City already selected. Going to search routes")
        pass
    write_text_to_input("Where are we starting?", start)
    random_sleep()
    search_results = helium.S('div[role="listbox"]')
    random_sleep()
    best_result = search_results.web_element.find_element(By.TAG_NAME, "div")
    random_sleep()
    helium.click(best_result)
    random_sleep()
    write_text_to_input("Where are we going?", dest)
    random_sleep()
    search_results = helium.S('div[role="listbox"]')
    random_sleep()
    best_result = search_results.web_element.find_element(By.TAG_NAME, "div")
    random_sleep()
    helium.click(best_result)
    random_sleep()
    helium.click("Show routes")
    random_sleep()
    current_url = helium.get_driver().current_url
    random_sleep()
    url = build_query_url(current_url, date, time)
    random_sleep()
    helium.go_to(url)
    found_routes = helium.S("app-planner-routes-list")
    random_sleep()
    best_result = found_routes.web_element.find_element(
        By.TAG_NAME, "app-planner-route"
    )
    random_sleep()
    helium.click(best_result)


def make_add_event_to_calendar_tool(calendar_service):

    @tool
    def add_event_to_calendar(
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        event_name: str,
        location: str,
        description: str,
    ) -> None:
        """
        Adds an event to the calendar.
        Args:
             year: Event year.
             month: Event month.
             day: Event day.
             hour: Event hour.
             minute: Event minute.
             event_name: Event name.
             location: Event location - requested route destination.
             description: Event desctiption which should include directions.
        """
        start_time = datetime(year, month, day, hour, minute)
        end_time = start_time + timedelta(hours=1)
        event = {
            "summary": event_name,
            "location": f"{location}",
            "description": f"{description}",
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "Europe/Warsaw",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "Europe/Warsaw",
            },
            "reminders": {
                "useDefault": True,
            },
        }
        event_result = (
            calendar_service.events().insert(calendarId="primary", body=event).execute()
        )
        logger.info(f"Event created: {event_result.get('htmlLink')}")

    return add_event_to_calendar
