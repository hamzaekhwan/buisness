from urllib import response
from rest_framework.response import Response
from polls.models import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from polls.serializers import  *
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model    
from rest_framework.permissions import IsAuthenticated  , IsAdminUser
from rest_framework import status
from rest_framework import generics





@api_view(['GET'])

def getconfig(request):
    inf = config.objects.all()
    serializer = ConfigSerializer(inf, many=True)
    
    return Response({'config':serializer.data})


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        data["detail"]="ok"
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer     

from django.http import HttpResponse   
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
@api_view(['POST'])
def signup(request):  
    try:

        data = request.data  
        print(data)  
            # save form in the memory not in database  
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password']),
            is_active=False
        ) 
        print(user)
            # to get the domain of the current site  
        current_site = get_current_site(request)  
        
        mail_subject = 'Activation link has been sent to your email id'  
        message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
        print(message)    
        to_email = data['email']
        email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
        print("Fsfs")    
        email.send()  
        print("Fsfs")
        return Response('Please confirm your email address to complete the registration')   

    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


    
def activate(request, uidb64, token):  
    User = get_user_model()  
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  


def confirm_change(request, uidb64, token):  
    User = get_user_model()  
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        query=Profile.objects.get(user=user)
        query.Isverified=True
        user.save()  
        query.save()
        return HttpResponse('your email is updated and you are active now.')  
    else:  
        return HttpResponse('Activation link is invalid!') 

class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer










@api_view(['PUT'])
@permission_classes([IsAuthenticated])

def updateUserProfile(request):
    user = request.user

    query=Profile.objects.get(user=user)
    data = request.data
    if "Name" in data :
        query.Name=data['Name']
    if "Job" in data   :
        query.Job=data['Job']
    
    if "Bio" in data :
        query.Bio=data['Bio']    
    if "Location" in data: 
        query.Location=data['Location']
    if "image" in data :
        print(query)
        file=data['image']
        query.Image=file 
    if "Email" in data:
        query.Isverified=False
        user.email=data['Email']
        user.is_active=False
        current_site = get_current_site(request)  
        
        mail_subject = 'Activation link has been sent to your email id'  
        message = render_to_string('confirm_change_email.html', {  
                'email':data['Email'],
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })      
        to_email = data['Email']
        email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            ) 
        email.send()     
    query.save()   
    user.save() 
    return Response('profile is updated')      

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])

def getUserProfile(request):    

    user = request.user
    jsonObject={}
    jsonObject['isActive']=user.is_active
    query=query=Profile.objects.get(user=user)
    file=query.Image
    obj=pic(file)
    serializer=picSerializer(obj)
    img=serializer.data
    jsonObject['Image']=img['image']
    jsonObject['Name ']=query.Name
    jsonObject['Email']=user.email
    jsonObject['Job']=query.Job
    jsonObject['Bio ']=query.Bio
    jsonObject['Location ']=query.Location
    jsonObject['Isverified ']=query.Isverified




    return Response(jsonObject)
  
@api_view(['DELETE'])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')



