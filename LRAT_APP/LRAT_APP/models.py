from django.db import models
from django.contrib.auth.models import User

# Each user has one dashboard
class UserDashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_logins = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Dashboard"

# Each dashboard can have multiple subscriptions
class Subscription(models.Model):
    dashboard = models.ForeignKey(UserDashboard, on_delete=models.CASCADE, related_name='subscriptions')
    name = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, default="Active")  # Active, Expiring, etc.

    def __str__(self):
        return f"{self.name} ({self.dashboard.user.username})"
