from ._anvil_designer import LoginFormTemplate
from anvil import open_form
import anvil.users
import anvil
from anvil.tables import app_tables

class LoginForm(LoginFormTemplate):

  def __init__(self, **properties):
    self.init_components(**properties)
    # Do not auto-open other forms here

  def login_btn_click(self, **event_args):
    email = self.email_box.text.strip()
    password = self.password_box.text

    try:
      user = anvil.users.login_with_email(email, password)
    except anvil.users.AuthenticationFailed:
      anvil.alert("Incorrect email or password.")
      return

    # Get user row linked to Anvil User
    user_row = app_tables.users.get(anvil_user=user)

    if not user_row:
      anvil.alert("Your account is missing profile data. Contact admin.")
      return

    # Block unapproved admin accounts
    if user_row['role'] == "admin" and user_row['status'] == "pending":
      anvil.alert("Your admin request is still pending approval.")
      anvil.users.logout()
      return

    # Determine role
    role = user_row['role'] if user_row['role'] else "teacher"

    # Redirect
    if role == "admin":
      open_form("AdminDashboard")
    else:
      open_form("TeacherDashboard")

  def password_box_pressed_enter(self, **event_args):
    """Called when Enter is pressed in the password box"""
    self.login_btn_click()

  def signup_btn_click(self, **event_args):
    """This runs when the user clicks the Signup button"""
    open_form("SignupForm")

  def password_box_hide(self, **event_args):
    """This method is called when the TextBox is removed from the screen"""
    pass

  def signup_link_click(self, **event_args):
    """This runs when the signup link is clicked"""
    open_form("SignupForm")

  def email_box_pressed_enter(self, **event_args):
    """This runs when Enter is pressed in the email box"""
    self.password_box.focus()
