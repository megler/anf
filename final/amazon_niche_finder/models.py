from tkinter import CASCADE
from typing import cast
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name}"


class Category(MPTTModel):
    cat_id = models.IntegerField(null=False, name="cat_id")
    cat_name = models.CharField(max_length=100,
                                null=False,
                                name="cat_name",
                                default="")
    cat_parent_id = models.IntegerField(null=False, name="cat_parent_id")
    cat_level = models.IntegerField(null=False, name="cat_level")
    cat_link = models.URLField(null=True, name="cat_link")
    cat_bestsellers_link = models.URLField(null=True,
                                           name="cat_bestsellers_link")
    parent = TreeForeignKey("self",
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name="children")

    def __str__(self):
        return f"{self.cat_name}"

    class MPTTMeta:
        order_insertion_by = ["cat_name"]
