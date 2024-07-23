from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()

    def __str__(self):
        return self.name

class Quote(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.JSONField()

    def __str__(self):
        return f"{self.text[:50]}... - {self.author.name}"
