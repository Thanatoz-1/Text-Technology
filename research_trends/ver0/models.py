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


class Conference(models.Model):
    name = models.CharField(max_length=128)
    year = models.IntegerField()
    abbr = models.CharField(max_length=64)

    def __str__(self):
        return self.abbr


class Keyword(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Paper(models.Model):
    title = models.CharField(max_length=1024)
    # the max length so far is less than 5k chars
    abstract = models.TextField(max_length=8092)
    url = models.CharField(max_length=1024, default="")

    conference = models.ForeignKey(
        Conference, on_delete=models.CASCADE, related_name="papers"
    )
    authors = models.ManyToManyField(Author, related_name="papers")
    affiliations = models.ManyToManyField(Affiliation, related_name="papers")
    keys = models.ManyToManyField(Keyword, related_name="papers")

    def __str__(self):
        return self.title
