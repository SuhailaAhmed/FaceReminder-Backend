from django.db import models
from Gp_Backend.s3_storages import MediaStorage

class connection(models.Model):
    account = models.OneToOneField("accounts.Account", on_delete=models.CASCADE, related_name='connection')
    name = models.CharField(max_length=100, null= False)
    image = models.ImageField(upload_to='connection/', storage=MediaStorage, null=True, blank=True)
    age = models.IntegerField(max_length=50, null =False)
    relation = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=200, null= True, blank = True)
    biograghy = models.CharField(max_length=200, null=True, blank = True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self) :
        return self.name