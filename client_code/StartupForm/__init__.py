from ._anvil_designer import StartupFormTemplate
import anvil.users
import anvil
from anvil import open_form

class StartupForm(StartupFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Check if user is logged in
    user = anvil.users.get_user()

    if user:
      # User is already logged in - go to appropriate dashboard
      try:
        from anvil.tables import app_tables
        user_data = app_tables.users.get(email=user['email'])
        role = user_data.get('role', 'teacher')

        if role == 'admin':
          open_form("AdminDashboard")
        else:
          open_form("TeacherDashboard")
      except:
        open_form("LoginForm")
    else:
      # User not logged in - show login form
      open_form("LoginForm")