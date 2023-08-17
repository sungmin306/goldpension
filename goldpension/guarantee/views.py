from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Gcompany
from .serializers import SearchSerializer, GcompanySerializer
from django.db.models import Q
from rest_framework import status
# Create your views here.


class GcompanyView(APIView):
    def get(self,request):
        print("들어왔습니다.")
        name = request.data.get('name')
        print(name)
        phone_number = request.data.get('phone_number')
        print(phone_number)
        queryset = Gcompany.objects.filter(name = name, phone_number = phone_number)
        print(queryset)
        serializer_data = []
        for i in queryset:
            serializer = SearchSerializer(i)
            serializer_data.append(serializer.data)
        print(serializer_data)
        return Response(serializer_data)
    
    def post(self, request, format=None):
        serializer = GcompanySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    