import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    date_create = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=500)


class History(Base):
    action = models.TextField()
    result = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
