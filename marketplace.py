"""
MarketPlace API
"""
import endpoints
import purchases

from protorpc import message_types
from protorpc import remote

@endpoints.api(name='marketplace', version='v1')
class MarketPlaceApi(remote.Service):
  """MarketPlace API v1."""

  @endpoints.method(message_types.VoidMessage, 
                    purchases.PurchaseCollection,
                    path='marketplace', 
                    http_method='GET',
                    name='purchases.list')
  def purchases_list(self, unused_request):
    """
    List purchases stored to logged user.
    """
    return purchases.get_purchases()

# Creating api server to bind in app.yaml
APPLICATION = endpoints.api_server([MarketPlaceApi])
