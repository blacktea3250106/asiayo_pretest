from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

order_request_schema = swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_STRING, description='Order ID'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Hotel name'),
            'address': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'city': openapi.Schema(type=openapi.TYPE_STRING, description='City'),
                    'district': openapi.Schema(type=openapi.TYPE_STRING, description='District'),
                    'street': openapi.Schema(type=openapi.TYPE_STRING, description='Street'),
                },
                required=['city', 'district', 'street'],
            ),
            'price': openapi.Schema(type=openapi.TYPE_INTEGER, description='Order price'),
            'currency': openapi.Schema(type=openapi.TYPE_STRING, description='Currency'),
        },
        required=['id', 'name', 'address', 'price', 'currency'],
        example={
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                'city': "taipei-city",
                'district': "da-an-district",
                'street': "fuxing-south-road"
            },
            "price": 2050,
            "currency": "TWD"
        }
    ),
    responses={
        '201': openapi.Response(description='Order created successfully'),
        '400': openapi.Response(
            description='Bad Request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                        description='Name errors',
                        example=['Name contains non-English characters', 'Name is not capitalized']
                    ),
                    'price': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                        description='Price errors',
                        example=['Price is over 2000']
                    ),
                    'currency': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                        description='Currency errors',
                        example=['Currency format is wrong']
                    ),
                }
            )
        ),
    }
)