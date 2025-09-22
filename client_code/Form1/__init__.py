from ._anvil_designer import Form1Template
import anvil.users

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # show the login form
    user = anvil.users.login_with_form()

    # if a user logs in, opens the appropriate dashboard
    if user:
      role = user.get('role', None)
      if role == 'admin':
        # open the admin dashboard form (you need to create this form)
        from ..AdminDashboard import AdminDashboard
        self.content_panel.clear()
        self.content_panel.add_component(AdminDashboard())
      elif role == 'teacher':
        # open the teacher dashboard form (you need to create this form)
        from ..TeacherDashboard import TeacherDashboard
        self.content_panel.clear()
        self.content_panel.add_component(TeacherDashboard())
      else:
        # unknown role, show an error or log out
        anvil.users.logout()
        alert("Unknown user role. Please contact the administrator.")
    else:
      # no user logged in, show a message or do nothing
      alert("Login cancelled.")