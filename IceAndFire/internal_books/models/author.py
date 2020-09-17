from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return str(self.name)

    def remove_extra_author(self):
        """Removes an author with no books from database."""

        if not self.author_books.count():
            self.delete()
