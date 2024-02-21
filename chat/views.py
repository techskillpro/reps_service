from django.shortcuts import render, redirect
from Repair_App.models import *
from .models import *
from django.contrib.auth.models import User as AppUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse


# Create your views here.

@login_required(login_url='user_login')
def Send_personal_message(request, receiver_pk):
    try:
        receiver = AppUser.objects.get(id=receiver_pk)
        users = AppUser.objects.all()
        # form = MessageForm()
        message = Message.objects.filter(sender=request.user, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=request.user) 
        message = message.order_by('datetime')

        user = request.user
        unread_count = Message.objects.filter(sender=receiver, receiver=user, is_read=False)
        general_unread_count = Message.objects.filter(receiver=user, is_read=False).count()
        general_unread = Message.objects.filter(receiver=user, is_read=False)
        # print(unread_count)
        for i in unread_count:
            i.is_read = True
            i.save()

        if request.method == 'POST':
            try:
                get_messages = request.POST.get('message')
                get_file = request.POST.get('message_file')
                get_image = request.POST.get('message_image')
                request.session['last_check_for_new_messages'] = timezone.now().isoformat()
                Message.objects.create(sender=request.user, receiver=receiver, message=get_messages, message_file=get_file, message_image=get_image)
                return redirect('chat:sendpersonalmessage', receiver_pk=receiver_pk)
            except:
                return redirect('chat:sendpersonalmessage', receiver_pk=receiver_pk)
    except:
        return HttpResponse('Error Encountered. COntact Admin For Help.')

    context = {
        'receiver' : receiver,
        'general_unread_count' : general_unread_count,
        'general_unread' : general_unread,
        'message' : message,
        'users' : users,
        # 'form' : form,
    }
    return render(request, 'personal.html', context)

@login_required(login_url='user_login')
def Chatroom(request):
    try:
        users = AppUser.objects.all()
        user = request.user
        unread_count = Message.objects.filter(receiver=user, is_read=False).count()
        unread = Message.objects.filter(receiver=user, is_read=False)
        context = {
            'users' : users,
            'unread_count' : unread_count,
            'unread' : unread,
        }
    except:
        return HttpResponse('Error Encountered. COntact Admin For Help.')
    return render(request, 'message.html', context)

@login_required(login_url='user_login')
def delete_personal_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        message.delete()
        return redirect('chat:sendpersonalmessage', receiver_pk=message.receiver.id or message.sender.id)
    except:
        return redirect('chat:sendpersonalmessage', receiver_pk=message.receiver.id or message.sender.id)

@login_required(login_url='user_login')
def edit_personal_message(request, message_id):
    try:
        new_messages = Message.objects.get(id=message_id)
        users = AppUser.objects.all()
        receiver = new_messages.receiver
        # form = MessageForm()
        message = Message.objects.filter(sender=request.user, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=request.user)
        message = message.order_by('datetime')

        if request.method=="POST":
            try:
                get_message = request.POST.get("message")
                new_messages.message=get_message
                new_messages.save()
                return redirect('chat:sendpersonalmessage', receiver_pk=new_messages.receiver.id or new_messages.sender.id)
            except:
                return redirect('chat:sendpersonalmessage', receiver_pk=new_messages.receiver.id or new_messages.sender.id)

    except:
        return HttpResponse('Error Encountered. COntact Admin For Help.')

    context ={
        'message_edit':new_messages,
        'receiver' : receiver,
        'message' : message,
        'users' : users,
    }
    return render(request, 'edit_personal_messages.html', context)