from ._anvil_designer import SignupFormTemplate
from anvil import open_form
import anvil.users
from anvil.tables import app_tables
import anvil

class SignupForm(SignupFormTemplate):

  def __init__(self, **properties):
    self.init_components(**properties)
    self.password_box.hide_text = True   # Make password hidden

  def signup_btn_click(self, **event_args):
    "3When the user clicks the Sign Up button"

    name = self.name_box.text.strip()
    email = self.email_box.text.strip()
    password = self.password_box.text
    school_code = self.school_code_box.text.strip()

    # Basic validation
    if not name or not email or not password or not school_code:
     anvil.alert("Please fill all fields.")
    return

    try:
      # Create the Anvil user
     # user = anvil.users.signup_with_email(email, password)

      # Default everyone to teacher (unless you choose otherwise)
      role = "teacher"

      # Save user info in your app table
      app_tables.users.add_row(
        name=self.name_box,
        email=self.email_box,
        school_code=self.school_code_box,
        password=self.password_box,
        role = "teacher"
        
      )

      # Redirect based on role
      if role == "admin":
        open_form("AdminDashboard")
      else:
        open_form("TeacherDashboard")

    except Exception as e:
      anvil.alert(f"Error: {e}")

  def email_box_pressed_enter(self, **event_args):
    "This method is called when the user presses Enter in this text box"
    pass
