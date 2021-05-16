from django.db import models

# Create your models here.


class BaseModel(models.Model):
    """Base model class"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
