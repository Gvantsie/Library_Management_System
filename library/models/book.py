from django.db import models
from django.utils.translation import gettext_lazy as _

from library.choices.cover_choices import COVER_CHOICES
from library.choices.status_choices import STATUS_CHOICES

from library.models.author import Author
from library.models.genre import Genre


# Create your models here.
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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def is_available(self):
        return self.status == 'available' and self.stock > 0
