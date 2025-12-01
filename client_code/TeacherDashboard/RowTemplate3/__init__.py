from ._anvil_designer import RowTemplate3Template
from anvil import *

class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # DEBUG - Is this even running?
    print(f"ROW TEMPLATE: Loading row with data: {self.item}")

    self.title_label. text = self.item.get('title', '')
    self.urgency_label.text = self.item. get('urgency', '')
    self. status_label.text = self.item. get('status', '')
    self.location_label.text = self.item.get('location', '')

    print(f"ROW TEMPLATE: Set labels successfully!")