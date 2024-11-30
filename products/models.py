from django.db import models
import uuid
from django.urls import reverse


class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank = True)
    image = models.ImageField(upload_to = 'category', blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to = 'product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id])

    def __str__(self):
        return self.name