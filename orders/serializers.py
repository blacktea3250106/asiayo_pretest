from rest_framework import serializers

class AddressSerializer(serializers.Serializer):
    city = serializers.CharField()
    district = serializers.CharField()
    street = serializers.CharField()

class OrderSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    address = AddressSerializer()
    price = serializers.IntegerField()
    currency = serializers.CharField()

    def validate_name(self, value):
        """Validate that the name contains only ASCII characters and is capitalized."""
        if not value.isascii():
            raise serializers.ValidationError("Name contains non-English characters")
        if not all(word[0].isupper() for word in value.split()):
            raise serializers.ValidationError("Name is not capitalized")
        return value

    def validate_price(self, value):
        """Validate that the price does not exceed 2000."""
        if value > 2000:
            raise serializers.ValidationError("Price is over 2000")
        return value

    def validate_currency(self, value):
        """Validate the currency."""
        if value not in ["TWD", "USD"]:
            raise serializers.ValidationError("Currency format is wrong")
        return value

    def validate(self, attrs):
        """Perform additional validation and transformation."""
        price = attrs.get('price')
        currency = attrs.get('currency')

        if currency == "USD":
            # Convert price from USD to TWD
            attrs['price'] = price * 31
            attrs['currency'] = "TWD"
        return attrs

