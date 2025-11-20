from ._anvil_designer import LoginFormTemplate
import anvil.users
from anvil import open_form
from anvil.tables import app_tables
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

    try:
      # Authenticate with Anvil
      user = anvil.users.login_with_email(email, password)
    except anvil.users.AuthenticationFailed:
      anvil.alert("❌ Incorrect email or password.")
      return

      # Get user details from Users table
    try:
      user_data = app_tables.users.get(email=email)
    except:
      anvil.alert("❌ User profile not found. Contact admin.")
      anvil.users.logout()
      return

    role = user_data.get('role', 'teacher')
    status = user_data.get('status', 'pending')

    # Check if admin is approved
    if role == 'admin' and status != 'approved':
      anvil.alert("⏳ Your admin account is pending approval. Check your email.")
      anvil.users.logout()
      return

      # Redirect based on role
    if role == 'admin':
      open_form("AdminDashboard")
    else:
      open_form("TeacherDashboard")

  def password_box_pressed_enter(self, **event_args):
    """Allow Enter key to submit"""
    self.login_btn_click()

  def signup_link_click(self, **event_args):
    """Navigate to signup"""
    open_form("SignupForm")

  def email_box_pressed_enter(self, **event_args):
    """Tab to password on Enter"""
    self.password_box.focus()