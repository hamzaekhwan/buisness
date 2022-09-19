
import profile
from rest_framework.response import Response
from polls.models import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from polls.serializers import  *
from polls.functions import  *
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model    
from rest_framework.permissions import IsAuthenticated  , IsAdminUser
from rest_framework import status
from rest_framework import generics
import base64
import os



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
            # save form in the memory not in database  
            if User.objects.filter(email=data['email']).exists() or User.objects.filter(username=data['username']).exists()  :
                message = {'detail': 'User with this email or username already exists'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:    
                user = User.objects.create(
                    username=data['username'],
                    email=data['email'],
                    password=make_password(data['password'])     
                ) 
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
        
                email.send()  
                message = {'detail': 'Please confirm your email address to complete the registration'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST) 

    except:
        message = {'detail': 'User with this email or username already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def configMail(request): 

        user=request.user
        pro=Profile.objects.get(user=user)
        if pro.Isverified==True:
            message = {'detail': 'your email is already verified'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:


            current_site = get_current_site(request)  
            
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':account_activation_token.make_token(user),  
                })  
            print(message)    
            to_email = user.email
            email = EmailMessage(  
                            mail_subject, message, to=[to_email]  
                )  

            email.send()  
            message = {'detail': 'email verefied was sent successfully'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
def activate(request, uidb64, token):  
    User = get_user_model()  
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    pro=Profile.objects.get(user=user)    
    if pro.Isverified == True:
        user=None    
    if user is not None and account_activation_token.check_token(user, token):  
        
        pro.Isverified = True  
        pro.save()  
        return HttpResponse('Thank you for your email confirmation. Now your account is verified')  
    else:  
        return HttpResponse('Activation link is invalid!')  


def confirm_change(request, uidb64, token):  
    User = get_user_model()  
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    pro=Profile.objects.get(user=user)    
    if pro.Isverified == True:
        user=None    
    if user is not None and account_activation_token.check_token(user, token):  
        
        pro.Isverified = True  
        pro.save()
        return HttpResponse('your email is updated and you are verified now.')  
    else:  
        return HttpResponse('verification link is invalid!') 

# class ChangePasswordView(generics.UpdateAPIView):

#     queryset = User.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ChangePasswordSerializer


class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            data=request.data
            old_password=data['old_password']
            password=data['password']
            password2=data['password2']
            # serializer = self.get_serializer(data=request.data)
            
            
          
                # Check old password
               
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(password)
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        






@api_view(['GET', 'POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])



def social(request):
    if request.method == 'POST' :
        try:    

            user=request.user
            dataa=request.data
            fid=dataa['fid']
            
            username=dataa['username']
            isActive=dataa['isActive']  
            if isActive=="true":
                isActive=True
            else:
                isActive=False    

            if 'title' in dataa:
                title = dataa['title']
            else:
                title=" "        
            query1=platforms.objects.get(id=fid,isActive=True)
            if data.objects.filter(user_id=user.id , form_id=fid).exists():
                return Response({'you already have a '+ query1.name + " account here " })

            else:
                queryforsave=data(user_id=user.id,form_id=query1.id,name=query1.name,title=title,domain=query1.domain,username=username,color1=query1.color1,color2=query1.color2,image=query1.image,isActive=isActive)
                queryforsave.save()
                return Response({'socilaLink is saved'})
        except:
            message = {'detail': 'there is a proplem here'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT' :
        user=request.user
        dataa=request.data
        fid=dataa['fid']
        query1=platforms.objects.get(id=fid,isActive=True)
        queryforedit=data.objects.get(user_id=user.id,form_id=fid)
        if 'title' in dataa:
            title=dataa['title']
        else:
            title=queryforedit.title    
        if 'username' in dataa:
            url=dataa['username']
        else:
            url=queryforedit.username    
        if 'isActive'  in dataa:
            if dataa['isActive']=="true":
                queryforedit.isActive=True
            else:
                queryforedit.isActive=False    
        queryforedit.title=title          
        queryforedit.username=url
        queryforedit.save()
        return Response({'socilaLink is updated'})


    if request.method == 'GET' : 
        try:
            user = request.user
            query=data.objects.filter(user_id=user.id)
            jsonObject={}
            jsonObject['user_id']=user.id
            jsonObject['isDirectOn']=query[0].isDirectOn
            a=[]
            for i in query:
                
                jsonObject2={}  
                jsonObject2['form_id']=i.form_id
                another=platforms.objects.get(id=i.form_id)
                jsonObject2['name']=i.name
                jsonObject2['isActive']=i.isActive
                jsonObject2['title']=i.title
                jsonObject2['domain']=i.domain
                                     
                jsonObject2['link_type']=convert_ltype(another.link_type)
              
                jsonObject2['section']=convert_section(another.section)
                jsonObject2['username']=i.username
                color=[]
                color.append(i.color1)
                color.append(i.color2)
                jsonObject2['color_list']=color
                file=i.image
                obj=fi(file)
                serializer=fileSerializer(obj)
                img=serializer.data
                jsonObject2['image']=img['file']
                a.append(jsonObject2)

            jsonObject['data']=a
            return Response({'socialLinks':jsonObject})
        except:
            jsonObject={}
            jsonObject['user_id']=user.id
            jsonObject['isDirectOn']=False
            jsonObject['data']=[]
            return Response({'socialLinks':jsonObject})
    if request.method == 'DELETE' :
        user=request.user
        dataa=request.data
        fid=dataa['fid']
        data.objects.filter(user_id=user.id , form_id=fid).delete()
        return Response({'socilaLink is deleted'})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editIsDirectOn(request):
    user=request.user
    dataa=request.data
    isDirectOn=dataa['isDirectOn']
    if data.objects.filter(user_id=user.id).exists():
        if isDirectOn=="true":
            data.objects.filter(user_id=user.id).update(isDirectOn=True)
        else :
            data.objects.filter(user_id=user.id).update(isDirectOn=False)
        query=    data.objects.filter(user_id=user.id)
        return Response({'isDirectOn':query[0].isDirectOn})
    else:
        message = {'detail': 'you have not any social link'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def social_arrange(request):
    try:
        user=request.user
        dataa=request.data
        form_id=dataa['form_id']
     
        data.objects.filter(user_id=user.id).update(index_num=" ")
        data.objects.filter(user_id=user.id,form_id=form_id).update(index_num="1")
        return Response({"detail":" your social link ordered successfully  "})    
    except:
        message = {'detail': 'you have not more social links'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)   

from django.core.files.base import ContentFile

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])

def UserProfile(request):
   if request.method == 'PUT' :
    user = request.user
    query=Profile.objects.get(user=user)
    data = request.data
    if "name" in data:
        query.Name=data['name']
    if "job" in data:
        query.Job=data['job']
    if "bio" in data:
        query.Bio=data['bio']
    if "location" in data:
        query.Location=data['location']
    if "image" in data:
        
        code64=data['image']
        import shortuuid
        s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
        otp = s.random(length=5)
        image_name = user.username + "_" + otp+".png"

        extension = image_name.split('.')[1].lower()

        image_name = '{}_{}_profile_image.{}'.format(request.user.first_name, request.user.last_name, extension)

        imgStr = code64.split(';base64')

        data = ContentFile(base64.b64decode(imgStr[1]), name=image_name)


        query.Image=data
    if "email" in data:
        user.email=data['email']
        query.Isverified=False
        current_site = get_current_site(request)  
        
        mail_subject = 'Activation link has been sent to your email id'  
        message = render_to_string('confirm_change_email.html', {  
                'email':data['email'],
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })      
        to_email = data['email']
        email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            ) 
        email.send()     
    query.save()   
    user.save() 
    return Response({'detail':'profile is updated'})      
   elif  request.method == 'GET' :
    user = request.user
    jsonObject={}
    jsonObject['isActive']=user.is_active
    query=query=Profile.objects.get(user=user)
    file=query.Image
    obj=pic(file)
    serializer=picSerializer(obj)
    img=serializer.data
    jsonObject['email']=user.email
    jsonObject['job']=query.Job
    jsonObject['bio ']=query.Bio
    jsonObject['location ']=query.Location
    jsonObject['isVerified ']=query.Isverified
    return Response(jsonObject)

@api_view(['GET', 'POST','DELETE'])
@permission_classes([IsAuthenticated])
def favoriteUser(request):
    if request.method == 'POST' :  
        data=request.data
        user=request.user
        user_id=data['user_id']
        if User.objects.filter(id=user_id).exists():
            if favorite.objects.filter(user_id=user.id,favoriteUser_id=user_id).exists():
                message = {'detail': 'this user is already in favorite list'}  
                return Response(message)
            else:
                
                fav=favorite(user_id=user.id,favoriteUser_id=user_id)
                fav.save() 
                message = {'detail': 'successfully added to favorite list'}  
                return Response(message)
        else:
            message = {'detail': 'user with this id is not exist'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET' :
        user=request.user
        fav=favorite.objects.filter(user_id=user.id)
        if fav.exists():
            for i in fav:
                arr=[]
                jsonObject={}
                jsonObject['favorite_user']=i.favoriteUser_id
                query=Profile.objects.get(user=user)
                file=query.Image
                obj=pic(file)
                serializer=picSerializer(obj)
                img=serializer.data
                jsonObject['Image']=img['image']
                jsonObject['Name']=query.Name
                arr.append(jsonObject)
            return Response({'detail':arr})    
        else:
            message = {'detail': 'you have not any favorite user'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)        

    if request.method == 'DELETE':
        data=request.data
        user=request.user
        user_id=data['user_id']
        f=favorite.objects.filter(user_id=user.id,favoriteUser_id=user_id)
        if f.exists():
            f.delete()
            message = {'detail': 'user deleted from favorite list successfully'}  
            return Response(message)
        else:
            message = {'detail': 'this user is not in your favorite list'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def custombutton(request):
  if request.method == 'PUT' :  
    user = request.user

    query=Custom_button.objects.get(user=user)
    data = request.data
    if "title" in data :
        query.title=data['title']
    
    if "icon" in data :
        print(query)
        file=data['icon']
        query.icon=file 
    if "color" in data :
        query.color=data['color']    
    if "isActive" in data: 
        if data["isActive"] == "true":

            query.isActive=True
        else:
            query.isActive=False
    query.save()
    return Response('custom_button is updated')         
  elif  request.method == 'GET' :
    user = request.user
    query=Custom_button.objects.get(user=user)
    jsonObject={}
    
    
    file=query.icon
    obj=pic(file)
    serializer=picSerializer(obj)
    img=serializer.data
    jsonObject['user_id']=user.id
    jsonObject['icon']=img['image']
    jsonObject['isActive']=query.isActive
    jsonObject['title ']=query.title
    jsonObject['color ']=query.color



    return Response(jsonObject)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def Vcard_view(request):
    if request.method == 'PUT' : 
  
        user = request.user
        query=Vcard.objects.get(user=user)
        data = request.data
        if "image" in data :
            print(query)
            file=data['image']
            query.image=file 
        if "first_name" in data :
            query.first_name=data['first_name']
        if "last_name" in data :
            query.last_name=data['last_name']
        if "email" in data :
            query.email=data['email']

        if "phone" in data :
            query.phone=data['phone']
        if "address" in data :
            query.address=data['address']
        if "city" in data :
            query.city=data['city']
        if "state" in data :
            query.state=data['state']
        if "zip" in data :
            query.zip=data['zip']
        if "country" in data :
            query.country=data['country']
        if "company" in data :
            query.company=data['company']   
        if "title" in data :
            query.title=data['title']
        if "website" in data :
            query.website=data['website']
        if "notes" in data :
            query.notes=data['notes'] 
                       
        if "isActive" in data :
           
            if data["isActive"] == "true":

                query.isActive=True
            else:
                query.isActive=False    
        query.save()    
        import shortuuid
      
        s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
        otp = s.random(length=5)            
        file_name=user.username + "_" + otp
        vcf_file = f'{file_name.lower()}.vcf'     
        vcard = make_vcard(query.first_name,query.last_name, query.company, query.title, query.phone, query.address, query.email,query.notes,query.country ,query.city, query.zip,query.state,query.website,query.image )
        write_vcard(vcf_file, vcard)
     
        query.vcf_file    = vcf_file

        
        query.save()
        return Response('Vcard is updated') 
    elif  request.method == 'GET' : 
        user = request.user
        query=Vcard.objects.get(user=user)
        jsonObject={}
        
        
        jsonObject['user_id']=user.id
        jsonObject['first_name']=query.first_name
        jsonObject['last_name']=query.last_name
        jsonObject['email ']=query.email
        jsonObject['company ']=query.company
        jsonObject['title ']=query.title
        jsonObject['phone ']=query.phone
        jsonObject['address ']=query.address
        jsonObject['notes ']=query.notes
        jsonObject['state ']=query.state
        jsonObject['country ']=query.country
        jsonObject['city ']=query.city
        file=query.image
        obj=pic(file)
        serializer=picSerializer(obj)
        img=serializer.data
        jsonObject['image']=img['image']
        jsonObject['website']=query.website
        file=query.vcf_file
        obj=fi(file)
        
        serializer=fileSerializer(obj)
        file2=serializer.data
        jsonObject['vcf_file']=file2['file']
        
        jsonObject['isActive ']=query.isActive
        

       


        return Response(jsonObject)
def write_vcard(f, vcard):
    
    full_path = os.path.join('media', f)
    # full_path = os.path.join('/home/hamzaekhwan/buisness/media', f)
    # print(full_path)
    with open(full_path, 'w') as f:
        f.writelines([l + '\n' for l in vcard])
def make_vcard(
        first_name,
        last_name,
        company,
        title,
        phone,
        address,
        email,
        notes,
        country ,
        city,
         zip,
         state,
         website,
         image):
    address_formatted = ';'.join([p.strip() for p in address.split(',')])
    return [
        'BEGIN:VCARD',
        'VERSION:1.1',
        f'N:{last_name};{first_name}',
        f'FN:{first_name} {last_name}',
        f'ORG:{company}',
        f'TITLE:{title}',
        f'EMAIL;PREF;INTERNET:{email}',
        f'TEL;WORK;VOICE:{phone}',
        f'ADR;WORK;PREF:;;{address_formatted}',
        f'REV:1',
        f'NOTES:{notes}',
        f'COUNTRY:{country}',
        f'CITY:{city}',
        f'ZIP:{zip}',
        f'STATE:{state}',
        f'WEBSITE:{website}',
        f'IMAGE:{image}',
        
        'END:VCARD'
    ]    




@api_view(['GET'])
def get_platforms(request)    :
    platform=platforms.objects.filter(isActive=True)
    jsonObject={}
    result=[]
    for i in platform:
        print(i.name)
        jsonObject={}
        a=[]
        jsonObject['id']=i.id
        jsonObject['name']=i.name
        jsonObject['domain']=i.domain
        jsonObject['section']=convert_section(i.section)
        jsonObject['info']=i.info
        jsonObject['dialog_title']=i.dialog_title
        jsonObject['link_type']=convert_ltype(i.link_type)
        jsonObject['error_message']=i.error_message
        a.append(i.color1)
        a.append(i.color2)
        jsonObject['color_list']=a
       
        file=i.image
        obj=fi(file)
        serializer=fileSerializer(obj)
        img=serializer.data
        jsonObject['image']=img['file']
        result.append(jsonObject)

    return Response({'platforms':result})


@api_view(['GET'])
def get_socialOthers(request, pk):
    try:
        user=User.objects.get(id=pk)
        query=data.objects.filter(user_id=user.id)
        jsonObject={}
        jsonObject['user_id']=user.id
        jsonObject['isDirectOn']=query[0].isDirectOn
        if query[0].isDirectOn == True:
            query=data.objects.filter(user_id=user.id,index_num="1")
            serializer = DataSerializer(query, many=True)
            jsonObject['data']=serializer.data
            return Response({'socialLinks':jsonObject})
        else:
            serializer = DataSerializer(query, many=True)
            jsonObject['data']=serializer.data
            return Response({'socialLinks':jsonObject})    

    except:
        message={'error':'this user has not any social links'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_vcardOthers(request, pk):
    try:
        user=User.objects.get(id=pk)
        query=Vcard.objects.get(user=user)
        jsonObject={}
        jsonObject['user_id']=user.id
        jsonObject['isActive']=query.isActive
        file=query.vcf_file
        obj=fi(file)
        
        serializer=fileSerializer(obj)
        file2=serializer.data
        jsonObject['path']=file2['file']

        return Response(jsonObject)
    except:
        message={'error':'there is no user with this id'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)   




@api_view(['GET'])
def get_profileOthers(request, pk):
    try:
        user=User.objects.get(id=pk)
        jsonObject={}
        jsonObject['isActive']=user.is_active
        query=query=Profile.objects.get(user=user)
        file=query.Image
        obj=pic(file)
        serializer=picSerializer(obj)
        img=serializer.data
        jsonObject['user_id']=user.id
        jsonObject['image']=img['image']
        jsonObject['name ']=query.Name
        jsonObject['email']=user.email
        jsonObject['job']=query.Job
        jsonObject['bio ']=query.Bio
        jsonObject['location ']=query.Location
        jsonObject['isVerified ']=query.Isverified
        return Response(jsonObject)
    except:
        message={'error':'there is no user with this id'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_platform_ById(request, pk):
    try:
        platform=platforms.objects.get(id=pk,isActive=True)
        jsonObject={}
        a=[]
        jsonObject['id']=platform.id
        jsonObject['name']=platform.name
        jsonObject['domain']=platform.domain
        jsonObject['section']=convert_section(platform.section)
        jsonObject['info']=platform.info
        jsonObject['dialog_title']=platform.dialog_title
        jsonObject['link_type']=convert_ltype(platform.link_type)
        jsonObject['error_message']=platform.error_message
        a.append(platform.color1)
        a.append(platform.color2)
        jsonObject['color_list']=a
    
        file=platform.image
        obj=fi(file)
        serializer=fileSerializer(obj)
        img=serializer.data
        jsonObject['image']=img['file']
      

        return Response({'platforms':jsonObject})

    except:
        message={'error':'there is no platform with this id'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['DELETE'])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')
    