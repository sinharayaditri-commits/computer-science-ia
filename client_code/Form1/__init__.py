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
    
    user = anvil.users.get_user()
    if not user:
      open_form('LoginForm')
    elif user['job_type'] == 'Admin':
      open_form('AdminDashboard')
    elif user['job_type'] == 'Teacher':
      open_form('TeacherDashboard')
    else:
      alert("Unknown job type. Contact admin.")
      open_form('LoginForm')
      else:
        anvil.users.logout()
        anvil.alert("Unknown user role. Please contact the administrator.")
    else:
      anvil.alert("Login cancelled.")