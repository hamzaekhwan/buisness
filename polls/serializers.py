from rest_framework import serializers,viewsets
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

class appstore_configSerializer(serializers.ModelSerializer):
    class Meta:
        model = appstore_config_class
        fields = ('status','Link')
class Playstore_configSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playstore_config_class
        fields = ('status','Link')       


class ConfigSerializer(serializers.ModelSerializer):

    playstore = Playstore_configSerializer(many=True)
    appstore=appstore_configSerializer(many=True)
    class Meta:
        model = config
        fields = ('app_name','App_icon','app_email','app_phone','Maintaince_mode','App_account','app_version','Termes_conditions','About_us', 'privacy_policy','playstore','appstore')
    
      

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
   
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name



class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance








class pic (object)        :
    def __init__(self,image):
        self.image=image


class picSerializer(serializers.Serializer)        :

    image=serializers.ImageField()