from ._anvil_designer import TeacherDashboardTemplate
from anvil import open_form
import anvil.server
import anvil
import anvil.users

class TeacherDashboard(TeacherDashboardTemplate):
  def __init__(self, user_email=None, **properties):
    self.init_components(**properties)

    if not user_email:
      user = anvil.users.get_user()
      if user:
        user_email = user['email']

    self.user_email = user_email
    self.load_dashboard()

  def load_dashboard(self):
    try:
      if not self.user_email:
        anvil.alert("User not found.  Please log in again.")
        open_form("LoginForm")
        return

      test_result = anvil.server.call('test_tables')
      print(f"TEST RESULT: {test_result}")
      anvil.alert(f"Table test: {test_result['message']}")

      self.welcome_label.text = f"Welcome, {self.user_email}!"
      self.refresh_issues()
    except Exception as e:
      anvil.alert(f"Error loading dashboard: {e}")

  def refresh_issues(self):
    try:
      issues = anvil.server.call('get_teacher_issues', self.user_email)

      # DEBUG - Let's see what we got! 
      print(f"DEBUG: Got {len(issues)} issues from server")
      print(f"DEBUG: Issues data: {issues}")

      if issues:
        print(f"DEBUG: First issue: {issues[0]}")

      self.issues_grid.items = issues
      print(f"DEBUG: Set issues_grid. items successfully")

    except Exception as e:
      print(f"ERROR in refresh_issues: {e}")
      import traceback
      traceback. print_exc()

  def report_new_issue_btn_click(self, **event_args):
    open_form("ReportIssueForm", user_email=self.user_email)

  def refresh_btn_click(self, **event_args):
    self.refresh_issues()

  def logout_click(self, **event_args):
    anvil.users.logout()
    open_form("LoginForm")