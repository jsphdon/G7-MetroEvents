from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import CreateUserForm
from .models import User, Comment, Event, Organizer, Request


def format_date(objects):
    for object in objects:
        object.start_date = object.start_date.strftime("%Y-%m-%d")
        object.end_date = object.end_date.strftime("%Y-%m-%d")

#! REGISTER PAGE


class RegisterPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account:myaccount')
        form = CreateUserForm()

        context = {'form': form}
        return render(request, 'register.html', context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(
                request, 'Account was created for ' + username)

            return redirect('account:login')

        context = {'form': form}
        return render(request, 'register.html', context)


#! LOGIN PAGE
class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                return redirect('account:myaccount')
            elif request.user.is_superuser:
                return redirect('account:administrator')
            elif request.user.is_staff:
                return redirect('account:organizer')
            else:
                return redirect('account:myaccount')
        else:
            return render(request, "login.html")

    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(
                request, username=username, password=password)

            if user is not None:
                login(request, user)
                if not user.is_staff:
                    return redirect('account:myaccount')
                elif user.is_superuser:
                    return redirect('account:administrator')
                elif user.is_staff:
                    return redirect('account:organizer')
                else:
                    return HttpResponse("ERROR")
            else:
                messages.info(request, 'Username OR password is incorrect')

            return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('account:login')

#! USER PAGE


@method_decorator(login_required, name='dispatch')
class HomePage(View):
    def get(self, request):
        if request.user.is_superuser:
            return redirect('account:administrator')
        elif request.user.is_staff:
            return redirect('account:organizer')
        elif not request.user.is_staff:
            myEvents = Event.objects.filter(participants=request.user)
            events = Event.objects.exclude(participants=request.user)
            context = {
                'myEvents': myEvents,
                'events': events,
            }
            return render(request, 'useraccount.html', context)
        else:
            return HttpResponse("Error")

    def post(self, request):
        if 'request_joinbtn' in request.POST:
            eventid = request.POST.get('event-id')
            print()
            req = Request.objects.filter(
                user=request.user, requestType="Join Event", event_id=eventid)
            if req:
                messages.info(
                    request, "You have already requested to join the event.")
                return redirect('account:user')
            reqJoin = Request.objects.create(
                user=request.user, requestType="Join Event", event_id=eventid)

            messages.info(
                request, "You have requested to join the event, you will received a notification once the organizer approve your request.")

        elif 'request_orgbtn' in request.POST:
            print(request.user.id)
            req = Request.objects.filter(
                user=request.user, requestType="Promote to Organizer")
            if req:
                messages.info(
                    request, "You have already requested to become an organizer.")
                return redirect('account:myaccount')
            reqOrg = Request.objects.create(
                user=request.user, requestType="Promote to Organizer")

            messages.info(
                request, "Request sent, once organizer, you will be redirected to the organizer page")
        elif 'submitUpvote' in request.POST:
            myeventid = request.POST.get('myevent-id')
            event = Event.objects.get(id=myeventid)

            btnradio = request.POST.get('btnradio')

            if btnradio == "upvote":
                event.upvotes = event.upvotes + 1
                event.save()
            elif btnradio == "downvote":
                event.upvotes = event.upvotes - 1
                event.save()
            messages.info(request, 'Upvote submitted successfully!')
        elif 'submitComment' in request.POST:
            myeventid = request.POST.get('myevent-id')
            event = Event.objects.get(id=myeventid)

            comments = request.POST.get('comment')
            print(comments)

            comment = Comment.objects.update(comment=comments)
            event.comment.add(comment)
            event.save()
            messages.info(request, 'Comment submitted successfully!')
        return redirect('account:myaccount')


#! Admin Page
@method_decorator(login_required, name='dispatch')
class AdminPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            currentUser = request.user
            if currentUser.is_superuser:
                requests = Request.objects.filter(
                    requestType="Promote to Organizer", status="Reviewing")
                events = Event.objects.all()
                users = User.objects.all()
                organizers = Organizer.objects.all()
                print(requests)
                context = {
                    'users': users,
                    'events': events,
                    'organizers': organizers,
                    'requests': requests,
                }
                return render(request, 'adminAccount.html', context)
            elif not currentUser.is_staff:
                return redirect('account:myaccount')
            elif currentUser.is_staff:
                return redirect('account:organizer')
            else:
                return redirect('account:login')

        return redirect('account:login')

    def post(self, request):
        if 'requestorg_acceptbtn' in request.POST:
            userid = request.POST.get("user-id")
            requestid = request.POST.get("request-id")
            print(userid)
            print(requestid)
            req = Request.objects.get(id=requestid)
            organizer = Organizer.objects.create(organizer_id=userid)
            req.status = "Accept"
            req.date_replied = datetime.now()
            req.replied_by = request.user
            user = req.user
            user.is_staff = True
            organizer.save()
            req.save()
            user.save()
        if 'requestorg_declinebtn' in request.POST:
            print("Request to be an organizer, DECLINED")
            req = Request.objects.get(id=request.POST.get("request-id"))
            req.status = "Decline"
            req.date_replied = datetime.now()
            req.replied_by = request.user
            req.save()

        if 'EditBtn' in request.POST:
            id = request.POST.get("event_id")
            event_type = request.POST.get("event_type")
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            Event.objects.filter(id=id).update(
                event_type=event_type, start_date=start_date, end_date=end_date)
        elif 'DeleteBtn' in request.POST:
            print('Deleted Event')
            id = request.POST.get("event_id")
            Event.objects.filter(id=id).delete()
        return redirect('account:administrator')

#! ORGANIZER PAGE


@method_decorator(login_required, name='dispatch')
class OrganizerPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            currentUser = request.user
            if currentUser.is_superuser:
                return redirect('account:administrator')
            elif currentUser.is_staff:
                organizer = Organizer.objects.get(organizer_id=currentUser)
                myEvents = Event.objects.filter(organizer=organizer)

                requests = Request.objects.filter(
                    event_id__in=myEvents, status="Reviewing")

                format_date(myEvents)
                context = {
                    'myEvents': myEvents,
                    'requests': requests,
                }
                return render(request, 'organizerAccount.html', context)
            elif not request.user.is_staff:
                return redirect('account:myaccount')
            else:
                return HttpResponse("Error")
        return redirect('account:login')

    def post(self, request):
        organizer = request.user
        if request.method == 'POST':
            if 'EditBtn' in request.POST:
                id = request.POST.get("event_id")
                event_type = request.POST.get("event_type")
                start_date = request.POST.get("start_date")
                end_date = request.POST.get("end_date")
                Event.objects.filter(id=id).update(
                    event_type=event_type, start_date=start_date, end_date=end_date)
            elif 'DeleteBtn' in request.POST:
                print('Deleted Event')
                id = request.POST.get("event_id")
                Event.objects.filter(id=id).delete()
            elif 'acceptRequestbtn' in request.POST:
                event = Event.objects.get(id=request.POST.get("event_id"))
                req = Request.objects.get(id=request.POST.get("request_id"))
                user = User.objects.get(id=request.POST.get("user_id"))
                event.participants.add(user)
                req.replied_by = organizer
                req.date_replied = datetime.now()
                req.status = "Accept"
                req.save()
            elif 'denyRequestbtn' in request.POST:
                req = Request.objects.get(id=request.POST.get("request-id"))
                req.replied_by = organizer
                req.date_replied = datetime.now()
                req.status = "Decline"
                req.save()
            return redirect('account:organizer')


#! ADD EVENT PAGE
class AddEvent(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
                return render(request, 'addEvent.html')
            else:
                return HttpResponse("Error")
        return redirect('account:login')

    def post(self, request):
        organizer = Organizer.objects.get(organizer_id=request.user)
        event_type = request.POST.get("event_type")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        event = Event.objects.create(event_type=event_type,
                                     start_date=start_date, end_date=end_date)
        organizer.event.add(event)

        print("Event successfully created.")
        messages.info(request, 'An event ' + event_type + ' has been created')
        if request.user.is_superuser:
            return redirect('account:administrator')
        elif request.user.is_staff:
            return redirect('account:organizer')
        else:
            return redirect('account:login')
