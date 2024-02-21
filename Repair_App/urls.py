from django.urls import path
from .views import *

urlpatterns = [
    path('', Base, name='base'),
    path('about-us/', About, name='about'),
    path('book-appointment/', Appointment, name='book-appointment'),
    path('singleservices/', SingleService, name='singleservices'),
    path('service/', Service, name='services'),
    path('contact-us/', Contacts, name='contact'),
    path('complains/', Complains, name='complains'),
    path('', Base, name='base'),
    path('user_register/', Register, name='user_register'),
    path('user_login/', User_login, name='user_login'),
    path('user_logout/', User_logout, name='user_logout'),
    path('update_location/', Update_location, name='update_location'),
    path('payment/', Paymentt, name='payment'),
    path('consultancy/', Consultancy, name='consultancy'),
    path('swap/', Swap_deal, name='swap'),
    path('verify/<str:ref>/', Verify_payment, name='verify_payment'),
    
]