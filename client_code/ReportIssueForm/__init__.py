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
      print(f"DEBUG: Urgency dropdown set")

      # Load schools
      print(f"DEBUG: About to call get_all_schools...")
      schools = anvil.server.call('get_all_schools')
      print(f"DEBUG: get_all_schools returned: {schools}")

      if schools:
        self.school_dropdown.items = schools
        print(f"DEBUG: School dropdown set successfully")
      else:
        print(f"DEBUG: Schools list is empty!")
        self. school_dropdown.items = []

      self.location_dropdown.items = []

    except Exception as err:
      print(f"ERROR in load_form_data: {err}")
      anvil.alert(f"Error loading form: {err}")

  def school_dropdown_change(self, **event_args):
    """This is called when school dropdown selection changes"""
    try:
      school_row = self.school_dropdown.selected_value
      print(f"DEBUG: school_dropdown_change triggered")
      print(f"DEBUG: School selected: {school_row}")

      if school_row:
        print(f"DEBUG: About to call get_locations_by_school...")
        locations = anvil.server. call('get_locations_by_school', school_row)
        print(f"DEBUG: Locations returned: {locations}")
        self.location_dropdown.items = locations or []
        print(f"DEBUG: Location dropdown set with {len(locations)} items")
      else:
        print(f"DEBUG: No school selected")
        self.location_dropdown.items = []
    except Exception as err:
      print(f"ERROR in school_dropdown_change: {err}")
      anvil.alert(f"Error loading locations: {err}")

  def location_dropdown_change(self, **event_args):
    """This method is called when an item is selected in location dropdown"""
    print(f"DEBUG: Location selected: {self.location_dropdown.selected_value}")

  def submit_btn_click(self, **event_args):
    try:
      title = (self.title_box.text or "").strip()
      description = (self.description_box. text or "").strip()
      urgency = self.urgency_dropdown.selected_value
      location_id = self.location_dropdown. selected_value

      print(f"DEBUG: Submitting issue - Title: {title}, Urgency: {urgency}, Location: {location_id}")

      if not all([title, description, urgency]):
        anvil. alert("Please fill in title, description and urgency.")
        return

      result = anvil.server. call('submit_issue', title, description, urgency, location_id, self.user_email)
      if result. get('success'):
        anvil.alert("Issue submitted!")
        open_form("TeacherDashboard", user_email=self.user_email)
      else:
        anvil.alert(result.get('message') or "Failed to submit issue.")
    except Exception as err:
      anvil.alert(f"Error: {err}")
      print(f"ERROR: {err}")

  def cancel_btn_click(self, **event_args):
    open_form("TeacherDashboard", user_email=self. user_email)