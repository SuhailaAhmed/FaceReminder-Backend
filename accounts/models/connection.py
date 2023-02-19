from django.db import models
from Gp_Backend.s3_storages import MediaStorage


class Connection(models.Model):
    account = models.ForeignKey("accounts.Account", on_delete=models.CASCADE, related_name="connections")
    image = models.ImageField(upload_to="connection/", storage=MediaStorage)
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=100)
    age = models.IntegerField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    biograghy = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name