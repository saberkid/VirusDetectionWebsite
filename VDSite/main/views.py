from django.shortcuts import render
from main.tasks import send_notification, send_query
# Create your views here.


def index(request):
    return render(request, 'index.html')


def UpLoad(request):
    context = {}
    if request.method == "POST" and 'userfile' in request.FILES:
        # Get the posted form
        userfile = request.FILES['userfile']
        email = request.POST.get('email', None)
        result_list = send_query(userfile)
        # Send notification email
        if email:
            send_notification(email)
        context = {'result_list': result_list}
    return render(request, 'index.html', context)