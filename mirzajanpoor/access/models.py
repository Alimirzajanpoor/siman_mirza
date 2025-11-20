from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from core.models import AbstractModel
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, password, **kwargs):
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password, **kwargs):
        kwargs["is_admin"] = False
        return self._create_user(password, **kwargs)

    def create_superuser(self, password, **kwargs):
        kwargs["is_admin"] = True
        return self._create_user(password, **kwargs)


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        _(
            "Phone number",
        ),
        max_length=11,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(_("First Name"), max_length=32, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=64, blank=True)
    is_active = models.BooleanField(
        _("Active"), help_text=_("their account is active or not"), default=True
    )
    is_admin = models.BooleanField(
        _("Admin"),
        help_text="whether the use can log into admin site or not",
        default=False,
    )
    USERNAME_FIELD = "phone_number"
    objects = UserManager()

    def __str__(self):
        return f"{self.phone_number} , {self.first_name}"

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_admin

    def has_module_perms(self, app_label):
        return self.is_active and self.is_admin

    def get_all_permissions(self, obj=None):
        return []

    class Meta(AbstractModel.Meta):
        verbose_name = _("User")
        verbose_name_plural = _("Users")
