import helium
from smolagents import InferenceClientModel

from tui_flow import TuiFlow
from web_browsing_agent import WebBrowsingAgent
import argparse
from utils import init_browser_driver
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="Qwen/Qwen3-VL-8B-Instruct", help="Model to use. Has to be a VLM to work")
    parser.add_argument("--task_prompt", type=str, help="Instructions prompt path", default="./prompts/task_prompt.txt")
    parser.add_argument("--user_prompt", type=str, help="User prompt path", default="./prompts/user_prompt.txt")
    return parser.parse_args()


def main():
    args = parse_args()
    init_browser_driver()
    agent = WebBrowsingAgent(InferenceClientModel, args.model)
    tui = TuiFlow(agent, args.task_prompt, args.user_prompt)
    tui.run()
    helium.kill_browser()


if __name__ == "__main__":
    main()