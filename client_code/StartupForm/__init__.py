from ._anvil_designer import StartupFormTemplate
import anvil.users
import anvil
from anvil import open_form

class StartupForm(StartupFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Delay switching forms until after StartupForm has fully loaded
    anvil.js.call_js("setTimeout", lambda: open_form("LoginForm"), 0)
