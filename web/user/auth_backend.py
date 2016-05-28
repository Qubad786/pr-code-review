from github import Github
from web.user.models import User


class UserAuthenticationBackend(object):

    # noinspection PyMethodMayBeStatic
    def authenticate(self, access_token):
        """
        Authenticates user if it already exists otherwise creates new user.
        :param access_token: string
        """
        github_auth_user = Github(access_token).get_user()

        try:
            user = User.objects.get(username=github_auth_user.login)
            user.access_token = access_token
            user.save()
        except User.DoesNotExist:
            # Create new user if it does not exist already.
            user = User.objects.create_user(
                username=github_auth_user.login,
                full_name=github_auth_user.name,
                access_token=access_token,
            )

        return user

    # noinspection PyMethodMayBeStatic
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
