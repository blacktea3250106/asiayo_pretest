from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OrderSerializer
from .swaggers import order_request_schema

class OrderView(APIView):
    @order_request_schema
    def post(self, request):
        """Handle POST request to validate and transform order data."""
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


