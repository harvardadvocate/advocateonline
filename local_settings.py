
from django.utils.crypto import get_random_string 
chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)' 
SECRET_KEY = get_random_string(50, chars)
DEBUG = True 
DATABASES = { 'default': { 'ENGINE': 'django.db.backends.mysql', 'NAME': 'advocate', 'USER': 'root', 'PASSWORD': '', 'HOST': 'localhost' } }
