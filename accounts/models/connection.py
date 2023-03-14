from django.db import models

from Gp_Backend.s3_storages import MediaStorage


def get_image_path(instance, filename):
    # Get the account id from the instance
    account_id = instance.account.id
    # Return the full path to the image file
    return f"connections/{account_id}/{filename}"


class Connection(models.Model):
    account = models.ForeignKey("accounts.Account", on_delete=models.CASCADE, related_name="connections")
    image = models.ImageField(upload_to=get_image_path, storage=MediaStorage)
    name = models.CharField(max_length=100, null=True, blank=True)
    relation = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    biography = models.CharField(max_length=4000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Connection_" + self.id
