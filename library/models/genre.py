from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Genre(models.Model):
    genre_name = models.CharField(verbose_name=_("Genre Name"), max_length=50)

    def __str__(self):
        return self.genre_name

    class Meta:
        verbose_name = _("Genre Name")
        verbose_name_plural = _("Genre Names")
