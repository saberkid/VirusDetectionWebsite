# FortinetRemote
This is a web application that allows users to upload a text
file as a list of hashes (MD5 or Sha256) and generates a simple report using
information provided by querying VirusTotal's public API for the scan report of the hashes.

The project is developed based on [Djiango](https://www.djangoproject.com/)'s framework.
## Features
* Users' query results are cached (into main memory by default) to facilitate frequent query.
* Users can also be notified by emails when the query is done. (see Issues for setup instructions)
## Denpendencies
* python==3.x (Let's move on to python 3 if you still use python 2)
* django==2.1.7
```
pip install django
```
* requests
```
pip install requests
```

## Run
* Switch to the project folder
```
cd VDSite
```
* run the following command
```
python manager.py runserver 0.0.0.0:8000
```
* Go to http://localhost:8000 in your browser, and you will see the website as required.
## Layout of the project
```
main/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py # defines the query result model
    tests.py
    urls.py # defines the url mapping
    views.py # defines the view rendering functions
    templates/
        index.html # the home page
    tasks.py  # defines web tasks such as sending query and email notifications
    query.py  # defines the query operation
    
 VDSite/
     __init__.py
     settings.py # defines global setting of the server
     urls.py
     wsgi.py
```

## Issues
1. API's daily limit

Since the Public API is limited to 4 requests per minute on `virustotal.com`, the query is sleeped every 20 seconds.

2. Test mode

For fast verification, only up to 5 hashed values are tested. To disable the test mode, set `mode` to strings other than `'test'` in function `send_query` located in [main/task.py](VDSite/main/tasks.py).

3. Email notification

To enable the email notification, set `EMAIL_HOST , EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_FROM ` at the end of [VDSite/settings.py](VDSite/VDSite/settings.py)

4. Cache options

The cache is placed into main memory by default. There are also many other options in Django. For example, to enable a database caching, comment out the following in [VDSite/settings.py](VDSite/VDSite/settings.py)
```
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 60 * 60 * 24, # TIMEOUT after 1 day
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
```
Uncomment
```
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'main_query_result',
#         'TIMEOUT': 60 * 60 * 24, # TIMEOUT after 1 day
#         'OPTIONS': {
#             'MAX_ENTRIES': 100000
#         }
#     }
# }
```
Then run the following commands:
```
python manager.py makemigrations
python manager.py migrate
```
For more information on django's cache mechanism, visit [here](https://docs.djangoproject.com/en/2.1/topics/cache/)

## TODO lists
* Check the validicity of user's email address input.
* Check the format and size of the user upload. 
* Paging if the query result is too long. (More of a front end job, not fulfilled here)
* Using asynchronized operations to update the webpage with partial results. (In Djiango, implementation of async requests depends on different brokers. Not fulfilled here for the easy deployment of the project)
