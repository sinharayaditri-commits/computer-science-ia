from ._anvil_designer import Form1Template
import anvil.users

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Prompt user to log in
    user = anvil.users.login_with_form()
    if user:
      role = user.get('role', None)
      if role == 'admin':
        from ..AdminDashboard import AdminDashboard
        self.clear()
        self.add_component(AdminDashboard())
      elif role == 'teacher':
        from ..TeacherDashboard import TeacherDashboard
        self.clear()
        self.add_component(TeacherDashboard())
      else:
        anvil.users.logout()
        anvil.alert("Unknown user role. Please contact the administrator.")
    else:
      anvil.alert("Login cancelled.")