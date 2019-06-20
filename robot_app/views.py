import os
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'robot_app/index.html')


def upload(request):
    # print(request.POST)
    file_name = os.path.join('cache', request.POST['name'])
    file = request.FILES['file']

    with open(file_name, 'wb') as f:
        f.write(file.read())

    return render(request, 'robot_app/index.html')