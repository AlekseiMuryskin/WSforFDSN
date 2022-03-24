from django.shortcuts import render

# Create your views here.

def main_page(request):
    return render(request,'fdsnws/main_page.html',{})

def dataselect(request):
    return render(request,'fdsnws/dataselect.html',{})

def station(request):
    return render(request,'fdsnws/station.html',{})



