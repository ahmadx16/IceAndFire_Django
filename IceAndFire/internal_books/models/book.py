from django.db import models
from .author import Author

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

    def update_authors(self, updated_authors):
        """Updates authors of a given book instance."""

        if not updated_authors:
            return
        updated_authors = [author["name"] for author in updated_authors]
        authors = list(self.authors.all())
        # clear previous authors reference to book
        self.authors.clear()
        # create new authors referencing to same book
        self.new_book_authors(updated_authors)
        self.find_remove_extra_authors(authors)

    def new_book_authors(self, new_authors):
        """Adds new book authors if not in database."""

        for author in new_authors:
            author_instance, _ = Author.objects.get_or_create(name=author)
            self.authors.add(author_instance)

    def find_remove_extra_authors(self, authors):
        """Finds and Removes given authors with no books from database."""

        for author in authors:
            author.remove_extra_author()
