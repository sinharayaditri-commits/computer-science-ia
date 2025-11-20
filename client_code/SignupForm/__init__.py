from ._anvil_designer import SignupFormTemplate
import anvil.users
from anvil import open_form
import anvil.server
import anvil
from anvil.notification import Notification

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
      Notification("All fields are required!", style="danger").show()
      return

    if len(password) < 6:
      Notification("Password must be at least 6 characters.", style="danger").show()
      return

    if '@' not in email:
      Notification("Please enter a valid email.", style="danger").show()
      return

      # Call server to create account
    result = anvil.server.call('create_user_account', name, email, password, role)

    if result['success']:
      Notification(result['message'], style="success").show()
      open_form('LoginForm')
    else:
      Notification(result['message'], style="danger").show()

  def role_dropdown_change(self, **event_args):
    """Update role description"""
    role = self.role_dropdown.selected_value
    if hasattr(self, 'role_description'):
      if role == "admin":
        self.role_description.text = "Admin: Manage tasks and approve new admins"
      else:
        self.role_description.text = "Teacher: Submit IT issues"

  def email_box_pressed_enter(self, **event_args):
    self.password_box.focus()

  def password_box_pressed_enter(self, **event_args):
    self.signup_btn_click()

  def login_link_click(self, **event_args):
    open_form("LoginForm")