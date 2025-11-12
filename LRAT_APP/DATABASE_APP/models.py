from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    expected_grad_year = models.IntegerField(null=True, blank=True)

class Software(models.Model):
    software_id = models.AutoField(primary_key=True)
    subscription_name = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.IntegerField()
    license_start = models.DateField(null=True, blank=True)
    license_end = models.DateField(null=True, blank=True)
    help_page = models.URLField(max_length=300, blank=True, null=True)
    uninstall_instructions = models.URLField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subscription_name

class SoftwareOption(models.Model):
    software = models.ForeignKey(
        Software, on_delete=models.CASCADE, related_name="options"
    )
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        unique_together = ("software", "name")

    def __str__(self):
        return self.name

class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    currently_used = models.BooleanField(default=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    date_expired = models.DateTimeField(null=True, blank=True)
    renew = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="subscriptions")
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name="subscriptions")
    option = models.ForeignKey(
        SoftwareOption,
        on_delete=models.SET_NULL,
        related_name="subscriptions",
        null=True,
        blank=True,
    )
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def compute_total_cost(self):
        if self.option:
            return self.option.cost or Decimal("0.00")
        if self.software:
            return self.software.cost or Decimal("0.00")
        return Decimal("0.00")

    def save(self, *args, **kwargs):
        self.total_cost = self.compute_total_cost()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.option:
            return self.option.name
        return self.software.subscription_name