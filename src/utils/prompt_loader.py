from jinja2 import Environment, FileSystemLoader
import os

class PromptLoader:
    """
    Utility for loading and rendering Jinja2 templates
    from a 'prompts/' folder (default in the project root).
    """
    
    def __init__(self, template_dir: str = None, base_context: dict = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.template_dir = template_dir or os.path.join(base_dir, "../prompts")
        self.env = Environment(loader=FileSystemLoader(self.template_dir),
                                autoescape=False,       
                                trim_blocks=True,     
                                lstrip_blocks=True
                                )
        self.base_context = base_context or {}

    def render(self, template_name: str, context: dict) -> str:
        """
        Renders a Jinja2 prompt with the passed variables.
        """
        merged_context = {**self.base_context, **context}
        template = self.env.get_template(template_name)
        return template.render(merged_context)
