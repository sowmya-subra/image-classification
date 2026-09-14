from django.shortcuts import render


def writeup(request):
    return render(request, "writeup.html")