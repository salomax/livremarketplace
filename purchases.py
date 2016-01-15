from datetime import datetime
from protorpc import messages
from protorpc import message_types

class Purchase(messages.Message):
  """Purchase that stores a message."""
  name = messages.StringField(1)
  quantity = messages.IntegerField(2, required=True)
  date_purchase = message_types.DateTimeField(3, required=True)


class PurchaseCollection(messages.Message):
  """Collection of purchases."""
  items = messages.MessageField(Purchase, 1, repeated=True)

def get_purchases():
  return PurchaseCollection(items=[Purchase(name='teste', quantity=1, date_purchase=datetime.now())])