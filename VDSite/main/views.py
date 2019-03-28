from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from main.forms import UploadedFileForm
# Create your views here.


def index(request):
    return render(request, 'index.html')


def UpLoad(request):
    saved = False
    if request.method == "POST":
        # Get the posted form
        form = UploadedFileForm(request.POST, request.FILES)

        if form.is_valid():
            profile = Profile()
            profile.name = MyProfileForm.cleaned_data["name"]
            profile.picture = MyProfileForm.cleaned_data["picture"]
            profile.save()
            saved = True


    return render(request, 'saved.htmll',
                  locals())