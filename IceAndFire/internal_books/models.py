from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=150)
    isbn = models.CharField(max_length=150)
    country = models.CharField(max_length=60)
    number_of_pages = models.IntegerField()
    publisher = models.CharField(max_length=150)
    release_date = models.DateField(max_length=150)

    def __str__(self):
        return str(self.name)


class Author(models.Model):
    book = models.ForeignKey(Book, default=1, related_name="authors", on_delete=models.CASCADE)
    name = models.CharField(max_length=150, primary_key=True)

    def __str__(self):
        return str(self.name)
