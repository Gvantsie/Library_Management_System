from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from TBC_final import settings
from library.models.book import Book


# Create your models here.
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"), related_name='reservations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("Book"), related_name='reservations')
    reserved_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Reserved At"))
    status = models.CharField(verbose_name=_("Status"), max_length=20, choices=[('reserved', 'Reserved'), ('canceled', 'Canceled')], default='reserved')

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.email} reserved {self.book.title}"

    def clean(self):
        # Count existing reservations for the user
        existing_reservations_count = Reservation.objects.filter(user=self.user).count()
        if existing_reservations_count >= 3:
            raise ValidationError("You can only reserve up to three books.")

    def cancel(self):
        self.status = 'canceled'
        self.save()

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure model passes validation
        super().save(*args, **kwargs)
