from django.shortcuts import render
from main.tasks import send_notification, send_query
# Create your views here.


def index(request):
    return render(request, 'index.html')


def upload(request):
    context = {}
    if request.method == "POST" and 'userfile' in request.FILES:
        userfile = request.FILES['userfile']    # Get the posted form
        filename = request.FILES['userfile'].name    # Get the filename
        email = request.POST.get('email', None)
        result_list = send_query(userfile)
        if email:    # Send notification email
            send_notification(email)

        context = {'result_list': result_list, 'filename': filename}
    return render(request, 'report.html', context)