from ._anvil_designer import SignupFormTemplate
from anvil import open_form
import anvil.users
import anvil. server
import anvil

class SignupForm(SignupFormTemplate):

  def __init__(self, **properties):
    self.init_components(**properties)
    self.role_dropdown. items = ["teacher", "admin"]

  def signup_btn_click(self, **event_args):
    name = self.name_box.text.strip()
    email = self.email_box.text.strip()
    password = self.password_box.text
    role = self.role_dropdown.selected_value

    if not (name and email and password and role):
      anvil.alert("Please fill in all fields.")
      return

    try:
      result = anvil.server.call(
        "create_user_account",
        name, email, password, role
      )

      if result. get('success'):
        if role == "teacher":
          anvil.alert("Account created!  You can now log in.")
        else:
          anvil.alert("Admin account request sent.  Await approval.")
        open_form("LoginForm")
      else:
        anvil.alert(f"Error: {result. get('message', 'Unknown error')}")
    except Exception as e:
      anvil.alert(f"Error creating account: {str(e)}")

  def role_dropdown_change(self, **event_args):
    pass

  def email_box_pressed_enter(self, **event_args):
    self.password_box.focus()