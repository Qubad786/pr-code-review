from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, full_name, access_token, password=None):
        """
        Creates and saves a User with the given parameters.
        :param username: string
        :param full_name: string
        :param access_token: string
        :param password: string
        :return: User
        """
        user = self.model(
            username=username,
            full_name=full_name,
            access_token=access_token,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, full_name, access_token, password):
        """
        Creates and saves a super User with the given parameters.
        :param username: string
        :param full_name: string
        :param access_token: string
        :param password: string
        :return: User
        """
        user = self.create_user(
            username=username,
            full_name=full_name,
            access_token=access_token,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    """
    A fully featured User model that uses github username as the username field.
    """
    username = models.CharField(verbose_name=_('user name'), max_length=255, unique=True)
    full_name = models.CharField(verbose_name=_('full name'), max_length=255)
    access_token = models.CharField(verbose_name=_('access token'), max_length=255, unique=True)

    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_admin = models.BooleanField(
        verbose_name=_('admin status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.full_name

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return self.full_name

    def get_short_name(self):
        """
        Returns full name as we don't have first name alone.
        """
        return self.full_name

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        Simplest possible answer: All admins are staff
        """
        return self.is_admin
