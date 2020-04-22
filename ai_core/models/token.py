from django.db import models

from ai_django.ai_core.utils.shortcuts import generate_unique_code


class TokenModel(models.Model):
    _token_length = 8

    code = models.CharField(blank=False, max_length=_token_length)

    def save(self, *args, **kwargs):
        if not self.id:
            # Set code on creation
            self.code = generate_unique_code(length=self._token_length)
        return super(TokenModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
