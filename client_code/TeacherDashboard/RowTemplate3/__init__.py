from ._anvil_designer import RowTemplate3Template
from anvil import *

class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Display the issue data in each label
    self. title_label.text = self.item.get('title', '')
    self.urgency_label.text = self.item.get('urgency', '')
    self.status_label.text = self.item.get('status', '')
    self.location_label.text = self. item.get('location', '')