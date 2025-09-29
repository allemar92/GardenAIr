from jinja2 import Environment, FileSystemLoader
import os

class PromptLoader:
    def __init__(self, template_dir: str = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.template_dir = template_dir or os.path.join(base_dir, "../prompts")
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def render(self, template_name: str, context: dict) -> str:
        """
        Rende un prompt Jinja2 con le variabili passate.
        """
        template = self.env.get_template(template_name)
        return template.render(context)
