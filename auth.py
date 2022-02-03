from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope


def authenticate(user):
    target_scope = [AuthScope.BITS_READ]
    auth = UserAuthenticator(user, target_scope, force_verify=False)
    token, refresh_token = auth.authenticate()
    user.set_user_authentication(token, target_scope, refresh_token)
