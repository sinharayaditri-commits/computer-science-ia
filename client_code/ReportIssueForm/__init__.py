from ._anvil_designer import ReportIssueFormTemplate
import anvil.server
from anvil import open_form
import anvil

class ReportIssueForm(ReportIssueFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_data()

  def load_data(self):
    """Load schools and urgency options"""
    try:
      # Set urgency options
      self.urgency_drop.items = ["Low", "Medium", "High", "Critical"]
      self.urgency_drop.selected_value = "Medium"

      # Load schools
      schools = anvil.server.call('get_all_schools')
      self.location_drop.items = schools

      if schools:
        self.location_drop.selected_value = schools[0][0]
    except Exception as err:
      anvil.alert(f"❌ Error loading data: {str(err)}")

  def submit_btn_click(self, **event_args):
    """Submit the issue"""
    title = self.title_box.text.strip()
    description = self.desc_area.text.strip()
    urgency = self.urgency_drop.selected_value
    location_id = self.location_drop.selected_value

    # Validation
    if not title or not description:
      anvil.alert("❌ Please fill in title and description.")
      return

    if not urgency or not location_id:
      anvil.alert("❌ Please select urgency and location.")
      return

      # Submit via server
    result = anvil.server.call(
      'submit_issue',
      title,
      description,
      urgency,
      location_id
    )

    if result['success']:
      anvil.alert("✅ " + result['message'])
      self.clear_form()
      open_form("TeacherDashboard")
    else:
      anvil.alert("❌ " + result['message'])

  def clear_form(self):
    """Clear all fields"""
    self.title_box.text = ""
    self.desc_area.text = ""
    self.urgency_drop.selected_value = "Medium"