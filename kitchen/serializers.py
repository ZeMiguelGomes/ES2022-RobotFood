from rest_framework import serializers
from .models import Staff

class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff 
        fields = ('staff_email', 'staff_name', 'password', 'authToken', 'isLoggedIn')