from ._anvil_designer import TeacherDashboardTemplate
from anvil import open_form
import anvil.server
import anvil.users
import anvil

class TeacherDashboard(TeacherDashboardTemplate):
  def __init__(self, user_email=None, **properties):
    self.init_components(**properties)
    self.user_email = user_email
    self.load_dashboard()

  def load_dashboard(self):
    """Load dashboard data"""
    try:
      if not self.user_email:
        anvil.alert("Error: User email not found. Please login again.")
        open_form("LoginForm")
        return

      self.welcome_label.text = f"Welcome, {self.user_email}!"

      # Load issues
      self.refresh_issues()
    except Exception as err:
      anvil.alert(f"❌ Error loading dashboard: {str(err)}")

  def refresh_issues(self):
    """Refresh the issues list"""
    try:
      issues = anvil.server.call('get_teacher_issues', self.user_email)

      # Populate DataGrid
      self.issues_grid.rows = [
        {
          'title': issue['title'],
          'urgency': issue['urgency'],
          'status': issue['status'],
          'created_at': issue['created_at'],
          'last_updated': issue['last_updated']
        }
        for issue in issues
      ]
    except Exception as err:
      anvil.alert(f"❌ Error loading issues: {str(err)}")

  def report_new_issue_btn_click(self, **event_args):
    """Navigate to report issue form"""
    open_form("ReportIssueForm", user_email=self.user_email)

  def refresh_btn_click(self, **event_args):
    """Refresh the dashboard"""
    self.refresh_issues()
    anvil.alert("✅ Dashboard refreshed!")

  def logout_click(self, **event_args):
    """Logout and return to login"""
    open_form("LoginForm")