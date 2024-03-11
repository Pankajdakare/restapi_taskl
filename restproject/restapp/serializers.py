from rest_framework import serializers
from restapp.models import Client,Project
from django.contrib.auth.models import User

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields ='__all__'


class UserSerialiser(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'}, write_only = True)
    class Meta:
        model = User
        fileds = ['username','email','password','password2']
        extra_kwargs = {
            'password':{ 'write_only':True}
        }
    
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        print('HERE..... $$$$$ ',self.validated_data)
        if password != password2 :
            raise serializers.ValidationError({"Error":"password does not match"})
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({"Error":"email already exists"})
        
        account = User(email = self.validated_data['email'], username = self.validated_data['username'])
        account.set_password(password = self.validated_data['password'])
        account.save()
        return account
    

class ProjectSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields ='__all__'
    

