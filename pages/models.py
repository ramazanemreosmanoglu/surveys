"""
Site Sayfaları için model.
"""

from django.db import models
from ckeditor.fields import RichTextField

class Page(models.Model):
    name = models.CharField(max_length=200, verbose_name="Sayfa Adı")
    url = models.CharField(verbose_name="Sayfa Url'i", max_length=200)
    is_it_in_navbar = models.BooleanField(default=False, verbose_name="Navbar'da linki olacak mı?")
    page_content = RichTextField(verbose_name="Sayfa İçeriği")

    def __str__(self):
        return self.name
