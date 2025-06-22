import logging

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.serializers import UserSerializer

logger = logging.getLogger(__name__)

class UserRegistration(APIView):
    @extend_schema(
        summary='User registration',
        description='User registration for create, update, delete their own shops',
        request=UserSerializer,
        responses=UserSerializer,

    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('User registration successful')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error('User registration failed. userViews.py POST')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

