from django.contrib import admin
from .models import Tag, Transaction, Lead

admin.site.register(Lead)
admin.site.register(Tag)
admin.site.register(Transaction)
