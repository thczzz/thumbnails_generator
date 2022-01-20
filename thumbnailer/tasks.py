import os
from zipfile import ZipFile
from celery import shared_task
from celery.schedules import crontab
from core.celery import celery_app
from core.celery import task
from PIL import Image
from celery.contrib import rdb
from datetime import datetime, timedelta

from django.conf import settings


@shared_task
def make_thumbnails(file_path, thumbnails=[]):
    os.chdir(settings.IMAGES_DIR)
    path, file = os.path.split(file_path)
    file_name, ext = os.path.splitext(file)

    zip_file = f"{file_name}.zip"
    results = {'archive_path': f"{settings.MEDIA_URL}images/{zip_file}"}
    try:
        img = Image.open(file_path)
        zipper = ZipFile(zip_file, 'w')
        # rdb.set_trace() - celery breakpoint
        # zipper.write(file) - original file..

        for w, h in thumbnails:
            img_copy = img.copy()
            img_copy.thumbnail((w, h))
            thumbnail_file = f'{file_name}_{w}x{h}.{ext}'
            img_copy.save(thumbnail_file)
            zipper.write(thumbnail_file)

            os.remove(thumbnail_file)

        img.close()
        zipper.close()
        os.remove(file_path)

    except IOError as err:
        print(err)

    return results


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/5"),
        delete_stored_files.s()
    )


@task
def delete_stored_files():
    for subdir, dirs, files in os.walk(settings.IMAGES_DIR):
        for file in files:
            filepath = subdir + os.sep + file
            get_creation_time = datetime.fromtimestamp(os.path.getctime(filepath))
            time_elapsed = datetime.now() - get_creation_time
            limit = timedelta(minutes=15)
            if time_elapsed > limit:
                os.remove(filepath)
