from ._anvil_designer import AdminDashboardTemplate
import anvil.server
from anvil import open_form
import anvil.users
import anvil

class AdminDashboard(AdminDashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self. load_dashboard()

  def load_dashboard(self):
    """Load admin dashboard"""
    try:
      user = anvil.users.get_user()
      self.load_issues()
    except Exception as err:
      anvil.alert(f"Error loading dashboard: {str(err)}")

  def load_issues(self, filters=None):
    """Load issues with optional filters"""
    try:
      issues = anvil. server.call('get_all_issues', filters)
      self. issues_grid.rows = [
        {
          'title': issue['title'],
          'description': issue['description'],
          'urgency': issue['urgency'],
          'status': issue['status'],
          'location': str(issue['location']),
          'assigned_to': issue['assigned_to'] or 'Unassigned'
        }
        for issue in issues
      ]
    except Exception as err:
      anvil.alert(f"Error loading issues: {str(err)}")

  def logout_btn_click(self, **event_args):
    """Logout"""
    print("DEBUG: Logout button clicked!")
    anvil.alert("Logging you out...")
    anvil.users.logout()
    print("DEBUG: User logged out")
    open_form("LoginForm")
    print("DEBUG: Redirecting to LoginForm")

  def pending_approvals_link_click(self, **event_args):
    """Navigate to admin approval form"""
    open_form("AdminApprovalForm")