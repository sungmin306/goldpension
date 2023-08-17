from rest_framework import serializers
from .models import Gcompany

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gcompany
        fields = (
            'searching', 
            'apply_detail', 
            'company_name', 
            'work_place',
        )
        

class GcompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gcompany
        fields = [
            "name",
            "age",
            "phone_number",
            "gender", 
            'searching', 
            'apply_detail', 
            'company_name', 
            'work_place',
        ]