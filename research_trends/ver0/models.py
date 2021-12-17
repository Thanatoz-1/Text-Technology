from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Affiliation(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

class Keyword(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=4096)

    def __str__(self):
        return self.name

class Paper(models.Model):
    title = models.CharField(max_length=512)
    abstract = models.CharField(max_length=65536)
    authors = models.ManyToManyField(Author, related_name="papers")
    affliations = models.ManyToManyField(Affiliation, related_name="paper")
    keywords = models.ManyToManyField(Keyword, blank=True, related_name="papers")

    def __str__(self):
        return f'Title: {self.title}\nAbstract: {self.abstract}'
