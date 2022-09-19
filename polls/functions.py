from django.core.files.base import ContentFile

import base64,shortuuid


def convert_ltype(number):
    if number=="1":
        return "Social media"
    elif number=="2":
        return "Contact info"
    elif number=="3":
    
        return "For Business" 
    elif number=="4":
      
        return "Payments" 
    elif number=="6":

        return "Music" 
    else:  
        return "More" 
        



     



def convert_section(number):
    if number=="1":
        sec="username"
        return    sec
    elif number=="2":
        sec="link"
        return    sec
    

def convert_base64(code64,name1,name2):    
       
            s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
            otp = s.random(length=5)
            var=code64.split('/')[1]
            image_name =  otp+  '.'+var.split(';')[0]

            extension = image_name.split('.')[1].lower()

            image_name = '{}_{}.{}'.format( name1 , name2, extension)

            imgStr = code64.split(';base64')

            new_image = ContentFile(base64.b64decode(imgStr[1]), name=image_name)

            return new_image