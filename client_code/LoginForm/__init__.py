from ._anvil_designer import LoginFormTemplate
from anvil import open_form
import anvil.users
import anvil
import anvil.  server

class LoginForm(LoginFormTemplate):

  def __init__(self, **properties):
    self.init_components(**properties)

  def login_btn_click(self, **event_args):
    email = self. email_box.text.  strip()
    password = self.  password_box. text

    print(f"DEBUG: Attempting login with email: {email}")

    try:
      user = anvil. users.login_with_email(email, password)
      print(f"DEBUG: Anvil auth successful for {email}")
    except anvil.users.AuthenticationFailed as e:
      error_msg = str(e)
      print(f"DEBUG: Anvil auth FAILED: {error_msg}")

      # If email not confirmed, skip to database check for TESTING
      if "confirmed your email" in error_msg:
        print(f"DEBUG: Email not confirmed - skipping Anvil, checking database directly")
        # Continue to database check below
      else:
        anvil.alert("Incorrect email or password.")
        return
    except Exception as e:
      print(f"DEBUG: Unexpected error during auth: {e}")
      anvil.alert(f"Login error: {e}")
      return

    print(f"DEBUG: Checking user profile in database...")
    try:
      user_data = anvil.server.call('get_user_profile', email)
      print(f"DEBUG: User data from database: {user_data}")
      if not user_data:
        anvil.alert("User profile not found.  Please sign up first.")
        return
    except Exception as e:
      print(f"DEBUG: Error getting profile: {e}")
      anvil. alert(f"Error: {str(e)}")
      return

    print(f"DEBUG: User role is: {user_data['role']}")
    if user_data['role'] == "admin" and user_data['status'] == "pending":
      anvil.alert("Your admin request is still pending approval.")
      return

    if user_data['role'] == "admin":
      print(f"DEBUG: Routing to AdminDashboard")
      open_form("AdminDashboard")
    else:
      print(f"DEBUG: Routing to TeacherDashboard with email {email}")
      open_form("TeacherDashboard", user_email=email)

  def password_box_pressed_enter(self, **event_args):
    self.login_btn_click()

  def signup_btn_click(self, **event_args):
    open_form("SignupForm")

  def signup_link_click(self, **event_args):
    open_form("SignupForm")

  def email_box_pressed_enter(self, **event_args):
    self.password_box.focus()