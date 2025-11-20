from ._anvil_designer import ReportIssueFormTemplate
from anvil import open_form
import anvil.server
import anvil

class ReportIssueForm(ReportIssueFormTemplate):
  def __init__(self, user_email=None, **properties):
    self.init_components(**properties)
    self.user_email = user_email
    self.load_form_data()

  def load_form_data(self):
    """Load schools and locations"""
    try:
      schools = anvil.server.call('get_all_schools')
      self.school_dropdown.items = schools
    except Exception as err:
      anvil.alert(f"Error loading schools: {str(err)}")

  def school_dropdown_change(self, **event_args):
    """Load locations when school is selected"""
    try:
      school_id = self.school_dropdown.selected_value
      if school_id:
        locations = anvil.server.call('get_locations_by_school', school_id)
        self.location_dropdown.items = locations
    except Exception as err:
      anvil.alert(f"Error loading locations: {str(err)}")

  def submit_btn_click(self, **event_args):
    """Submit the issue"""
    try:
      title = self.title_box.text.strip()
      description = self.description_box.text.strip()
      urgency = self.urgency_dropdown.selected_value
      location_id = self.location_dropdown.selected_value

      if not all([title, description, urgency, location_id]):
        anvil.alert("Please fill in all fields.")
        return

      result = anvil.server.call('submit_issue', title, description, urgency, location_id, self.user_email)

      if result['success']:
        anvil.alert("✅ Issue submitted successfully!")
        open_form("TeacherDashboard", user_email=self.user_email)
      else:
        anvil.alert(f"❌ {result['message']}")
    except Exception as err:
      anvil.alert(f"❌ Error: {str(err)}")

  def cancel_btn_click(self, **event_args):
    """Cancel and return to dashboard"""
    open_form("TeacherDashboard", user_email=self.user_email)