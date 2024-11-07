from django.db import models

class Email(models.Model):
    email_address = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email_address
