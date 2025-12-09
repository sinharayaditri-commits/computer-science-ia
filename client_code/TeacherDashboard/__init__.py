from ._anvil_designer import TeacherDashboardTemplate
from anvil import open_form
import anvil.server
import anvil
import anvil.users

class TeacherDashboard(TeacherDashboardTemplate):
  def __init__(self, user_email=None, **properties):
    self.init_components(**properties)

    if not user_email: 
      user = anvil.users. get_user()
      if user:
        user_email = user['email']

    self.user_email = user_email
    self.issues = []  # Store all issues
    self. current_index = 0  # Track which issue we're viewing

    self.load_dashboard()

  def load_dashboard(self):
    try:
      if not self.user_email:
        anvil.alert("User not found.  Please log in again.")
        open_form("LoginForm")
        return

      self.welcome_label.text = f"Welcome, {self. user_email}!"
      self.refresh_issues()
    except Exception as e:
      anvil.alert(f"Error loading dashboard: {e}")

  def refresh_issues(self):
    try:
      self. issues = anvil.server.call('get_teacher_issues', self. user_email)
      self.current_index = 0
      self.display_current_issue()
    except Exception as e: 
      print(f"ERROR:  {e}")
      anvil.alert(f"Error loading issues: {e}")

  def display_current_issue(self):
    """Display the current issue in the card"""
    if not self.issues:
      # No issues - show empty state
      self. title_label.text = "No issues found"
      self. urgency_label. text = ""
      self.status_label.text = ""
      self. location_label.text = ""
      self.description_label. text = ""
      self.issue_counter_label. text = "0 of 0"
      self.previous_btn. enabled = False
      self.next_btn. enabled = False
      return

      # Get current issue
    issue = self.issues[self.current_index]

    # Display the data
    self.title_label.text = issue. get('title', '')
    self.urgency_label.text = f"Urgency:  {issue.get('urgency', '')}"
    self. status_label.text = f"Status: {issue.get('status', '')}"
    self.location_label. text = f"Location: {issue.get('location', '')}"
    self.description_label.text = issue.get('description', '')

    # Update counter
    self.issue_counter_label. text = f"Issue {self.current_index + 1} of {len(self.issues)}"

    # Enable/disable buttons
    self.previous_btn.enabled = self. current_index > 0
    self. next_btn.enabled = self.current_index < len(self.issues) - 1

  def previous_btn_click(self, **event_args):
    """Go to previous issue"""
    if self.current_index > 0:
      self.current_index -= 1
      self.display_current_issue()

  def next_btn_click(self, **event_args):
    """Go to next issue"""
    if self.current_index < len(self.issues) - 1:
      self.current_index += 1
      self.display_current_issue()

  def report_new_issue_btn_click(self, **event_args):
    open_form("ReportIssueForm", user_email=self. user_email)

  def refresh_btn_click(self, **event_args):
    self.refresh_issues()

  def logout_click(self, **event_args):
    anvil.users.logout()
    open_form("LoginForm")