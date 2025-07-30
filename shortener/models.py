from django.db import models
from django.utils.crypto import get_random_string


class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    custom_code = models.CharField(max_length=10, blank=True, null=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.custom_code and not self.short_code:
            self.short_code = get_random_string(6)
        super().save(*args, **kwargs)

    @property
    def final_code(self):
        return self.custom_code if self.custom_code else self.short_code

    def __str__(self):
        return self.original_url
