import pandas as pd
import numpy as np
from userRequests.models import ServiceRequest
from accounts.models import User
from services.models import Plan, Subscription

def ComplaintStatusCount():
    """
    Returns a dictionary with counts of service requests by their status.
    Steps:
    1. Query all ServiceRequest objects and get only their 'status' field as a list of dicts.
    2. If there are no service requests, return a dictionary with all statuses set to 0.
    3. Convert the list of status dicts to a pandas DataFrame for easier counting.
    4. Use pandas 'value_counts' to count how many times each status appears.
    5. Convert the result to a dictionary and return it.
    """
    # Step 1: Query all service request statuses
    status_counts = ServiceRequest.objects.values('status')
    # Step 2: If no service requests, return all zeros
    if not status_counts:
        return {"Open": 0, "In Progress": 0, "Resolved": 0, "Closed": 0}
    # Step 3: Convert to DataFrame
    df = pd.DataFrame(status_counts)
    # Step 4: Count each status
    counts = df['status'].value_counts().to_dict()
    # Step 5: Return the counts as a dictionary
    return counts

def avg_resolution_time():
    """
    Calculates the average resolution time for resolved service requests.
    Steps:
    1. Query all ServiceRequest objects with status 'RESOLVED' and a non-null resolved_at field.
    2. If there are no such requests, return 0.
    3. Convert the queryset to a pandas DataFrame with 'created_at' and 'resolved_at' columns.
    4. Convert these columns to datetime objects for calculation.
    5. Calculate the resolution time for each request (difference between resolved_at and created_at, in hours).
    6. Compute the mean (average) of all resolution times.
    7. Return the average, rounded to 2 decimal places.
    """
    # Step 1: Get resolved requests
    resolved_requests = ServiceRequest.objects.filter(status='RESOLVED').exclude(resolved_at__isnull=True)
    # Step 2: If none, return 0
    if not resolved_requests.exists():
        return 0
    # Step 3: Convert to DataFrame
    df = pd.DataFrame.from_records(resolved_requests.values('created_at', 'resolved_at'))
    # Step 4: Convert to datetime
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['resolved_at'] = pd.to_datetime(df['resolved_at'])
    # Step 5: Calculate resolution time in hours
    df['resolution_time'] = (df['resolved_at'] - df['created_at']).dt.total_seconds() / 3600.0
    # Step 6: Compute average
    avg_time = df['resolution_time'].mean()
    # Step 7: Return rounded average
    return round(avg_time, 2)

def subscription_stats():
    """
    Returns a dictionary with counts of users by their subscription plans.
    Steps:
    1. Query all User objects and get their 'role' and related 'subscription__plan__name' fields.
    2. If there are no users, return a dictionary with all plan names set to 0.
    3. Convert the list of user subscription dicts to a pandas DataFrame for easier counting.
    4. Use pandas 'value_counts' to count how many users are subscribed to each plan.
    5. Convert the result to a dictionary and return it.
    """
    # Step 1: Query user roles and their subscription plan names
    user_subscriptions = Subscription.objects.values('is_active')
    # Step 2: If no users, return all zeros
    if not user_subscriptions:
        return {"No subscrption found"}
    # Step 3: Convert to DataFrame
    df = pd.DataFrame(list(user_subscriptions))
    # Step 4: Count users per subscription plan
    counts = df['is_active'].value_counts().to_dict()
    # Step 5: Return the counts as a dictionary
    return {'subscriptions': counts}