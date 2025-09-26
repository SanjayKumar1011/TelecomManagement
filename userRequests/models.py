from django.db import models
from accounts.models import User

class ServiceRequest(models.Model):
    StatusChoices = [
        ('OPEN', 'Open'),     
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),]
    customer = models.ForeignKey(User, on_delete=models.CASCADE,
                             limit_choices_to={'role': 'CUSTOMER'})
    issue_description = models.TextField()
    status = models.CharField(max_length=20, choices=StatusChoices, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request {self.id} by {self.customer.username} - {self.status}"