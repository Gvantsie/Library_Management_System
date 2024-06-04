from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from TBC_final import settings
from library.models.book import Book


class BookTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=_("transactions"))
    book = models.ForeignKey(to='library.book', on_delete=models.CASCADE, related_name=_("transactions"))
    borrowed_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Borrowed At"))
    returned_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Returned At"))

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    class Meta:
        verbose_name = _("Book Transaction")
        verbose_name_plural = _("Book Transactions")
