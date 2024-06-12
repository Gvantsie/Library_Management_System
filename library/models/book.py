from django.db import models
from django.utils.translation import gettext_lazy as _

from library.choices.cover_choices import COVER_CHOICES
from library.choices.status_choices import STATUS_CHOICES

from library.models.author import Author
from library.models.genre import Genre


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("Author"), related_name='books')
    genre = models.ManyToManyField(Genre, verbose_name=_("Genre"))
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    description = models.TextField(verbose_name=_("Description"))
    stock = models.IntegerField(verbose_name=_("Stock"))
    publication_date = models.DateField(verbose_name=_("Publication Date"))
    cover_type = models.CharField(verbose_name=_("Cover Type"), choices=COVER_CHOICES, max_length=30,
                                  default="hard", null=True)
    cover = models.ImageField(verbose_name=_("Cover"), upload_to='cover', null=True, blank=True)
    status = models.CharField(verbose_name=_("Status"), choices=STATUS_CHOICES, max_length=30,
                              default="available", null=False)
    notified = models.BooleanField(default=False, verbose_name=_("Notified"))

    # New fields to track borrowing history and total copies
    times_borrowed = models.PositiveIntegerField(default=0, verbose_name=_("Times Borrowed"))
    total_copies = models.PositiveIntegerField(default=0, verbose_name=_("Total Copies"))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def is_available(self):
        return self.status == 'available' and self.stock > 0

    def update_borrowing_stats(self, increase=True):
        """Update borrowing statistics for the book."""
        if increase:
            self.times_borrowed += 1
            self.stock -= 1
        else:
            self.stock += 1
        self.save(update_fields=['times_borrowed', 'stock'])
