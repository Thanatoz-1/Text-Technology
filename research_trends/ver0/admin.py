from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Author)
admin.site.register(Affiliation)
admin.site.register(Conference)
admin.site.register(Keyword)
admin.site.register(Paper)
