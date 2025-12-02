# Pages module
from .input_page import render as render_input_page
from .story_page import render as render_story_page
from .script_page import render as render_script_page
from .style_page import render as render_style_page
from .cartoon_page import render as render_cartoon_page

__all__ = [
    'render_input_page',
    'render_story_page',
    'render_script_page',
    'render_style_page',
    'render_cartoon_page',
]

