import logging
logger = logging.getLogger(__name__)


class TuiFlow:
    def __init__(self, agent, insructions_prompt, user_prompt_template_path):
        self.agent = agent
        self.instructions_prompt = self.load_prompt(insructions_prompt)
        self.user_prompt_template = self.load_prompt(user_prompt_template_path)

    @staticmethod
    def load_prompt(prompt_path):
        try:
            with open(prompt_path, 'r') as f:
                prompt = f.read()
                return prompt
        except FileNotFoundError:
            logger.error(f"File {prompt_path} not found")

    def format_user_prompt(self, format_dict):
        try:
            return self.user_prompt_template.format(**format_dict)
        except KeyError as e:
            logger.error(f"Failed to format prompt: {e}")

    @staticmethod
    def ask_question(question):
        try:
            answer = input(question + "\n")
            return answer
        except KeyboardInterrupt:
            logger.error("User interrupted")
            exit(1)


    def run(self):
        logger.info("Hello I am your jakdojade planner agent. Answer a few questions about your event plan.")
        questions = {
            "city": "What city are you in?",
            "start": "What is your starting destination?",
            "end": "What is your ending destination?",
            "event": "How should I name the event in the calendar?",
            "date": "What is the date of the event? (DD.MM.YYYY hh:mm)",
        }
        answers = {}
        for q_key, q_value in questions.items():
            answers[q_key] = self.ask_question(q_value)

        user_prompt = self.format_user_prompt(answers)
        logger.info(user_prompt)
        self.agent.run(self.instructions_prompt + user_prompt)
