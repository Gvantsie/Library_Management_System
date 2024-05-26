from django.db import models
from django.utils.translation import gettext_lazy as _
from TBC_final import settings


class UserStatistics(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"), related_name="stats")
    books_read = models.IntegerField(default=0, verbose_name=_("Books Read"))
    books_reserved = models.IntegerField(default=0, verbose_name=_("Books Reserved"))

    def __str__(self):
        return f"{self.user.email} stats"

    class Meta:
        verbose_name = _("User Statistics")
        verbose_name_plural = _("User Statistics")
