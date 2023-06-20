from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from time import sleep

def index(request):
    if request.method == "GET":
        return render(request, 'main/index.html')
    elif request.method == "POST":
        return redirect('output')


def output(request):
    context = {
        'pres': 'pres.pptx',
        'video': 'video.mp4'
    }
    return render(request, 'main/output.html', context=context)


def file_view(request, filename):
    sleep(6)
    try:
        filedir = 'files/'
        with open(filedir + filename, 'rb') as f:
            file_data = f.read()
            # sending response
            response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    except IOError:
        # handle file not exist case here
        response = HttpResponseNotFound('<h1>File not exist</h1>')

    return response