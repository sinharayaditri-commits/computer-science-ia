from ._anvil_designer import StartupFormTemplate
from anvil import open_form
import anvil

class StartupForm(StartupFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    open_form("LoginForm")
