from smolagents import CodeAgent, ActionStep
from tools import use_jakdojade_to_find_routes, make_add_event_to_calendar_tool
from time import sleep
import helium
from PIL import Image
from io import BytesIO
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class WebBrowsingAgent:
    def __init__(self, model_cls, model_id, calendar_credentials_path="credentials.json"):
        calendar_service = self.authenticate_calendar(calendar_credentials_path)
        add_event_to_calendar = make_add_event_to_calendar_tool(calendar_service)

        model = model_cls(model_id=model_id)
        self.agent = CodeAgent(
            tools=[
                use_jakdojade_to_find_routes,
                add_event_to_calendar,
            ],
            model=model,
            additional_authorized_imports=["helium"],
            step_callbacks=[self.save_screenshot],
            max_steps=20,
            verbosity_level=2,
        )
        # Import helium for the agent
        self.agent.python_executor("import helium")

    @staticmethod
    def authenticate_calendar(calendar_credentials_path="credentials.json"):
        scopes = ["https://www.googleapis.com/auth/calendar.events"]
        try:
            flow = InstalledAppFlow.from_client_secrets_file(calendar_credentials_path, scopes)
            creds = flow.run_local_server(port=0)
            service = build("calendar", "v3", credentials=creds)
            return service
        except Exception as e:
            logger.error(f"Failed to initialize calendar service: {e}")
            exit(1)

    @staticmethod
    def save_screenshot(memory_step: ActionStep, agent: CodeAgent) -> None:
        sleep(1.0)  # Let JavaScript animations happen before taking the screenshot
        driver = helium.get_driver()
        current_step = memory_step.step_number
        if driver is not None:
            for (
                previous_memory_step
            ) in agent.memory.steps:  # Remove previous screenshots for lean processing
                if (
                    isinstance(previous_memory_step, ActionStep)
                    and previous_memory_step.step_number <= current_step - 2
                ):
                    previous_memory_step.observations_images = None
            png_bytes = driver.get_screenshot_as_png()
            image = Image.open(BytesIO(png_bytes))
            print(f"Captured a browser screenshot: {image.size} pixels")
            memory_step.observations_images = [
                image.copy()
            ]  # Create a copy to ensure it persists

        url_info = f"Current url: {driver.current_url}"
        memory_step.observations = (
            url_info
            if memory_step.observations is None
            else memory_step.observations + "\n" + url_info
        )

    def run(self, instructions):
        return self.agent.run(instructions)