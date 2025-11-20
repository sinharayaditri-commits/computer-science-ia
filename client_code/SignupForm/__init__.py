from ._anvil_designer import SignupFormTemplate
import anvil.users
from anvil import open_form
import anvil.server
import anvil

class SignupForm(SignupFormTemplate):

  def __init__(self, **properties):
    self.init_components(**properties)
    self.role_dropdown.items = ["teacher", "admin"]

  def signup_btn_click(self, **event_args):
    try:
      if not self.email.text or not self.password.text:
        Notification("Email and Password cannot be empty!", style="danger").show()
        return

      name = self.name_box.text
      email = self.email_box.text
      password = self.password.text
      role = self.role_dropdown.selected_value

      result = anvil.server.call('create_user_account', name, email, password, role)

      if result['success']:
        Notication(result['message'], style="success").show()
        open_form('LoginForm')
      else:
        Notification(result['message'], style="danger").show()

    except Exception as err:
      Notification(f"Signup failed: [err]", style="danger").show()
      

    # ---------------------------------------
    # Redirect after signup
    # ---------------------------------------
    if role == "teacher":
      anvil.alert("Account created! You can now log in.")
      open_form("LoginForm")

    elif role == "admin":
      anvil.alert("Admin account request sent. Await approval.")
      open_form("LoginForm")

  def role_dropdown_change(self, **event_args):
    pass

  def email_box_pressed_enter(self, **event_args):
    self.password_box.focus()
