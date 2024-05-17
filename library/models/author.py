from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(verbose_name=_("First Name"), max_length=100)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=255)
    date_of_birth = models.DateField(verbose_name=_("Date of Birth"))
    date_of_death = models.DateField(verbose_name=_("Date of Death"), null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")
