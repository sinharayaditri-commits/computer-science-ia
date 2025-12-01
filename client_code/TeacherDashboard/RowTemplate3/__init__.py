from ._anvil_designer import RowTemplate3Template
from anvil import *

class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Display the data
    self.label_title.text = self.item.get('title', '')
    self.label_urgency.text = self.item. get('urgency', '')
    self. label_status.text = self.item. get('status', '')
    self.label_location.text = self.item.get('location', '')