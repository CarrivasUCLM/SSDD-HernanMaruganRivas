import Ice
Ice.loadSlice('iceflix.ice')

import IceFlix


class AuthenticatorI(IceFlix.Authenticator):
    def getAuthenticator(self):

class MediaCatalogI(IceFlix.MediaCatalog):
    def getCatalogService(self):
