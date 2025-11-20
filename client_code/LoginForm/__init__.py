from ._anvil_designer import LoginFormTemplate
import anvil.users
from anvil import open_form
import anvil.server
import anvil

class LoginForm(LoginFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def login_btn_click(self, **event_args):
    """Handle login button click"""
    email = self.email_box.text.strip()
    password = self.password_box.text.strip()

    if not email or not password:
      anvil.alert("Please enter email and password.")
      return

    # Call server to verify credentials
    result = anvil.server.call('verify_login', email, password)

    if result['success']:
      role = result['role']
      # Open dashboard and pass email as parameter
      if role == 'admin':
        open_form("AdminDashboard", user_email=email)
      else:
        open_form("TeacherDashboard", user_email=email)
    else:
      anvil.alert(result['message'])

  def password_box_pressed_enter(self, **event_args):
    """Allow Enter key to submit"""
    self.login_btn_click()

  def signup_link_click(self, **event_args):
    """Navigate to signup"""
    open_form("SignupForm")

  def email_box_pressed_enter(self, **event_args):
    """Tab to password on Enter"""
    self.password_box.focus()