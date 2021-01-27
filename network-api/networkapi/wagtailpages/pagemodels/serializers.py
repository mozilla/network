import datetime
from rest_framework import serializers
from wagtail_airtable.serializers import AirtableSerializer

from networkapi.buyersguide.fields import ExtendedYesNoField
from networkapi.wagtailpages.pagemodels.products import TRACK_RECORD_CHOICES


class TrackRecordChoicesSerializer(serializers.RelatedField):
    def to_internal_value(self, data):
        value = data.lower().strip()
        for choice_key, choice_value in TRACK_RECORD_CHOICES:
            print(f"{choice_key} vs {value}")
            if choice_key.lower() == value:
                return str(choice_key)
        return data

    def get_queryset(self):
        pass


class ExtendedYesNoSerializer(serializers.RelatedField):
    """
    Custom serializer for importing ExtendedYesNoFields.

    ie. Finds "U" in a list of ["U", "Yes", "No", "NA"].
    """

    def to_internal_value(self, data):
        value = data.lower().strip()
        for choice_key, choice_value in ExtendedYesNoField.choice_list:
            if choice_key.lower() == value:
                return choice_key
        return data

    def get_queryset(self):
        pass


class DateSerializer(serializers.DateTimeField):
    def to_internal_value(self, date):
        if type(date) == str and len(date):
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        return date


class ProductSerializer(AirtableSerializer):

    # Page.title from wagtailcore.page. Airtable can update this value.
    title = serializers.CharField(max_length=255, required=True)
    privacy_ding = serializers.BooleanField(default=False)
    adult_content = serializers.BooleanField(default=False)
    uses_wifi = serializers.BooleanField(default=False)
    uses_bluetooth = serializers.BooleanField(default=False)
    review_date = DateSerializer(required=True)
    company = serializers.CharField(required=False, max_length=100)
    blurb = serializers.CharField(required=False, max_length=5000)
    product_url = serializers.URLField(required=False, max_length=2048)
    price = serializers.CharField(required=False, max_length=100)
    worst_case = serializers.CharField(required=False, max_length=5000)
    signup_requires_email = ExtendedYesNoSerializer(default='U')
    signup_requires_phone = ExtendedYesNoSerializer(default='U')
    signup_requires_third_party_account = ExtendedYesNoSerializer(default='U')
    signup_requirement_explanation = serializers.CharField(required=False, max_length=5000)
    how_does_it_use_data_collected = serializers.CharField(required=False, max_length=5000)
    data_collection_policy_is_bad = serializers.BooleanField(default=False)
    user_friendly_privacy_policy = ExtendedYesNoSerializer(default='U')
    show_ding_for_minimum_security_standards = serializers.BooleanField(default=False)
    meets_minimum_security_standards = serializers.BooleanField(default=False)
    uses_encryption = ExtendedYesNoSerializer(default='U')
    uses_encryption_helptext = serializers.CharField(required=False, max_length=5000)
    security_updates = ExtendedYesNoSerializer(default='U')
    security_updates_helptext = serializers.CharField(required=False, max_length=5000)
    strong_password = ExtendedYesNoSerializer(default='U')
    strong_password_helptext = serializers.CharField(required=False, max_length=5000)
    manage_vulnerabilities = ExtendedYesNoSerializer(default='U')
    manage_vulnerabilities_helptext = serializers.CharField(required=False, max_length=5000)
    privacy_policy = ExtendedYesNoSerializer(default='U')
    privacy_policy_helptext = serializers.CharField(required=False, max_length=5000)
    phone_number = serializers.CharField(required=False, max_length=100)
    live_chat = serializers.CharField(required=False, max_length=100)
    email = serializers.CharField(required=False, max_length=100)
    twitter = serializers.CharField(required=False, max_length=100)


class GeneralProductPageSerializer(ProductSerializer):
    """
    YourModel serializer used when importing Airtable records.
    This serializer will help validate data coming in from Airtable and help prevent
    malicious intentions.
    This model assumes there is a "name" mapping in YourModel.map_import_fields()
    """

    camera_device = ExtendedYesNoSerializer(default='U')
    camera_app = ExtendedYesNoSerializer(default='U')
    microphone_device = ExtendedYesNoSerializer(default='U')
    microphone_app = ExtendedYesNoSerializer(default='U')
    location_device = ExtendedYesNoSerializer(default='U')
    location_app = ExtendedYesNoSerializer(default='U')
    personal_data_collected = serializers.CharField(required=False, max_length=5000)
    biometric_data_collected = serializers.CharField(required=False, max_length=5000)
    social_data_collected = serializers.CharField(required=False, max_length=5000)
    how_can_you_control_your_data = serializers.CharField(required=False, max_length=5000)
    data_control_policy_is_bad = serializers.BooleanField(default=False, required=False)  # TODO: Test a blank import
    company_track_record = TrackRecordChoicesSerializer(default='Average')  # TODO: Test this imports correctly
    track_record_is_bad = serializers.BooleanField(default=False, required=False)
    track_record_details = serializers.CharField(required=False, max_length=5000)
    offline_capable = ExtendedYesNoSerializer(default='U')
    offline_use_description = serializers.CharField(required=False, max_length=5000)
    uses_ai = ExtendedYesNoSerializer(default='U')
    ai_uses_personal_data = ExtendedYesNoSerializer(default='U')
    ai_is_transparent = ExtendedYesNoSerializer(default='U')
    ai_helptext = serializers.CharField(required=False, max_length=5000)
