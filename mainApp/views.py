from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Receptionist, Visitor, VisitReason
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages

def loginpage(request):
    if request.method=='POST':
        email= request.POST.get('email')    #taking username value from html login page
        password= request.POST.get('password')
        print(email)
        print(password)
        try:    #--> to resolve runtime errors,[when we try to fetch record from database sometimes it may raise errors if user record does not exist so to handle this errors we use try and except]
            recep = Receptionist.objects.get(email=email, password=password)  
            print(password) #to fetch data from database where name and password should be matched 
            print(recep)
            if recep:
                print(recep)
                user = authenticate(username=email, password=password)
                if user:
                    print("Authenticated User : ", user)
                    login(request, user)
                    request.session['recep'] = email
               
                    return redirect("/")
                else:
                    user = User.objects.create(username=email)
                    user.set_password(password)
                    user.save()
                    user = authenticate(username=email, password=password)
                    login(request, user)
                    request.session['recep'] = email
                    return redirect("/")
            else:
                return redirect("/login")
        except:
            messages.error(request, 'Please Enter Details Correctly!')
            return redirect("/login") 
    return render(request, 'login.html')


def logoutpage(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@login_required(login_url="/login/")
def indexpage(request):
    tvisitors = Visitor.objects.count()
    bvisits = Visitor.objects.filter(purpose=1).count()
    pvisits = Visitor.objects.filter(purpose=2).count()
    jvisits = Visitor.objects.filter(purpose=3).count()
    latest_visits = Visitor.objects.filter().order_by('-id')[:10]
    return render(request, 'index.html', {'total_visits':tvisitors, 'bvisits':bvisits, 'pvisits':pvisits, 'jvisits':jvisits, 'latest_visits':latest_visits})


@login_required(login_url="/login/")
def visitorpage(request):
    tvisitors = Visitor.objects.count()
    bvisits = Visitor.objects.filter(purpose=1).count()
    pvisits = Visitor.objects.filter(purpose=3).count()
    jvisits = Visitor.objects.filter(purpose=2).count()
    visitors = Visitor.objects.filter().order_by('id')
    return render(request, 'visitor.html', {'total_visits':tvisitors, 'bvisits':bvisits, 'pvisits':pvisits, 'jvisits':jvisits, 'visitors':visitors})



@login_required(login_url="/login/")
def updateRecepPage(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y-%m-%d")
        r = Receptionist.objects.get(id=id)
        r.name = name
        r.phone = phone
        r.email = email
        r.address = address
        r.city = city
        r.state = state
        # r = Receptionist(id=id, name=name, phone=phone, email=email, address=address, city=city, state=state, date_of_creation=formatted_date)
        r.save()
        messages.success(request, 'Data is updated successfully!')
        return redirect("/viewRecptionist/")
    data = Receptionist.objects.get(id=id)
    return render(request, 'update-recep.html', {'recep':data})


@login_required(login_url="/login/")
def removeRecepPage(request, id):
    latest_visited_url = request.META.get('HTTP_REFERER', None)
    data = Receptionist.objects.get(id=id)
    data.delete()
    return redirect(latest_visited_url)


@login_required(login_url="/login/")
def updateVisitorPage(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        to_meet = request.POST.get('to_meet')
        purpose = request.POST.get('purpose')
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y-%m-%d")
        purpose = VisitReason.objects.get(id=int(purpose))
        v = Visitor(id=id, name=name, email=email, phone=phone, address=address, to_meet=to_meet, purpose=purpose, date_of_visit=formatted_date)
        v.save()
        messages.success(request, 'Data is updated successfully')
        return redirect("/visitor/")
    data = Visitor.objects.get(id=id)
    visitReason = VisitReason.objects.all()
    return render(request, 'update-visitor.html', {'v':data, 'visitReason':visitReason})


@login_required(login_url="/login/")
def removeVisitorPage(request, id):
    latest_visited_url = request.META.get('HTTP_REFERER', None)
    data = Visitor.objects.get(id=id)
    data.delete()
    return redirect(latest_visited_url)


@login_required(login_url="/login/")
def addReceptionist(request):
    if request.method == 'POST':
        if request.POST.get('password') != request.POST.get('cpassword'):
            messages.error(request, 'Both Passwords must be same.')
            return redirect("/add-receptionist/")

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        password = request.POST.get('password')
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y-%m-%d")
        r = Receptionist(name=name, phone=phone, email=email, address=address, city=city, state=state, date_of_creation=formatted_date, password=password)
        r.save()
        # messages.success(request, 'Data is stored successfully!')
        return redirect("/viewRecptionist/")
    return render(request, 'add-receptionist.html')


@login_required(login_url="/login/")
def view_Receptionist(request):
    r = Receptionist.objects.all()
    tvisitors = Visitor.objects.count()
    bvisits = Visitor.objects.filter(purpose=1).count()
    pvisits = Visitor.objects.filter(purpose=3).count()
    jvisits = Visitor.objects.filter(purpose=2).count()
    # return render(request, 'viewRecptionist.html')
    return render(request, 'viewRecptionist.html', {'total_visits':tvisitors, 'bvisits':bvisits, 'pvisits':pvisits, 'jvisits':jvisits, 'receps':r})


@login_required(login_url="/login/")
def addnewVisitor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        to_meet = request.POST.get('to_meet')
        purpose = request.POST.get('purpose')
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y-%m-%d")
        purpose = VisitReason.objects.get(id=int(purpose))
        v = Visitor(name=name, email=email, phone=phone, address=address, to_meet=to_meet, purpose=purpose, date_of_visit=formatted_date)
        v.save()
        messages.success(request, 'Data is Stored')
        return redirect("/add-new-visitor/")
    
    tvisitors = Visitor.objects.count()
    bvisits = Visitor.objects.filter(purpose=1).count()
    pvisits = Visitor.objects.filter(purpose=3).count()
    jvisits = Visitor.objects.filter(purpose=2).count()
    visitReason = VisitReason.objects.all()
    return render(request, 'add-new-visitor.html', {'visitReason':visitReason, 'total_visits':tvisitors, 'bvisits':bvisits, 'pvisits':pvisits, 'jvisits':jvisits})


@login_required(login_url="/login/")
def BusinessVisit(request):
    tvisitors = Visitor.objects.count()
    bvisits = Visitor.objects.filter(purpose=1).count()
    pvisits = Visitor.objects.filter(purpose=3).count()
    jvisits = Visitor.objects.filter(purpose=2).count()
    purpose = VisitReason.objects.get(id=1)
    busi_visits = Visitor.objects.filter(purpose=purpose)
    return render(request, 'buisenessVisit.html', {'busi_visits':busi_visits, 'total_visits':tvisitors, 'bvisits':bvisits, 'pvisits':pvisits, 'jvisits':jvisits})
    # return render(request, 'buisenessVisit.html')


@login_required(login_url="/login/")
def personalVisit(request):
    tvisitors = Visitor.objects.count()
    bvisits = Visitor.objects.filter(purpose=1).count()
    pvisits = Visitor.objects.filter(purpose=3).count()
    jvisits = Visitor.objects.filter(purpose=2).count()
    purpose = VisitReason.objects.get(id=3)
    personal = Visitor.objects.filter(purpose=purpose)
    return render(request, 'personalVisitor.html', {'personal':personal, 'total_visits':tvisitors, 'bvisits':bvisits, 'pvisits':pvisits, 'jvisits':jvisits})
    # return render(request, 'personalVisitor.html')


@login_required(login_url="/login/")
def jobVisit(request):
    tvisitors = Visitor.objects.count()
    bvisits = Visitor.objects.filter(purpose=1).count()
    pvisits = Visitor.objects.filter(purpose=3).count()
    jvisits = Visitor.objects.filter(purpose=2).count()
    purpose = VisitReason.objects.get(id=2)
    job_visits = Visitor.objects.filter(purpose=purpose)
    return render(request, 'job-visit.html', {'job_visits':job_visits, 'total_visits':tvisitors, 'bvisits':bvisits, 'pvisits':pvisits, 'jvisits':jvisits})


@login_required(login_url="/login/")
def viewProfile(request):
    if request.session.get('recep'):
        r = Receptionist.objects.get(email = request.session.get('recep'))
        tvisitors = Visitor.objects.count()
        bvisits = Visitor.objects.filter(purpose=1).count()
        pvisits = Visitor.objects.filter(purpose=3).count()
        jvisits = Visitor.objects.filter(purpose=2).count()
        return render(request, 'view-profile.html', {'recep':r, 'total_visits':tvisitors, 'bvisits':bvisits, 'pvisits':pvisits, 'jvisits':jvisits})
    return HttpResponseRedirect("/login/")
