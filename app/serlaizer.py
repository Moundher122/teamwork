from rest_framework import serializers
from .models import User,file

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(
        write_only=True
    )
    class Meta:
        model = User
        fields = ['id','username','email','password']

class fileserlaizer(serializers.ModelSerializer):
    class Meta:
        model=file
        fields='__all__'
    