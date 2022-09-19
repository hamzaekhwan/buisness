
import profile
from rest_framework.response import Response
from polls.models import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *


from polls.serializers import  *


from rest_framework.permissions import IsAuthenticated  , IsAdminUser
from rest_framework import status
from rest_framework import generics
import  shortuuid
import os

from polls.functions import  *

@api_view(['GET', 'POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])

def title_edit(request):
    if request.method == 'POST' :
        try:
            data=request.data
            user=request.user
            if 'text' in data:
                text=data['text']
            else:
                text=" "    
            if 'fontSize' in data:
                fontSize=data['fontSize']
            else:
                fontSize=" "   
            if 'fontName' in data:
                fontName=data['fontName']
            else:
                fontName=" "    
            if 'fontType' in data:
                fontType=data['fontType']
            else:  
                fontType=" "  
            if 'fontColor' in data:
                fontColor=data['fontColor']
            else:
                fontColor = " "  
            query=    title.objects.filter(user=user)
            if    query.exists():
                message = {'detail': 'this user already has title'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)        
            new_title=title(user=user,text=text,fontSize=fontSize,fontName=fontName,fontType=fontType,fontColor=fontColor)
            new_title.save()
            message = {'detail': 'title added successfully'}
            return Response(message)
        except:
            message = {'detail': 'there is a proplem here'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST) 
    if request.method == 'PUT':
        try:
            data=request.data
            user=request.user
            title_id=data['title_id']
            query=title.objects.filter(user=user,id=title_id)
            if query.exists():
                if 'text' in data:
                    text=data['text']
                else:  
                    text=query[0].text  
                if 'fontSize' in data:
                    fontSize=data['fontSize']
                else:  
                    fontSize=query[0].fontSize

                if 'fontName' in data:
                    fontName=data['fontName']
                else:  
                    fontName=query[0].fontName    
                if 'fontType' in data:
                    fontType=data['fontType']
                else:  
                    fontType=query[0].fontType    
                if 'fontColor' in data:
                    fontColor=data['fontColor']
                else:  
                    fontColor=query[0].fontColor
                query.update(text=text,fontSize=fontSize,fontName=fontName,fontType=fontType,fontColor=fontColor)
                message = {'detail': 'title was updated'}
                return Response(message) 
            else:     
                message = {'detail': 'this user has not any title'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)     
        except:
            message = {'detail': 'there is a proplem here'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST) 
    if request.method == 'GET':
        user=request.user
        query=title.objects.filter(user=user)
        serializer=titleSerializer(query,many=True)
        return Response({'detail':serializer.data})
    if request.method == 'DELETE':
       

        data=request.data
        user=request.user
        title_id=data['title_id']
        query=title.objects.filter(id=title_id,user=user)
        if query.exists():
            query.delete()
            message = {'detail': 'title is deleted successfully'}
            return Response(message)
        else:    
    
            message = {'detail': 'your title id is incorrect'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET', 'POST','PUT','DELETE'])
def header_edit(request):
    if request.method == 'POST' :
        try:
            data=request.data
            user=request.user
            if 'text' in data:
                text=data['text']
            else:
                text=" "    
            if 'fontSize' in data:
                fontSize=data['fontSize']
            else:
                fontSize=" "   
            if 'fontName' in data:
                fontName=data['fontName']
            else:
                fontName=" "    
            if 'fontType' in data:
                fontType=data['fontType']
            else:  
                fontType=" "  
            if 'fontColor' in data:
                fontColor=data['fontColor']
            else:
                fontColor = " "       
            new_header=header(user=user,text=text,fontSize=fontSize,fontName=fontName,fontType=fontType,fontColor=fontColor)
            new_header.save()
            message = {'detail': 'header added successfully'}
            return Response(message)
        except:
            message = {'detail': 'there is a proplem here'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST) 
    if request.method == 'PUT':
        try:
            data=request.data
            user=request.user
            header_id=['header_id']
            query=header.objects.filter(user=user,id=header_id)
            if query.exists():
                if 'text' in data:
                    text=data['text']
                else:  
                    text=query[0].text  
                if 'fontSize' in data:
                    fontSize=data['fontSize']
                else:  
                    fontSize=query[0].fontSize

                if 'fontName' in data:
                    fontName=data['fontName']
                else:  
                    fontName=query[0].fontName    
                if 'fontType' in data:
                    fontType=data['fontType']
                else:  
                    fontType=query[0].fontType 
                if 'fontColor' in data:
                    fontColor=data['fontColor']
                else:  
                    fontColor=query[0].fontColor  
                query.update(text=text,fontSize=fontSize,fontName=fontName,fontType=fontType,fontColor=fontColor)
                message = {'detail': 'header was updated'}
                return Response(message)
            else:     
                message = {'detail': 'this user has not any title'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)     
        except:
            message = {'detail': 'there is a proplem here'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST) 
    if request.method == 'GET':
        user=request.user
        query=header.objects.filter(user=user)
        serializer=headerSerializer(query,many=True)
        return Response({'detail':serializer.data})
    if request.method == 'DELETE':
        data=request.data
        user=request.user
        header_id=data['header_id']
        query=header.objects.filter(id=header_id,user=user)
        if query.exists():
            query.delete()
            message = {'detail': 'header is deleted successfully'}
            return Response(message)
        else:    
    
            message = {'detail': 'your header id is incorrect'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET', 'POST','PUT','DELETE'])
def html_edit(request):
    if request.method == 'POST' :

        try:
            data=request.data
            user=request.user
            if 'body ' in data:
                body =data['body ']
            else:
                body=" "    
            if 'info' in data:
                info=data['info']
            else:
                info=" "    
            new_html=html(user=user,body=body,info=info)
            new_html.save()
            message = {'detail': 'html added successfully'}
            return Response(message)    
        except:
            message = {'detail': 'there is a proplem'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)     
    if request.method == 'PUT':

        try:

            data=request.data
            user=request.user
            html_id=data['html_id']
            query=html.objects.filter(user=user,id=html_id)
            if query.exists():   
                if 'body ' in data:
                    body =data['body ']
                else:
                    body=query[0].body   
                if 'info' in data:
                    info=data['info']
                else:
                    info=query[0].info    
                query.update(body=body,info=info)
                message = {'detail': 'html was updated'}
                return Response(message)        
        except:
            message = {'detail': 'there is a proplem here'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)         
    if request.method == 'GET':
        user=request.user
        query=html.objects.filter(user=user)
        serializer=htmlSerializer(query,many=True)
        return Response({'detail':serializer.data})   
    if request.method == 'DELETE':

        data=request.data
        user=request.user
        html_id=data['html_id']
        query=html.objects.filter(id=html_id,user=user)
        if query.exists():
            query.delete()
            message = {'detail': 'html is deleted successfully'}
            return Response(message)
        else:    
    
            message = {'detail': 'your html id is incorrect'}      


@api_view(['GET', 'POST','PUT','DELETE'])
def form_edit(request):
    if request.method == 'POST' :

        try:
            data=request.data
            user=request.user
            if 'subject ' in data:
                subject =data['subject ']
            else:
                subject=" "    
            if 'content' in data:
                content=data['content']
            else:
                content=" "    
            if 'From ' in data:
                From =data['From ']
            else:
                From=" "    
            if 'to' in data:
                to=data['to']
            else:
                to=" "
            new_form=contact_form(user=user,subject=subject,content=content,From=From,to=to)
            new_form.save()
            message = {'detail': 'Form added successfully'}
            return Response(message)    
        except:
            message = {'detail': 'there is a proplem'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)     
    if request.method == 'PUT':

        try:

            data=request.data
            user=request.user
            form_id=data['form_id']
            query=contact_form.objects.filter(user=user,id=form_id)
            if query.exists():   
                if 'subject ' in data:
                    subject =data['subject ']
                else:
                    subject=query[0].subject   
                if 'content' in data:
                    content=data['content']
                else:
                    content=query[0].content    
                if 'From' in data:
                    From=data['From']
                else:
                    From=query[0].From
                if 'to' in data:
                    to=data['to']
                else:
                    to=query[0].to        
                query.update(subject=subject,content=content,From=From,to=to)
                message = {'detail': 'form was updated'}
                return Response(message)        
        except:
            message = {'detail': 'there is a proplem here'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)         
    if request.method == 'GET':
        user=request.user
        query=contact_form.objects.filter(user=user)
        serializer=contact_formSerializer(query,many=True)
        return Response({'detail':serializer.data})   
    if request.method == 'DELETE':

        data=request.data
        user=request.user
        form_id=data['Form_id']
        query=contact_form.objects.filter(id=form_id,user=user)
        if query.exists():
            query.delete()
            message = {'detail': 'Form is deleted successfully'}
            return Response(message)
        else:    
    
            message = {'detail': 'your Form id is incorrect'}




@api_view(['GET', 'POST','PUT','DELETE'])
def feed_edit(request):
    if request.method == 'POST' :

        try:
            data=request.data
            user=request.user
            rss_feed=data['rss_feed']
            new_feed=RSS_Feed(user=user,rss_feed=rss_feed)
            new_feed.save()
            message = {'detail': 'feed added successfully'}
            return Response(message)    
        except:
            message = {'detail': 'there is a proplem'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)     
    if request.method == 'PUT':

        try:

            data=request.data
            user=request.user
            feed_id=data['feed_id']
            query=RSS_Feed.objects.filter(user=user,id=feed_id)
            
            if query.exists():   
                if 'rss_feed ' in data:
                    rss_feed =data['rss_feed ']
                else:
                    rss_feed=query[0].rss_feed   
                      
                query.update(rss_feed=rss_feed)
                message = {'detail': 'feed was updated'}
                return Response(message)        
        except:
            message = {'detail': 'there is a proplem here'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)         
    if request.method == 'GET':
        user=request.user
        query=RSS_Feed.objects.filter(user=user)
        serializer=RSS_FeedSerializer(query,many=True)
        return Response({'detail':serializer.data})   
    if request.method == 'DELETE':

        data=request.data
        user=request.user
        feed_id=data['feed_id']
        query=RSS_Feed.objects.filter(id=feed_id,user=user)
        if query.exists():
            query.delete()
            message = {'detail': 'feed is deleted successfully'}
            return Response(message)
        else:    
    
            message = {'detail': 'your feed id is incorrect'}



@api_view(['GET', 'POST','PUT','DELETE'])
def link_edit(request):
    if request.method == 'POST' :

        try:
            data=request.data
            user=request.user
            if 'image' in data:
                code64=data['image']
                s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                otp = s.random(length=5)
                new_image=convert_base64(code64,'_Link_image',otp)

            else:
                new_image=" "    
            if 'link' in data:
                link=data['link']
            else:
                link=" "    
            if 'color ' in data:
                color =data['color ']
            else:
                color=" "    
            new_link=Link(user=user,image=new_image,link=link,color=color)
            new_link.save()
            message = {'detail': 'Link added successfully'}
            return Response(message)    
        except:
            message = {'detail': 'there is a proplem'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)     
    if request.method == 'PUT':

        try:

            data=request.data
            user=request.user
            link_id=data['link_id']
            query=Link.objects.filter(id=link_id,user=user)
            if query.exists():   
                if 'image ' in data:
                    code64=data['image']
                    s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                    otp = s.random(length=5)
                    new_image=convert_base64(code64,'_Link_image',otp)
                    
                else:
                    new_image=query[0].image  

                if 'link ' in data:
                    link =data['link ']
                else:
                    link=query[0].link   
                if 'color' in data:
                    color=data['color']
                else:
                    color=query[0].color       
                query.update(color=color,link=link,image=new_image)
                message = {'detail': 'Link was updated'}
                return Response(message)        
        except:
            message = {'detail': 'there is a proplem here'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)         
    if request.method == 'GET':
        user=request.user
        query=Link.objects.filter(user=user)
        serializer=LinkSerializer(query,many=True)
        return Response({'detail':serializer.data})   
    if request.method == 'DELETE':

        data=request.data
        user=request.user
        link_id=data['link_id']
        query=Link.objects.filter(id=link_id,user=user)
        if query.exists():
            query.delete()
            message = {'detail': 'Link is deleted successfully'}
            return Response(message)
        else:    
    
            message = {'detail': 'your Link id is incorrect'}


@api_view(['GET', 'POST','PUT','DELETE'])
def IMAGE_edit(request):
    if request.method == 'POST' :

        try:
            data=request.data
            user=request.user
            code64 = data['image']
                
            s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
            otp = s.random(length=5)
            new_image=convert_base64(code64,'_image_',otp)
            new_IMAGE=IMAGE(user=user,image=new_image)
            new_IMAGE.save()
            message = {'detail': 'IMAGE added successfully'}
            return Response(message)    
        except:
            message = {'detail': 'there is a proplem'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)     
    if request.method == 'PUT':

        try:

            data=request.data
            user=request.user
            image_id=data['link_id']
            query=IMAGE.objects.filter(id=image_id,user=user)
            if query.exists():   
                if 'image ' in data:
                    code64=data['image']
                    s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                    otp = s.random(length=5)
                    new_image=convert_base64(code64,'_image_',otp)
                    
                else:
                    new_image=query[0].image      
                query.update(image=new_image)
                message = {'detail': 'IMAGE was updated'}
                return Response(message)        
        except:
            message = {'detail': 'there is a proplem here'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)         
    if request.method == 'GET':
        user=request.user
        query=IMAGE.objects.filter(user=user)
        serializer=IMAGESerializer(query,many=True)
        return Response({'detail':serializer.data})   
    if request.method == 'DELETE':

        data=request.data
        user=request.user
        image_id=data['link_id']
        query=IMAGE.objects.filter(id=image_id,user=user)
        if query.exists():
            query.delete()
            message = {'detail': 'IMAGE is deleted successfully'}
            return Response(message)
        else:    
    
            message = {'detail': 'your IMAGE id is incorrect'}


@api_view(['GET', 'POST','PUT','DELETE'])
def product_edit(request):
    if request.method == 'POST' :

        try:
            data=request.data
            user=request.user
            if 'name' in data:
                name=data['name']
            else:
                name=" "  
            if 'image1' in data:
                code64=data['image1']
                s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                otp = s.random(length=5)
                new_image1=convert_base64(code64,'_Link_image',otp)

            else:
                new_image1=" "    
            if 'image2' in data:
                code64=data['image2']
                s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                otp = s.random(length=5)
                new_image2=convert_base64(code64,'_Link_image',otp)

            else:
                new_image2=" "  
            if 'image3' in data:
                code64=data['image3']
                s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                otp = s.random(length=5)
                new_image3=convert_base64(code64,'_Link_image',otp)

            else:
                new_image3=" "  
            if 'image4' in data:
                code64=data['image4']
                s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                otp = s.random(length=5)
                new_image4=convert_base64(code64,'_Link_image',otp)

            else:
                new_image4=" "  
            if 'image5' in data:
                code64=data['image5']
                s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                otp = s.random(length=5)
                new_image5=convert_base64(code64,'_Link_image',otp)

            else:
                new_image5=" "                  
            if 'price' in data:
                price=data['price']
            else:
                price=" "    
            if 'description ' in data:
                description =data['description ']
            else:
                description=" "    

            if 'discount ' in data:
                discount =data['discount ']
            else:
                discount=" " 
            
            if 'payment ' in data:
                payment =data['payment ']
            else:
                payment=" " 
            if 'connection ' in data:
                connection =data['connection ']
            else:
                connection=" "     
            if 'report ' in data:
                report =data['report ']
            else:
                report=" "     
            if 'info ' in data:
                info =data['info ']
            else:
                info=" "                  
            new_product=product(user=user,
            name=name,
            image1=new_image1,
            image2=new_image2,
            image3=new_image3,
            image4=new_image4,
            image5=new_image5,
            image2=new_image2,
            price=price,
            description=description,
            discount=discount,
            payment=payment,
            connection=connection,
            report=report,
            info=info
            )
            new_product.save()
            message = {'detail': 'product added successfully'}
            return Response(message)    
        except:
            message = {'detail': 'there is a proplem'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)    
    if request.method == 'PUT' :
        try:

            data=request.data
            user=request.user
            product_id=data['product_id']
            query=product.objects.filter(id=product_id,user=user)
            if query.exists():   
                if 'name' in data:
                    name=data['name']
                else:
                    name=query[0].name    
                if 'image1' in data:
                    code64=data['image1']
                    s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                    otp = s.random(length=5)
                    new_image1=convert_base64(code64,'_product_image',otp)
                    
                else:

                    new_image1=query[0].image  

                if 'image2' in data:
                    code64=data['image2']
                    s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                    otp = s.random(length=5)
                    new_image2=convert_base64(code64,'_product_image',otp)
                    
                else:

                    new_image2=query[0].image
                if 'image3' in data:
                    code64=data['image3']
                    s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                    otp = s.random(length=5)
                    new_image3=convert_base64(code64,'_product_image',otp)
                    
                else:
                    new_image3=query[0].image
                if 'image4' in data:
                    code64=data['image4']
                    s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                    otp = s.random(length=5)
                    new_image4=convert_base64(code64,'_product_image',otp)
                    
                else:
                    new_image4=query[0].image
                if 'image5' in data:
                    code64=data['image5']
                    s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
                    otp = s.random(length=5)
                    new_image5=convert_base64(code64,'_product_image',otp)
                    
                else:
                    new_image5=query[0].image                

                if 'price ' in data:
                    price =data['price ']
                else:
                    price=query[0].price   
                if 'description ' in data:
                    description =data['description ']
                else:
                    description=query[0].description   
                if 'discount ' in data:
                    discount =data['discount ']
                else:
                    discount=query[0].discount           
                if 'payment ' in data:
                    payment =data['payment ']
                else:
                    payment=query[0].payment   
                if 'connection ' in data:
                    connection =data['connection ']
                else:
                    connection=query[0].connection           
                if 'report' in data:
                    report=data['report']
                else:
                    report=query[0].report  
                if 'info' in data:
                    info=data['info']
                else:
                    info=query[0].info     

                query.update(user=user,
                name=name,
                image1=new_image1,
                image2=new_image2,
                image3=new_image3,
                image4=new_image4,
                image5=new_image5,
                image2=new_image2,
                price=price,
                description=description,
                discount=discount,
                payment=payment,
                connection=connection,
                report=report,
                info=info
                )
                message = {'detail': 'product was updated'}
                return Response(message)        
        except:
            message = {'detail': 'there is a proplem here'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST) 
    if request.method == 'GET' :
        user=request.user
        query=product.objects.filter(user=user)
        serializer=productSerializer(query,many=True)
        return Response({"detail":serializer.data})

    if request.method == 'DELETE':

        data=request.data
        user=request.user
        product_id=data['product_id']
        query=product.objects.filter(id=product_id,user=user)
        if query.exists():
            query.delete()
            message = {'detail': 'product is deleted successfully'}
            return Response(message)
        else:    
    
            message = {'detail': 'your product id is incorrect'}    






