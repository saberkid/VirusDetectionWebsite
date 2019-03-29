from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from main.query import sendQuery
# Create your views here.


def index(request):
    return render(request, 'index.html')


def UpLoad(request):
    context = {}
    if request.method == "POST" and 'userfile' in request.FILES:
        # Get the posted form
        userfile = request.FILES['userfile']
        result_list = sendQuery(userfile)
        context = {'result_list': result_list}
    return render(request, 'index.html', context)