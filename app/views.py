import os
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render
from pytube import *


# def get(request):
#     return render(request, 'index.html')

def index(request):
    user_dir = os.path.expanduser("~") + '/Downloads/'

    if request.POST.get('fetch-vid'):
        url = request.POST.get('given_url')
        video = YouTube(url)
        vid_title = video.title
        vid_thumbnail = video.thumbnail_url
        quality, stream = [], []

        for vid in video.streams.filter(progressive=True):
            quality.append(vid.resolution)
            stream.append(vid)

        context = {
            'vid_title': vid_title, 'vid_thumbnail': vid_thumbnail, 'quality': quality, 'stream': stream, 'url': url
        }

        return render(request, 'index.html', context)
    
    elif request.POST.get('download-vid'):
        url = request.POST.get('given_url')
        video = YouTube(url)
        stream = [x for x in video.streams.filter(progressive=True)]
        video_qual = video.streams[int(request.POST.get('download-vid')) - 1]
        video_qual.download(output_path = user_dir, filename = "video.mp4")
        file = FileWrapper(open(f'{user_dir}/video.mp4', 'rb'))
        response = HttpResponse(file, content_type = 'application/vnd.mp4')
        response['Content-Disposition'] = f'attachment; filename = "{video.title}.mp4"'
        os.remove(f'{user_dir}/video.mp4')
        return response

    return render(request,'index.html')
