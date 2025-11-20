from ._anvil_designer import LoginFormTemplate
import anvil.users
from anvil import open_form
from anvil.tables import app_tables
import anvil

class LoginForm(LoginFormTemplate):   # <-- THIS MUST MATCH THE FORM NAME EXACTLY

  def __init__(self, **properties):
    self.init_components(**properties)

  def login_btn_click(self, **event_args):
    email = self.email_box.text.strip()
    password = self.password_box.text

    try:
      user = anvil.users.login_with_email(email, password)
    except anvil.users.AuthenticationFailed:
      anvil.alert("Incorrect email or password.")
      return

    # Get UID
    uid = user.get_id()

    # Match UID to user_profiles table
    user_row = app_tables.user_profiles.get(anvil_user=uid)

    if not user_row:
      anvil.alert("Your profile data is missing. Contact admin.")
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
    self.login_btn_click()

  def signup_btn_click(self, **event_args):
    open_form("SignupForm")

  def signup_link_click(self, **event_args):
    open_form("SignupForm")

  def email_box_pressed_enter(self, **event_args):
    self.password_box.focus()