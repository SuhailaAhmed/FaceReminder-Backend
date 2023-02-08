from django.db import models

# Create your models here.
class Profile(models.Model):
    account = models.OneToOneField('accounts.Account', on_delete=models.CASCADE, related_name='profile')
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    image = models.URLField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.fullname