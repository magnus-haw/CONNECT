from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class EmailList(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    def list(self):
        return list(self.contact_set.values_list('email', flat=True))

class Contact(models.Model):
    emaillist = models.ForeignKey(EmailList, on_delete=models.CASCADE) 
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


