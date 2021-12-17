from django.contrib import admin
from .models import Paper, Author, Affiliation, Keyword
# Register your models here.
admin.site.register(Paper)
admin.site.register(Author)
admin.site.register(Affiliation)
admin.site.register(Keyword)