from ._anvil_designer import LoginFormTemplate
from anvil import open_form
import anvil.users
import anvil

class LoginForm(LoginFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Do not auto-open other forms here

  def login_btn_click(self, **event_args):
    email = self.email_box.text.strip()
    password = self.password_box.text

    if not email or not password:
      anvil.alert("Please enter email and password.")
      return

    try:
      user = anvil.users.login_with_email(email, password)
    except anvil.users.AuthenticationFailed:
      anvil.alert("Incorrect email or password.")
      return

    # If you use an app table to store roles, lookup here; otherwise check user dict
    try:
      # Safe lookup: try app_tables.users -> column named anvil_user linking to Anvil user
      from anvil.tables import app_tables
      user_row = app_tables.users.get(anvil_user=user)
      role = user_row['role'] if user_row is not None else user.get('role')
    except Exception:
      role = user.get('role')

    if role == "admin":
      open_form("AdminDashboard")
    elif role == "teacher":
      open_form("TeacherDashboard")
    else:
      anvil.alert("No role assigned. Contact admin.")

  def signup_link_click(self, **event_args):
    open_form("SignupForm")
