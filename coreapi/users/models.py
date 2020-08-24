from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    middle_name = models.CharField(_("Middle name"), blank=True, max_length=255)
    photo = ImageField(_("Photo"), upload_to="users/photo")

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
