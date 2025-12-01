from ._anvil_designer import issues_grid_row_templateTemplate
from anvil import *

class issues_grid_row_template(issues_grid_row_templateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Only include the fields your server function returns
    self.title_label. text = self.item. get('title', '')
    self.description_label.text = self.item.get('description', '')
    self.urgency_label.text = self.item.get('urgency', '')
    self.status_label.text = self.item.get('status', '')
    self.created_at_label.text = str(self.item. get('created_at', ''))
    self.location_label.text = self.item.get('location', '')