from api import routes
from api.api_client import ApiClient


def get_users(client: ApiClient, gender: str = None):
    return client.get(routes.Routes.USERS, params={'gender': gender} if gender else None)


def get_user(client: ApiClient, user_id: str):
    return client.get(routes.Routes.USER.format(user_id))
