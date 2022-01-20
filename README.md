# thumbnails_generator 

using Django, Celery, Redis ( With the help of this tutorial - https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/ )

I also added periodic files deletion ( if a generated thumbnail is older than 15 minutes it will be deleted )
