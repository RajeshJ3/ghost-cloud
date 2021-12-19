from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from objects import models as objects_models
from objects import serializers as objects_serializers

from utils import responses

class ObjectAPIView(APIView):

    model_class = objects_models.Object
    serializer_class = objects_serializers.ObjectSerializer
    
    @swagger_auto_schema(
        responses=responses.GET_RESPONSES,
        manual_parameters=[
            openapi.Parameter(name="id", in_="query", type=openapi.TYPE_INTEGER),
            openapi.Parameter(name="uuid", in_="query", type=openapi.TYPE_STRING),
            openapi.Parameter(name="belongs_to_uuid", in_="query", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, *args, **kwargs):

        qp = self.request.query_params

        id = qp.get("id", None)
        uuid = qp.get("uuid", None)
        belongs_to_uuid = qp.get("belongs_to_uuid", None)
        
        qs = self.model_class.objects.filter(
            Q(user=self.request.user) &
            Q(is_active=True)
        )

        if id:
            qs = qs.filter(id=id)

        if uuid:
            qs = qs.filter(uuid=uuid)
        
        if belongs_to_uuid:
            qs = qs.filter(belongs_to__uuid=belongs_to_uuid)

        s_qs = self.serializer_class(qs, many=True)

        return Response(s_qs.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=serializer_class,
        responses=responses.POST_RESPONSES,
    )
    def post(self, *args, **kwargs):
        data = self.request.data

        data = {
            **data,
            "user": self. request,
        }

        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
