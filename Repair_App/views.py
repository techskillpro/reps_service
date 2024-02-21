from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.conf import settings
from geopy.geocoders import Nominatim
from django.http import JsonResponse
from django.core.mail import send_mail

# Create your views here.

def Base(request):
    try:
        cards = Service_Card.objects.all()
        if request.user.is_authenticated:
            try:
                if request.user.customer:
                    #get the address of the user from the latitude.
                    latitude = request.user.customer.latitude
                    longitude = request.user.customer.longitude
                    if latitude and longitude:
                        try:
                            geoLocation = Nominatim(user_agent='Repair_App')
                            Location_address = geoLocation.reverse(
                                f"{latitude}, {longitude}",
                                timeout=5000, 
                                language = 'en', 
                                zoom=18, 
                                addressdetails= True,
                            )
                            address = Location_address.address
                        except:
                            pass
                    else:
                        pass
                else:
                    pass
            except:
                pass
    except:
        return HttpResponse('Error encountered, Contact Admin For Help')
    return render(request, 'index.html', {'cards':cards})

def Update_location(request):
    if request.method == 'POST' and request.user.is_authenticated:
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        try:
            geoLocation = Nominatim(user_agent='Repair_App')
            Location_address = geoLocation.reverse(
                f"{latitude}, {longitude}",
                timeout=5000, 
                language = 'en', 
                zoom=18, 
                addressdetails= True,
            )
            address = Location_address.address
        except:
            pass
        
        # Do something with the location data, e.g., save it to the user's profile
        request.user.customer.latitude = latitude
        request.user.customer.longitude = longitude
        request.user.customer.gps_location = Location_address
        request.user.customer.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

def map(request, customer_id):
    try:
        customer = models.Customer.objects.get(id=customer_id)
        latitude = customer.latitude
        longitude = customer.longitude

        if latitude and longitude:
            try:
                geoLocation = Nominatim(user_agent='Repair_App')
                Location_address = geoLocation.reverse(
                    f"{latitude}, {longitude}",
                    timeout=5000, 
                    language = 'en', 
                    zoom=18, 
                    addressdetails= True,
                )
                address = Location_address.address
            except:
                pass
        context = {
            'latitude' : latitude,
            'longitude' : longitude,
            'address' : address
        }
        # return render(request, 'ecom/map3.html', context)
        return HttpResponse('Hi')
    except:
        return HttpResponse('Error encountered. Contact Admin For Help')

def About(request):
    return render(request, 'about-us.html')

def Complains(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            complain = request.POST.get('message')

            contact = Complain.objects.create(
                name = name,
                email = email,
                subject = subject,
                complains = complain,
            )
            
            contact.save()
            return HttpResponse('Successfully sent')
        except:
            return HttpResponse('Error encountered. Contact Admin For Help')
    
    else:
        return render(request, 'complain.html')

def Contacts(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            contact = Contact.objects.create(
                name = name,
                email = email,
                subject = subject,
                message = message,
            )
            
            contact.save()
            return HttpResponse('Successfully sent')
        except:
            return HttpResponse('Error encountered. Contact Admin For Help')

    return render(request, 'contact.html')

@login_required(login_url='user_login')
def Appointment(request):
    if request.method == 'POST':
        try:
            model = request.POST.get('model')
            gadget_imei = request.POST.get('gadget_imei')
            purchase_date = request.POST.get('purchase_date')
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.POST.get('image3')
            description = request.POST.get('description')

            new_repair = Repair_Details.objects.create(
                customer = request.user.customer,
                gadget_model = model,
                gadget_IMEI = gadget_imei,
                purchase_date = purchase_date,
                complaint_description = description,
                gadget_image1 = image1,
                gadget_image2 = image2,
                gadget_image3 = image3,
            )
            
            new_repair.save()
            return HttpResponse('Repair Details successfully sent')
        except:
            return HttpResponse('Error encountered. Contact Admin For Help')

    return render(request, 'appointment.html')

def Service(request):
    try:
        plans = Plan.objects.all()
        cards = Service_Card.objects.all()
        context={
            'plans': plans,
            'cards': cards,
        }
        return render(request, 'service.html', context)
    except:
        return HttpResponse('Error encountered. Contact Admin For Help')

def SingleService(request):
    return render(request, 'service-details.html')


@login_required(login_url='user_login')
def Consultancy(request):
    if request.method == 'POST':
        try:
            amount=500
            if request.user.is_authenticated:
                customer=request.user.customer
                consultation = Consultation.objects.create(
                    customer=customer,
                    name=customer.user.first_name+customer.user.last_name+customer.user.username,
                    email=customer.user.email,
                    phone_number=customer.phone_number,
                    subject = request.POST.get('subject'),
                    complains = request.POST.get('message'),
                )

                paid = Payment.objects.create(
                    user = request.user,
                    email=consultation.email,
                    amount = amount,
                    consultation_id = consultation,
                    payment_reason = 'Consultation Payment',
                )
                paid.save()
                consultation.ref = paid.ref
                consultation.save()
                
            else:
                consultation = Consultation.objects.create(
                    name = request.POST.get('name'),
                    email = request.POST.get('email'),
                    phone_number = request.POST.get('phone_num'),
                    subject = request.POST.get('subject'),
                    complains = request.POST.get('message'),
                )

                paid = Payment.objects.create(
                    email=consultation.email,
                    amount = amount,
                    consultation_id = consultation,
                    payment_reason = 'Consultation Payment',
                )
                paid.save()
                consultation.ref = paid.ref
                consultation.save()

            return render(
                request,
                'make_pay.html',
                {
                    'amount' : 500,
                    'paystack_public_key' : settings.TEST_PAYSTACK_PUBLIC_KEY,
                    'payment' : paid,
                }
            )    
        except:
            return HttpResponse('Error encountered. Contact Admin For Help')
        
    return render(request, 'consultancy.html')
    

def Paymentt(request):
    form = PaymentForm()
    if request.method == 'POST':
        try:
            form = PaymentForm(request.POST)
            plan_id = request.POST.get('plan')
            plan = Plan.objects.get()
            
            paid = Payment.objects.create(
                repair_detail = request.POST.get('repair_detail'),
                email = request.POST.get('email'),
                amount = plan.price,
                payment_reason = request.POST.get('payment_reason'),
                plan=plan,
            )
            
            request.user.customer.plan = plan
            request.user.customer.save()
                    
            paid.save()
            return render(
                request,
                'make_pay.html',
                {
                    'amount' : plan.price,
                    # 'paystack_public_key' : settings.PAYSTACK_PUBLIC_KEY,
                    'paystack_public_key' : settings.TEST_PAYSTACK_PUBLIC_KEY,
                    # 'test_paystack_public_key' : 'pk_test_127d9bffed44d7947d26e7f19ca20d963f286b6e',
                    'payment' : paid,
                }
            )
        except:
            return HttpResponse('Error encountered. Contact Admin For Help')
    
    return render(request, 'init_pay.html', {'form':form})

    
def Verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    #    error_side  
    try:
        payment = get_object_or_404(Payment, ref=ref)

        verified = payment.verify_payment()
        if verified:
            messages.success(request, 'Verification and Payment Successful')
            try:
                consult = get_object_or_404(Consultation, ref=ref)
                messages.success(request, "Consultation Requests Successfully Sent")
                subject = 'Consultation Reply'
                message = f'Hi {payment.user.last_name} {payment.user.first_name}, Payment for consultation Received, We will get back to you later for feedback.'
                email_from = settings.EMAIL_HOST_USER
                receipient_email = [payment.email,]
                a = send_mail(subject, message, email_from, receipient_email)
                print(a)
            except:
                print('Error sending Mail...\nInternet connection needed')

            return redirect('base')

        else: 
            messages.error(request, 'Verification and Payment Failed')
            return redirect('payment')
    except:
        return HttpResponse('Error encountered. Contact Admin For Help')


def Register(request):
    if request.method == 'POST':
        try:
            Userform = UserRegisterForm(request.POST)
            Customerform = CustomerForm(request.POST)
            
            if Userform.is_valid() and Customerform.is_valid():
                user = Userform.save()
                username = Userform.cleaned_data['username']
                user.email = username
                user.save()
                print(username)
                customer = Customerform.save()
            
                #Saves user instance to customer
                customer.user = user
                customer.save()
                messages.success(request, 'Registration Successful!!')
                return redirect('user_login')
            else:
                messages.error(request, 'Error encountered in registration')
        except:
            return HttpResponse('Error encountered. Contact Admin For Help')
            
    else:
        Userform = UserRegisterForm()
        Customerform = CustomerForm()

    context = {
        'Userform' : Userform,
        'Customerform' : Customerform,
    }
    return render(request, 'register.html', context)


def User_login(request):
    if request.method == "POST":
        try:
            username = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                login(request,user)
                messages.success(request, 'Successfully Logged in!!')
                return redirect('base')

            else:
                return HttpResponse('Error Logging in')
        except:
            return HttpResponse('Error encountered. Contact Admin For Help')

    else:
        return render(request, 'login.html')


@login_required(login_url='user_login')
def User_logout(request):
    try:
        logout(request)
        if logout:
            messages.success(request, 'Successfully Logged out!!')
            return redirect('base')
        else:
            messages.error(request, 'Failed to log out!!')
            return redirect('base')
    except:
        return HttpResponse('Error encountered. Contact Admin For Help')
    
@login_required(login_url='user_login')
def Swap_deal(request):
    if request.method == 'POST':
        try:
            swap = Swap_Deal.objects.create(
                user=request.user.customer,
                item_name = request.POST.get('item_swap'),
                item_description = request.POST.get('detail'),
                item_needed = request.POST.get('item_needed'),
                item_pic1 = request.FILES.get('image1'),
                item_pic2 = request.FILES.get('image2'),
                item_pic3 = request.FILES.get('image3'),
                item_pic4 = request.FILES.get('image4'),
                item_pic5 = request.FILES.get('image5'),
            )
            swap.save()
            messages.success(request, "Swap Deal successfully sent")
            
            try:
                subject = 'Swap Deal Received'
                message = f'Hi {request.user.first_name} {request.user.last_name}, Swap Deal received, We will get back to you later for feedback.'
                email_from = settings.EMAIL_HOST_USER
                receipient_email = [swap.user.email,]
                a = send_mail(subject, message, email_from, receipient_email)
            except:
                print('Error sending Mail...\nInternet connection needed')
        except:
            return HttpResponse('Error encountered. Contact Admin For Help')

    return render(request, 'swap.html')