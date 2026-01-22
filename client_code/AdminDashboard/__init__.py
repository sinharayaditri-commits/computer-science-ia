from ._anvil_designer import AdminDashboardTemplate
import anvil.server
from anvil import open_form
import anvil.users
import anvil

class AdminDashboard(AdminDashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_dashboard()

  def load_dashboard(self):
    """Load admin dashboard"""
    try:
      self.label_1. text = "Welcome, Admin"
      print(f"DEBUG: Welcome label set")
      self.load_issues()
    except Exception as err:
      anvil.alert(f"Error loading dashboard: {str(err)}")
      print(f"DEBUG: Error in load_dashboard: {err}")
      import traceback
      traceback.print_exc()

  def load_issues(self):
    """Load issues and populate the Repeating Panel"""
    try: 
      print("DEBUG:   Calling get_all_issues()...")
      issues = anvil.server.call('get_all_issues')
      print(f"DEBUG:  Received {len(issues)} issues from server")

      if not issues or len(issues) == 0:
        print("DEBUG: No issues found in database")
        self.repeating_panel_1.items = []
        return

      # Set items on repeating panel - let data bindings handle display
      self.repeating_panel_1.items = issues
      print(f"DEBUG: Successfully loaded {len(issues)} items into Repeating Panel")

    except Exception as err:
      anvil.alert(f"Error loading issues: {str(err)}")
      print(f"DEBUG: Error loading issues: {err}")
      import traceback
      traceback.print_exc()
      
  def logout_btn_click(self, **event_args):
    """Logout"""
    print("DEBUG: Logout button clicked!")
    anvil.alert("Logging you out...")
    anvil.users.logout()
    open_form("LoginForm")

  @anvil.handle("pending_approvals_link", "click")
  def pending_approvals_link_click(self, **event_args):
    """Navigate to admin approval form"""
    open_form("AdminApprovalForm")