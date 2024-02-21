from . import views
from django.urls import path

app_name='chat'
urlpatterns = [
    path('all_chat/', views.Chatroom, name='chat_room'),
    # path('room/<str:group_name>/<int:group_pk>', views.GroupChat, name='room'),
    # path('delete_message/<message_id>/', views.delete_message, name='delete_message'),
    # path('edit_message/<message_id>', views.edit_message, name='edit_message'),
    path('delete_personal_message/<message_id>/', views.delete_personal_message, name='delete_messagess'),
    path('edit_personal_message/<message_id>', views.edit_personal_message, name='edit_messagess'),
    path('personal_chat/<int:receiver_pk>/', views.Send_personal_message, name='sendpersonalmessage'),
]
