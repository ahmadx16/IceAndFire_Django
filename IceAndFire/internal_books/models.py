from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    name = models.CharField(max_length=150)
    isbn = models.CharField(max_length=150)
    country = models.CharField(max_length=60)
    authors = models.ManyToManyField(Author, related_name='author_books')
    number_of_pages = models.IntegerField()
    publisher = models.CharField(max_length=150)
    release_date = models.DateField(max_length=150)

    def __str__(self):
        return str(self.name)


def update_authors(updated_authors, book):
    """Updates authors of a given book instance."""

    if not updated_authors:
        return
    updated_authors = [author["name"] for author in updated_authors]
    # clear previous authors reference to book
    book.authors.clear()
    # create new authors referencing to same book
    new_book_authors(book, updated_authors)


def new_book_authors(book, new_authors):
    """Adds new book authors if not in database."""

    for author in new_authors:
        author_instance, _ = Author.objects.get_or_create(name=author)
        book.authors.add(author_instance)
