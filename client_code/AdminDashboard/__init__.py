from ._anvil_designer import AdminDashboardTemplate
from anvil.tables import app_tables
import anvil

class AdminDashboard(AdminDashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.refresh_issues()

  def refresh_issues(self):
    issue_rows = app_tables.issues.search()
    issues_list = []
    for issue in issue_rows:
      # Get linked location details
      loc = issue['location']
      loc_text = ""
      if loc is not None:
        loc_text = f"{loc['branch']} / {loc['floor']} / {loc['room']}"
      # Get assigned_to name
      assigned_to = issue['assigned_to']
      assigned_name = assigned_to['name'] if assigned_to is not None else "Unassigned"
      issues_list.append({
        'title': issue['title'],
        'description': issue['description'],
        'urgency': issue['urgency'],
        'status': issue['status'],
        'location': loc_text,
        'assigned_to': assigned_name,
        'issue_id': issue.get_id()  # Unique ID for lookup!
      })
    self.issues_grid.items = issues_list

  def assign_btn_click(self, **event_args):
    """
    This code runs when you click the Assign button in a row.
    """
    issue = self.item  # This is the issue dictionary for the row you clicked
    users = app_tables.users.search()
    user_names = [user['name'] for user in users]
    selected_user_name = anvil.alert("Select a user to assign this issue:", buttons=user_names)
    if selected_user_name:
      selected_user = next(user for user in users if user['name'] == selected_user_name)
      # Find the actual issue row by its unique ID
      issue_row = app_tables.issues.get_by_id(issue['issue_id'])
      if issue_row:
        issue_row.update(assigned_to=selected_user)
        anvil.alert("Issue assigned successfully!")
        self.refresh_issues()  # Refresh the grid after assigning