from unittest import mock

from django.db.models import Model
from django.test import SimpleTestCase

from app.models import Customer


class TestSave(SimpleTestCase):
    def test_when_billing_day_is_in_the_allowed_range_then_saves_the_instance(self):
        customer = Customer(billing_day=2)

        with mock.patch.object(Model, 'save') as mocked_save:
            customer.save()

        mocked_save.assert_called_once()

    def test_when_billing_day_is_not_in_the_allowed_range_then_raises_exception(self):
        customer = Customer(billing_day=32)

        with self.assertRaises(Customer.BillingDayNotAllowed):
            customer.save()
