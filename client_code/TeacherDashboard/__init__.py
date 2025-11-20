from ._anvil_designer import TeacherDashboardTemplate
from anvil import open_form
import anvil.server
import anvil.users
import anvil

class TeacherDashboard(TeacherDashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_dashboard()

  def load_dashboard(self):
    """Load dashboard data"""
    try:
      # Get current user
      user = anvil.users.get_user()
      self.welcome_label.text = f"Welcome, {user['email']}!"

      # Load issues
      self.refresh_issues()
    except Exception as err:
      anvil.alert(f"❌ Error loading dashboard: {str(err)}")

  def refresh_issues(self):
    """Refresh the issues list"""
    try:
      issues = anvil.server.call('get_teacher_issues')

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
    open_form("ReportIssueForm")

  def refresh_btn_click(self, **event_args):
    """Refresh the dashboard"""
    self.refresh_issues()
    anvil.alert("✅ Dashboard refreshed!")

  def logout_btn_click(self, **event_args):
    """Logout and return to login"""
    anvil.users.logout()
    open_form("LoginForm")