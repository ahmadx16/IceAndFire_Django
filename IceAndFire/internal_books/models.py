from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=150)
    isbn = models.CharField(max_length=150)
    # TODO: authors array field
    authors = models.CharField(max_length=150)
    country = models.CharField(max_length=60)
    number_of_pages = models.IntegerField()
    publisher = models.CharField(max_length=150)
    release_date = models.DateField(max_length=150)

    def __str__(self):
        return str(self.name)
