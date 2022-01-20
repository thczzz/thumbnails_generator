import os

from celery import current_app

from django import forms
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import time
import datetime
from .tasks import make_thumbnails


class FileUploadForm(forms.Form):
    image_file = forms.ImageField(required=True)


class HomeView(View):

    def get(self, request):
        form = FileUploadForm()
        test = datetime.datetime.fromtimestamp(os.path.getctime('./media/images/aHR0cHM6Ly9zY29udGVu.zip'))
        time_elapsed = datetime.datetime.now() - test
        print(time_elapsed)
        print(datetime.timedelta(minutes=1))
        return render(request, 'home.html', {'form': form})

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        context = {}

        if form.is_valid():
            file_path = os.path.join(settings.IMAGES_DIR, request.FILES['image_file'].name)
            width = int(request.POST.get('width'))
            height = int(request.POST.get('height'))

            with open(file_path, 'wb+') as fp:
                for chunk in request.FILES['image_file']:
                    fp.write(chunk)

            task = make_thumbnails.delay(file_path, thumbnails=[(width, height)])

            context['task_id'] = task.id
            context['task_status'] = task.status

            return render(request, 'home.html', context)

        context['form'] = form

        return render(request, 'home.html', context)


class TaskView(View):

    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return JsonResponse(response_data)