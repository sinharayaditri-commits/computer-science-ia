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
    try:
      # Set urgency dropdown
      self.urgency_dropdown.items = ["Low", "Medium", "High"]

      # Load schools
      schools = anvil.server.call('get_all_schools')
      self.school_dropdown. items = schools or []
      self.location_dropdown.items = []

      print(f"DEBUG: Loaded schools: {schools}")
    except Exception as err:
      anvil.alert(f"Error loading form: {err}")
      print(f"ERROR: {err}")

  def school_dropdown_change(self, **event_args):
    try:
      school_id = self.school_dropdown.selected_value
      print(f"DEBUG: School selected: {school_id}")
      if school_id:
        locations = anvil.server.call('get_locations_by_school', school_id)
        print(f"DEBUG: Locations for school: {locations}")
        self.location_dropdown.items = locations or []
      else:
        self.location_dropdown.items = []
    except Exception as err:
      anvil.alert(f"Error loading locations: {err}")
      print(f"ERROR: {err}")

  def submit_btn_click(self, **event_args):
    try:
      title = (self.title_box.text or ""). strip()
      description = (self.description_box.text or "").strip()
      urgency = self.urgency_dropdown.selected_value
      location_id = self.location_dropdown. selected_value

      print(f"DEBUG: Submitting issue - Title: {title}, Urgency: {urgency}, Location: {location_id}")

      if not all([title, description, urgency]):
        anvil.alert("Please fill in title, description and urgency.")
        return

      result = anvil.server.call('submit_issue', title, description, urgency, location_id, self.user_email)
      if result. get('success'):
        anvil. alert("Issue submitted!")
        open_form("TeacherDashboard", user_email=self.user_email)
      else:
        anvil.alert(result.get('message') or "Failed to submit issue.")
    except Exception as err:
      anvil. alert(f"Error: {err}")
      print(f"ERROR: {err}")

  def cancel_btn_click(self, **event_args):
    open_form("TeacherDashboard", user_email=self. user_email)