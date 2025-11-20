from ._anvil_designer import AdminApprovalFormTemplate
import anvil.server
from anvil import open_form
import anvil

class AdminApprovalForm(AdminApprovalFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_pending_admins()

  def load_pending_admins(self):
    try:
      pending = anvil.server.call('get_pending_admins')
      self.data_grid_1.rows = pending
    except Exception as err:
      anvil.alert(f"Error: {str(err)}")

  def approve_btn_click(self, **event_args):
    selected = self.data_grid_1.selected_row
    if not selected:
      anvil.alert("Please select an admin to approve")
      return
    result = anvil.server.call('approve_admin_account', selected['email'])
    if result['success']:
      anvil.alert("Admin approved!")
      self.load_pending_admins()
    else:
      anvil.alert(f"Error: {result['message']}")

  def reject_btn_click(self, **event_args):
    selected = self.data_grid_1.selected_row
    if not selected:
      anvil.alert("Please select an admin to reject")
      return
    result = anvil.server.call('reject_admin_account', selected['email'])
    if result['success']:
      anvil.alert("Admin rejected!")
      self.load_pending_admins()
    else:
      anvil.alert(f"Error: {result['message']}")

  def continue_to_dashboard_btn_click(self, **event_args):
    open_form("AdminDashboard")