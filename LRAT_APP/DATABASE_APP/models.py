from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from datetime import date, datetime
from django.utils import timezone

class DatabaseGroup(Group):
    class Meta:
        proxy = True
        app_label = "DATABASE_APP"
        verbose_name = "Group"
        verbose_name_plural = "Groups"

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

    def _expiry_date(self):
        """
        Always return a date object (not datetime).
        """
        if not self.date_expired:
            return None

        expiry = self.date_expired

        # Convert datetime to date
        if isinstance(expiry, datetime):
            if timezone.is_aware(expiry):
                return timezone.localtime(expiry).date()
            return expiry.date()

        return expiry

    @property
    def days_remaining(self):
        expiry = self._expiry_date()
        if not expiry:
            return None

        today = timezone.localdate()
        return (expiry - today).days

    @property
    def overdue_days(self):
        if self.days_remaining is None:
            return None
        return max(0, -self.days_remaining)

    @property
    def months_and_days_remaining(self):
        """
        Returns a tuple: (months, days) remaining until expiry.
        Example: (1, 23) = 1 month 23 days left.
        Includes approx month calculation without external libraries.
        """
        expiry = self._expiry_date()
        if not expiry:
            return None, None

        today = timezone.localdate()

        # If expired
        if expiry < today:
            return 0, - (expiry - today).days

        # Calculate Month
        months = (expiry.year - today.year) * 12 + (expiry.month - today.month)

        # If expiry day hasn't occurred yet, reduce 1 month
        if expiry.day < today.day:
            months -= 1

        # Calculate Day
        year = today.year + (today.month + months - 1) // 12
        month = (today.month + months - 1) % 12 + 1
        day = min(today.day, 28)
        ref_date = date(year, month, day)
        days = (expiry - ref_date).days

        # fallback if something went wrong
        if days < 0:
            days = 0

        return months, days

    @property
    def time_remaining_display(self):
        # Check if software has no expiry date
        if self.days_remaining is None:
            return "N/A"

        # Check if software is expired
        if self.days_remaining < 0:
            return f"Expired {self.overdue_days} days ago"

        # Get months and days
        months, days = self.months_and_days_remaining

        # If month is at least 1 month
        if months >= 1:
            month_label = "month" if months == 1 else "months"
            day_label = "day" if days == 1 else "days"
            return f"{months} {month_label} and {days} {day_label} left"

        # If license is less than one month then show days only
        day_label = "day" if days == 1 else "days"
        return f"{days} {day_label} left"