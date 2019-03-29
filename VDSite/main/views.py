from django.shortcuts import render
from main.tasks import send_notification, send_query
# Create your views here.


def index(request):
    return render(request, 'index.html')


def upLoad(request):
    context = {}
    if request.method == "POST" and 'userfile' in request.FILES:
        userfile = request.FILES['userfile']    # Get the posted form
        email = request.POST.get('email', None)
        result_list = send_query(userfile)
        if email:    # Send notification email
            send_notification(email)
        context = {'result_list': result_list}
    return render(request, 'index.html', context)