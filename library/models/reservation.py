from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from TBC_final import settings
from library.models.book import Book


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    reserved_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='reserved')
    returned = models.BooleanField(verbose_name=_("Returned"), default=False)
    due_date = models.DateField(verbose_name=_("Due Date"), null=True, blank=True)
    return_date = models.DateField(verbose_name=_("Return Date"), null=True, blank=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.email} reserved {self.book.title}"

    def clean(self):
        # Limit user to 3 active reservations
        existing_reservations_count = Reservation.objects.filter(user=self.user, status='reserved').count()
        if existing_reservations_count >= 3:
            raise ValidationError("You can only reserve up to three books.")

        # Set due_date to 1 week after reserved_at if not already set
        if not self.due_date:
            self.due_date = self.reserved_at + timedelta(days=7)

    def is_late(self):
        if self.return_date:
            return self.return_date > self.due_date
        return False

    def cancel(self):
        self.status = 'canceled'
        self.save()

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure model passes validation
        super().save(*args, **kwargs)


@receiver(post_save, sender=Reservation)
def update_book_stats_on_reservation(sender, instance, created, **kwargs):
    """Update book stats when a reservation is made."""
    if created and instance.status == 'reserved':
        instance.book.update_borrowing_stats(increase=True)


@receiver(post_delete, sender=Reservation)
def update_book_stats_on_reservation_cancel(sender, instance, **kwargs):
    """Update book stats when a reservation is canceled."""
    if instance.status == 'reserved':
        instance.book.update_borrowing_stats(increase=False)
