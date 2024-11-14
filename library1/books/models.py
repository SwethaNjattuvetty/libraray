from django.db import models

# Create your models here.
class Book(models.Model):
    #Attributes
    title=models.CharField(max_length=20)
    author=models.CharField(max_length=20)
    pages=models.IntegerField()
    price=models.IntegerField()
    Language=models.CharField(max_length=20)
    cover=models.ImageField(upload_to="images")
    pdf=models.FileField(upload_to="pdf")

    def __str__(self):
        return self.title