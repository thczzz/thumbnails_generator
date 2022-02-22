# thumbnails_generator 

using Django, Celery, Redis ( With the help of [tutorial](https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/)

I also added periodic files deletion ( if a generated thumbnail.zip is older than 15 minutes it will be deleted from the server )
