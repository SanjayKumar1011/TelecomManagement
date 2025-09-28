from rest_framework.serializers import ModelSerializer,ValidationError
from .models import Plan, Subscription
from django.utils import timezone

class PlanSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'  
    def validate_price(self, value):
        if value < 0:
            raise ValidationError("Price must be a positive number.")
        return value
    
    def validate_validity_days(self, value):
        if value <= 0:
            raise ValidationError("Validity days must be a positive integer.")
        return value
    
class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

    def validate(self, data):
        start_date = (
        data.get('start_date') or
        (self.instance.start_date if self.instance else timezone.now().date())
        )
        end_date = data.get('end_date')

        if start_date and end_date and end_date <= start_date:
            raise ValidationError("End date must be after start date.")
        return data
   
    def validate_is_active(self, value):
        if not isinstance(value, bool):
            raise ValidationError("is_active must be a boolean value.")
        return value
    
    def validate_user(self, value):
        if not value.is_active:
            raise ValidationError("User must be active to have a subscription.")
        return value    
    