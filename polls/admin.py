from django.contrib import admin
from .models import Poll, Choice, Comment, Alert, VisitorIPAddressModel

admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Comment)
admin.site.register(Alert)
admin.site.register(VisitorIPAddressModel)
