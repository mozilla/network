from django.urls import reverse
from rest_framework.test import APITestCase

from networkapi.buyersguide.factory import ProductFactory
from networkapi.buyersguide.models import RangeVote, BooleanVote
from django.core.management import call_command

VOTE_URL = reverse('product-vote')


class ManagementCommandTest(APITestCase):

    def test_aggregate_product_votes_range(self):
        """
        Test that aggregate_product_votes properly aggregates range votes
        """

        product = ProductFactory.create()
        test_product_id = product.id
        request_data = {
            'attribute': 'creepiness',
            'productID': test_product_id
        }

        self.assertListEqual(product.votes, [])

        # Make 10 creepiness votes
        for i in (1, 10, 20, 30, 40, 50, 60, 70, 80, 90):
            request_data['value'] = i
            response = self.client.post(VOTE_URL, request_data, format='json')
            self.assertEqual(response.status_code, 201)

        request_data['attribute'] = 'confidence'
        for value in (True, False):
            request_data['value'] = value
            for _ in range(5):
                response = self.client.post(VOTE_URL, request_data, format='json')
                self.assertEqual(response.status_code, 201)

        call_command('aggregate_product_votes')

        self.assertListEqual(product.votes, [{
            'attribute': 'creepiness',
            'average': 45,
            'vote_breakdown': {
                '0': 3,
                '1': 2,
                '2': 2,
                '3': 2,
                '4': 1
            }
        }, {
            'attribute': 'confidence',
            'vote_breakdown': {
                '0': 5,
                '1': 5
            }
        }])


class BuyersGuideVoteTest(APITestCase):

    def test_can_vote_range(self):
        """
        Range votes are recorded
        """

        test_product_id = ProductFactory.create().id
        vote_value = 50

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 201)

        latest_vote = RangeVote.objects.last()

        self.assertEqual(latest_vote.value, vote_value)
        self.assertEqual(latest_vote.product.id, test_product_id)

    def test_can_vote_bool(self):
        """
        Boolean votes are recorded
        """
        test_product_id = ProductFactory.create().id
        vote_value = True

        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')
        latest_vote = BooleanVote.objects.last()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(latest_vote.value, vote_value)
        self.assertEqual(latest_vote.product.id, test_product_id)

    def test_invalid_values(self):
        """
        Value can't be anything other than a Boolean or int
        """
        test_product_id = ProductFactory.create().id
        # String values not allowed
        vote_value = 'invalid'

        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        # Floating point numbers not allowed
        vote_value = 14.5
        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        # undefined values not allowed
        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': None,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

    def test_invalid_productID(self):
        """
        productID must be an int, and must exist in the database
        """
        test_product_id = '1'
        vote_value = 50

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        # Test an id that won't exist
        test_product_id = 100000000

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

    def test_range_value_out_of_range(self):
        """
        If value is an int, it must be between 1 and 100
        """
        test_product_id = ProductFactory.create().id
        vote_value = 0

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        test_product_id = ProductFactory.create().id
        vote_value = 101

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

    def test_invalid_attribute_with_int(self):
        """
        Test that attribute can only be 'creepiness' when value is an int
        """
        test_product_id = ProductFactory.create().id
        vote_value = 50

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 201)

        test_product_id = ProductFactory.create().id

        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

    def test_invalid_attribute_with_boolean(self):
        """
        Test that attribute can only be 'confidence' when value is a boolean
        """
        test_product_id = ProductFactory.create().id
        vote_value = True

        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 201)

        test_product_id = ProductFactory.create().id

        response = self.client.post(VOTE_URL, {
            'attribute': 'creepiness',
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

    def test_missing_payload_attributes(self):
        """
        Test that missing attributes are handled
        """
        test_product_id = ProductFactory.create().id
        vote_value = True

        # no attribute
        response = self.client.post(VOTE_URL, {
            'value': vote_value,
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        # no value
        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'productID': test_product_id
        }, format='json')

        self.assertEqual(response.status_code, 400)

        # no productID
        response = self.client.post(VOTE_URL, {
            'attribute': 'confidence',
            'value': vote_value
        }, format='json')

        self.assertEqual(response.status_code, 400)
