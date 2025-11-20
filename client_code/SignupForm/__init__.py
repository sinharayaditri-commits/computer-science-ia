from ._anvil_designer import SignupFormTemplate
import anvil.users
from anvil import open_form
import anvil.server
import anvil

class SignupForm(SignupFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.role_dropdown.items = ["teacher", "admin"]
    self.role_dropdown.selected_value = "teacher"

  def signup_btn_click(self, **event_args):
    """Handle signup"""
    name = self.name_box.text.strip()
    email = self.email_box.text.strip()
    password = self.password_box.text
    role = self.role_dropdown.selected_value

    # Validation
    if not name or not email or not password:
      anvil.alert("❌ All fields are required!")
      return

    if len(password) < 6:
      anvil.alert("❌ Password must be at least 6 characters.")
      return

    if '@' not in email:
      anvil.alert("❌ Please enter a valid email.")
      return

      # Call server to create account
    result = anvil.server.call('create_user_account', name, email, password, role)

    if result['success']:
      anvil.alert("✅ " + result['message'])
      open_form('LoginForm')
    else:
      anvil.alert("❌ " + result['message'])

  def role_dropdown_change(self, **event_args):
    """Show info about selected role"""
    pass

  def email_box_pressed_enter(self, **event_args):
    self.password_box.focus()

  def password_box_pressed_enter(self, **event_args):
    self.signup_btn_click()