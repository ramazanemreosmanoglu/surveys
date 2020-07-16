from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


from .models import Poll

class IndexSitemap(Sitemap):
    changefreq = "yearly"
    priority = 1.0

    def items(self):
        return [
            "home",
        ]

    def location(self, obj):
        return reverse(obj)


class AuthSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.7

    def items(self):
        return [
            "accounts:register",
            "accounts:login",
        ]

    def location(self, obj):
        return reverse(obj)

class Poll_Sitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return Poll.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.date