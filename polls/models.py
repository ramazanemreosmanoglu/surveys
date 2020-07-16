from django.db import models
from django.utils.timezone import now
from django.shortcuts import reverse
from django.utils.text import slugify
from accounts.models import User
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    text = models.TextField(verbose_name="Yorum", max_length=200)
    date = models.DateTimeField(default=now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text} - {self.pk}"

    class Meta:
        verbose_name = "Yorumlar"
        ordering = ["-date"]


class VisitorIPAddressModel(models.Model):
    ip = models.GenericIPAddressField("IP Adresi")


class Choice(models.Model):
    text = models.CharField(max_length=200, verbose_name="Metin")
    votes = models.PositiveIntegerField(default=0)
    voters = models.ManyToManyField(User, blank=True)
    visitor_voters = models.ManyToManyField(VisitorIPAddressModel, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Seçenekler"
        verbose_name_plural = "Seçenekler"
            


class Poll(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık", unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now, verbose_name="Tarih")
    explanation = models.TextField(verbose_name="Açıklama", null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False, max_length=130)
    choices = models.ManyToManyField(Choice, verbose_name="Seçenekler")
    comments = models.ManyToManyField(Comment, verbose_name="Yorumlar", blank=True)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("polls:detail", kwargs={"slug": self.slug})

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        return slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Poll, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Anket"
        verbose_name_plural = "Anketler"
        ordering = ["-date"]


class Alert(models.Model):
    title = models.CharField("Başlık", max_length=200)
    url = models.CharField(
        "URL",
        help_text=_(
            'Başında / olmadan URL\'i yazın.'
        ),
        max_length=200
    )

    text = models.CharField('Metin', max_length=500)
    is_active = models.BooleanField("Aktif", default=True)
    def __str__(self):
        if self.title:
            return self.title

        return self.pk
    
    class Meta:
        verbose_name = "Uyarı"
        verbose_name_plural = "Uyarılar"
