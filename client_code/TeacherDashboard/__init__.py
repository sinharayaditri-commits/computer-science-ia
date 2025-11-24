# client code: TeacherDashboard.py
from ._anvil_designer import TeacherDashboardTemplate
from anvil import open_form
import anvil.server
import anvil

class TeacherDashboard(TeacherDashboardTemplate):
  def __init__(self, user_email=None, **properties):
    self.init_components(**properties)
    self.user_email = user_email
    self.load_dashboard()

  def load_dashboard(self):
    try:
      if not self.user_email:
        anvil.alert("User not found. Please log in again.")
        open_form("LoginForm")
        return
      self.welcome_label.text = f"Welcome, {self.user_email}!"
      self.refresh_issues()
    except Exception as e:
      anvil.alert(f"Error loading dashboard: {e}")

  def refresh_issues(self):
    try:
      issues = anvil.server.call('get_teacher_issues', self.user_email)
      self.issues_grid.rows = issues
    except Exception as e:
      anvil.alert(f"Error fetching issues: {e}")

  def report_new_issue_btn_click(self, **event_args):
    open_form("ReportIssueForm", user_email=self.user_email)

  def refresh_btn_click(self, **event_args):
    self.refresh_issues()

  def logout_click(self, **event_args):
    open_form("LoginForm")