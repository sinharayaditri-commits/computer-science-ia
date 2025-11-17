from ._anvil_designer import SignupFormTemplate
from anvil import open_form
import anvil.users
from anvil.tables import app_tables
import anvil

class SignupForm(SignupFormTemplate):

  def __init__(self, **properties):
    self.init_components(**properties)

  def signup_btn_click(self, **event_args):
    name = self.name_box.text.strip()
    email = self.email_box.text.strip()
    password = self.password_box.text

    # Basic validation
    if not name or not email or not password:
      anvil.alert("Please fill in name, email and password.")
      return

    try:
      # Create the user account via Anvil Users service
      user = anvil.users.signup_with_email(email, password)

      # Add a row in your app_users table (recommended)
      # Make sure you have an App Table called "users" (app_tables.users)
      app_tables.users.add_row(
        anvil_user=user,    # link to the Anvil User object
        name=name,
        email=email,
        role="teacher"      # default role; admin can change later
      )

      anvil.alert("Sign-up successful. Please log in.")
      open_form("LoginForm")

    except Exception as e:
      # Show a helpful error to you (you can change this text later)
      anvil.alert(f"Sign-up failed: {e}")
