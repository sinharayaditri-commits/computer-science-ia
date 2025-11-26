from ._anvil_designer import StartupFormTemplate
import anvil.users
import anvil
import anvil.server
from anvil import open_form

class StartupForm(StartupFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    user = anvil.users.get_user()

    if user:
      try:
        user_data = anvil.server. call('get_user_profile', user['email'])
        if user_data:
          role = user_data['role']
          if role == 'admin':
            open_form("AdminDashboard")
          else:
            open_form("TeacherDashboard", user_email=user['email'])
        else:
          open_form("LoginForm")
      except:
        open_form("LoginForm")
    else:
      open_form("LoginForm")