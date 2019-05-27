from django.db import models
from django.conf import settings
import uuid

USER_MODEL = settings.AUTH_USER_MODEL


class HashUserToken(models.Model):
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    variable_2fa = models.CharField(max_length=128)

    def __str__(self):
        return "{} - {} - {}".format(self.user.__str__,
                                     self.uuid, self.variable_2fa)
