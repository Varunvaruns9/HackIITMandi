from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .choices import Organs, Groups, RH
from multiselectfield import MultiSelectField


class UserManager(BaseUserManager):
	"""Define a model manager for User model with no username field."""

	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""Create and save a User with the given email and password."""
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		"""Create and save a regular User with the given email and password."""
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		"""Create and save a SuperUser with the given email and password."""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/reports/user_<id>/<filename>
    return 'reports/user_{0}/{1}'.format(instance.email, filename)


class User(AbstractUser):
	username = None
	email = models.EmailField(_('email address'), unique=True)
	donor = models.BooleanField(default=True)
	organs = MultiSelectField(choices=Organs)
	bloodgroup = models.IntegerField(choices=Groups, blank=True, null=True)
	rh = models.IntegerField(choices=RH, blank=True, null=True)
	ailment = models.BooleanField(default=False, blank=True, null=True)
	report = models.FileField(upload_to=user_directory_path)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()
