from django.db import models
from Gp_Backend.s3_storages import MediaStorage

def get_image_path(instance, filename):
    # Get the account id from the instance
    account_id = instance.account.id
    # Return the full path to the image file
    return f'connections/{account_id}/{filename}'

class Connection(models.Model):
    account = models.ForeignKey("accounts.Account", on_delete=models.CASCADE, related_name="connections")
    image = models.ImageField(upload_to=get_image_path, storage=MediaStorage)
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    biograghy = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name