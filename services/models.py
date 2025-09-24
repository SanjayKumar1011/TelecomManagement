from django.db import models

class Plan(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    validity_days=models.IntegerField()

    def __str__(self):
        return self.name
    
class Subscription(models.Model):
    user=models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    plan=models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date=models.DateField(auto_now_add=True)
    end_date=models.DateField()
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"