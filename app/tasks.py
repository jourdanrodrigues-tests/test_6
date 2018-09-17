from app.models import Customer, SubscriptionValue, ChocolateRecommendation
from core.celery import app


@app.task
def generate_recommendations():
    for customer in Customer.objects.with_preferences_set_up().that_should_receive_recommendations():
        chocolate_recommendation = ChocolateRecommendation.objects.generate_from_customer(customer)
        chocolate_recommendation.email_customer()


@app.task
def bill():
    current_subscription_value = SubscriptionValue.objects.last().value
    for customer in Customer.objects.that_should_be_billed().select_related('user', 'subscription'):
        customer.charge(current_subscription_value)
