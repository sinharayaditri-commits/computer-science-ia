from ._anvil_designer import report_issue_formTemplate
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.users
import anvil.server

class report_issue_form(report_issue_formTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Set urgency options
    self.urgency_drop.items = ["High", "Medium", "Low"]

    # Populate location dropdown with all locations
    locations = app_tables.location.search()
    self.location_drop.items = [
      (f"{loc['branch']} - Floor {loc['floor']} - Room {loc['room']}", loc)
      for loc in locations
    ]

  def submit_btn_click(self, **event_args):
    # Get current user
    user = anvil.users.get_user()
    if not user:
      alert("Please log in to report an issue.")
      return

      # Get form values
    title = self.title_box.text
    description = self.desc_area.text
    urgency = self.urgency_drop.selected_value
    location = self.location_drop.selected_value

    # Basic validation
    if not title or not description or not urgency or not location:
      alert("Please fill in all fields.")
      return

      # Add the issue to the database
    app_tables.issues.add_row(
      title=title,
      description=description,
      urgency=urgency,
      status="Open",
      created_by=user,
      location=location,
      created_at=anvil.server.now()
    )

    alert("Issue reported successfully!")
    # Optionally clear form or navigate away
    self.title_box.text = ""
    self.desc_area.text = ""
    self.urgency_drop.selected_value = None
    self.location_drop.selected_value = None