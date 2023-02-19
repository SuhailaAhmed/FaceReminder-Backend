from django.db import models
import uuid

class AccountToken(models.Model):
    account = models.OneToOneField('accounts.Account', on_delete=models.CASCADE, related_name='token')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uuid)