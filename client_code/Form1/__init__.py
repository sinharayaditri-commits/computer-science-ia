from ._anvil_designer import Form1Template
import anvil.users

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    action = anvil.alert("Do you want to Log In or Sign Up?", buttons=["Log In", "Sign Up"])
    if action == "Sign Up":
      user = anvil.users.signup_with_form()
      anvil.alert("Sign up successful! Please ask your admin to set your role and enable your account if required.")
      user = anvil.users.login_with_form()
    else:
      user = anvil.users.login_with_form()

    print('User object:', user)
    print('Role property:', user['role'] if 'role' in user else None)

    if user:
      role = user['role'] if 'role' in user else None
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