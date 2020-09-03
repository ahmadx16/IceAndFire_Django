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
    number_of_pages = models.PositiveIntegerField()
    publisher = models.CharField(max_length=150)
    release_date = models.DateField(max_length=150)

    def __str__(self):
        return str(self.name)


def update_authors(updated_authors, book):
    """Updates authors of a given book instance."""

    if not updated_authors:
        return
    updated_authors = [author["name"] for author in updated_authors]
    authors = list(book.authors.all())
    # clear previous authors reference to book
    book.authors.clear()
    find_remove_extra_authors(authors)
    # create new authors referencing to same book
    new_book_authors(book, updated_authors)


def new_book_authors(book, new_authors):
    """Adds new book authors if not in database."""

    for author in new_authors:
        author_instance, _ = Author.objects.get_or_create(name=author)
        book.authors.add(author_instance)


def find_remove_extra_authors(authors):
    """Finds and Removes given authors with no books from database."""

    for author in authors:
        if not author.author_books.count():
            author.delete()
