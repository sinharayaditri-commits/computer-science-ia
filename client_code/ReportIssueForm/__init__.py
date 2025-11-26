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

      # Load schools - with detailed debugging
      print(f"DEBUG: About to call get_all_schools...")
      schools = anvil.server.call('get_all_schools')
      print(f"DEBUG: get_all_schools returned: {schools}")
      print(f"DEBUG: Type: {type(schools)}")
      print(f"DEBUG: Length: {len(schools) if schools else 0}")

      if schools:
        for i, school in enumerate(schools):
          print(f"DEBUG: School {i}: {school}")
        self.school_dropdown.items = schools
        print(f"DEBUG: School dropdown set successfully")
      else:
        print(f"DEBUG: Schools list is empty!")
        self.school_dropdown.items = []

      self.location_dropdown.items = []

    except Exception as err:
      print(f"ERROR in load_form_data: {err}")
      import traceback
      traceback.print_exc()
      anvil.alert(f"Error loading form: {err}")

  def school_dropdown_change(self, **event_args):
    try:
      school_id = self.school_dropdown.selected_value
      print(f"DEBUG: School selected: {school_id}")
      print(f"DEBUG: School type: {type(school_id)}")

      if school_id:
        print(f"DEBUG: About to call get_locations_by_school with: {school_id}")
        locations = anvil.server.call('get_locations_by_school', school_id)
        print(f"DEBUG: Locations returned: {locations}")
        self.location_dropdown.items = locations or []
      else:
        self.location_dropdown.items = []
    except Exception as err:
      print(f"ERROR in school_dropdown_change: {err}")
      import traceback
      traceback. print_exc()
      anvil.alert(f"Error loading locations: {err}")

  def submit_btn_click(self, **event_args):
    try:
      title = (self.title_box.text or "").strip()
      description = (self.description_box. text or "").strip()
      urgency = self.urgency_dropdown.selected_value
      location_id = self.location_dropdown.selected_value

      print(f"DEBUG: Submitting issue - Title: {title}, Urgency: {urgency}, Location: {location_id}")

      if not all([title, description, urgency]):
        anvil.alert("Please fill in title, description and urgency.")
        return

      result = anvil.server.call('submit_issue', title, description, urgency, location_id, self.user_email)
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