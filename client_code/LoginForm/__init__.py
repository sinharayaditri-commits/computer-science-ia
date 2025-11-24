# client code: LoginForm.py
from ._anvil_designer import LoginFormTemplate
from anvil import open_form
import anvil.server
import anvil

class LoginForm(LoginFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # no-op to avoid missing-hide warning if Designer still references it
    # (you can remove this method and the event in the Designer later)
  def password_box_hide(self, **event_args):
    pass

  def log_in_click(self, **event_args):
    """Called when the user clicks the 'log in' link/button."""
    email = (self.email_box.text or "").strip()
    password = (self.password_box.text or "").strip()
    if not email or not password:
      anvil.alert("Please enter both email and password.")
      return

    try:
      result = anvil.server.call('verify_login', email, password)
    except Exception as e:
      anvil.alert(f"Login error: {e}")
      return

    if result.get('success'):
      open_form("TeacherDashboard", user_email=email)
    else:
      # show server-provided message
      anvil.alert(result.get('message') or "Login failed.")