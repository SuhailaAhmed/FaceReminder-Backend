from django.db import models
from Gp_Backend.s3_storages import MediaStorage

class Profile(models.Model):
    account = models.OneToOneField("accounts.Account", on_delete=models.CASCADE, related_name='profile')
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null =True, blank = True)
    address = models.CharField(max_length=250, null =True, blank = True)
    image = models.ImageField(upload_to='profiles/', storage=MediaStorage, null=True, blank=True)

    def __str__(self) :
        return self.fullname
        


    def __str__(self):
        return self.fullname