from django.db import models

# Create your models here.

# Contact Us
class Contact_us(models.Model):
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email