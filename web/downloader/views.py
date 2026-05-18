from django.http import HttpResponse


def index(request):
    return HttpResponse("Downloader web interface is running.")