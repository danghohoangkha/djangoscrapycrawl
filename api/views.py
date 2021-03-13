from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
import json
# from api.utils import URLUtil
from api.models import ScrapyItem
scrapyd = ScrapydAPI('http://localhost:6800')

def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url) # check if url format is valid
    except ValidationError:
        return False
    return True
@csrf_exempt
@require_http_methods(['POST', 'GET']) # only get and post
def crawl(request):
    # Post requests are for new crawling tasks
    print("Vao crawl")
    if request.method == 'POST':
        url = request.POST.get('url', None) # take url comes from client. (From an input may be?)
        if not url:
            return JsonResponse({'error': 'Missing  args'})
        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})
        domain = urlparse(url).netloc # parse the url and extract the domain
        unique_id = str(uuid4()) # create a unique ID.

        x = {
            "unique_id": unique_id,
            "type": 'detailUni',
        }

        settings = {
            'unique_id': json.dumps(x), # unique ID for each record for DB
            # 'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

        task = scrapyd.schedule('default', 'icrawler',
            settings=settings, url=url, domain=domain)
        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':

        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)
        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})
@csrf_exempt
@require_http_methods(['POST', 'GET']) # only get and post
def crawlnewsuni(request):
    # Post requests are for new crawling tasks
    print("vao neee")
    if request.method == 'POST':
        url = request.POST.get('url', None) # take url comes from client. (From an input may be?)
        if not url:
            return JsonResponse({'error': 'Missing  args'})
        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})
        domain = urlparse(url).netloc # parse the url and extract the domain
        unique_id = str(uuid4()) # create a unique ID.
        print(url)
        x = {
            "unique_id": unique_id,
            "type": 'newslist',
        }

        settings = {
            'unique_id': json.dumps(x), # unique ID for each record for DB
            # 'type': 'newslist',
            # 'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

        task = scrapyd.schedule('default', 'newscrawler',
            settings=settings, url=url, domain=domain)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':

        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)
        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})

@csrf_exempt
@require_http_methods(['POST', 'GET']) # only get and post
def crawllastestnewsuni(request):
    # Post requests are for new crawling tasks
    print("vao neee")
    if request.method == 'POST':
        url = request.POST.get('url', None) # take url comes from client. (From an input may be?)
        if not url:
            return JsonResponse({'error': 'Missing  args'})
        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})
        crawlDate = request.POST.get('crawldate', None)  # take url comes from client. (From an input may be?)
        if not crawlDate:
            return JsonResponse({'error': 'Missing  args begin crawldate'})
        domain = urlparse(url).netloc # parse the url and extract the domain
        unique_id = str(uuid4()) # create a unique ID.

        x = {
            "unique_id": unique_id,
            "type": 'lastestnewslist',
        }

        settings = {
            'unique_id': json.dumps(x), # unique ID for each record for DB
            # 'type': 'newslist',
            # 'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

        task = scrapyd.schedule('default', 'lastestnewscrawler',
            settings=settings, url=url, crawlDate= crawlDate, domain=domain)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':

        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)
        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})

@csrf_exempt
@require_http_methods(['POST', 'GET']) # only get and post
def crawluni(request):
    # Post requests are for new crawling tasks
    print("vao crawlUni")
    if request.method == 'POST':
        url = request.POST.get('url', None) # take url comes from client. (From an input may be?)
        year = request.POST.get('year', None)
        print(url)
        print("year: ")
        print(year)
        if not url and not year:
            return JsonResponse({'error': 'Missing  args'})
        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})
        domain = urlparse(url).netloc # parse the url and extract the domain
        unique_id = str(uuid4()) # create a unique ID.

        x = {
            "unique_id": unique_id,
            "type": 'benchmarks',
        }

        settings = {
            'unique_id': json.dumps(x), # unique ID for each record for DB
            # 'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

        task = scrapyd.schedule('default', 'universities',
            settings=settings, url=url, domain=domain, year=year)
        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started'})
    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':

        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)
        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})

@csrf_exempt
@require_http_methods(['POST', 'GET']) # only get and post
def crawlmajor(request):
    # Post requests are for new crawling tasks
    print("vao crawlMajor")
    if request.method == 'POST':
        url = request.POST.get('url', None) # take url comes from client. (From an input may be?)
        if not url:
            return JsonResponse({'error': 'Missing  args'})
        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})
        domain = urlparse(url).netloc # parse the url and extract the domain
        unique_id = str(uuid4()) # create a unique ID.

        x = {
            "unique_id": unique_id,
            "type": 'major',
        }

        settings = {
            'unique_id': json.dumps(x),# unique ID for each record for DB
            # 'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

        task = scrapyd.schedule('default', 'majorCrawler',
            settings=settings, url=url, domain=domain)
        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':

        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)
        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})
@csrf_exempt
@require_http_methods(['POST', 'GET']) # only get and post
def crawldetailuni(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':
        url = request.POST.get('url', None) # take url comes from client. (From an input may be?)
        if not url:
            return JsonResponse({'error': 'Missing  args'})
        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})
        domain = urlparse(url).netloc # parse the url and extract the domain
        unique_id = str(uuid4()) # create a unique ID.

        x = {
            "unique_id": unique_id,
            "type": 'icon',
        }

        settings = {
            'unique_id': json.dumps(x), # unique ID for each record for DB
            # 'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

        task = scrapyd.schedule('default', 'detailuniCrawler',
            settings=settings, url=url, domain=domain)
        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':

        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)
        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})

@csrf_exempt
@require_http_methods(['POST', 'GET']) # only get and post
def tuitionuni(request):
    # Post requests are for new crawling tasks
    print("vao tuitionuni")
    if request.method == 'POST':
        url = request.POST.get('url', None) # take url comes from client. (From an input may be?)
        if not url:
            return JsonResponse({'error': 'Missing  args'})
        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})
        domain = urlparse(url).netloc # parse the url and extract the domain
        unique_id = str(uuid4()) # create a unique ID.

        x = {
            "unique_id": unique_id,
            "type": 'tuition',
        }

        settings = {
            'unique_id': json.dumps(x),  # unique ID for each record for DB
            # 'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

        task = scrapyd.schedule('default', 'tuitionuni',
            settings=settings, url=url, domain=domain)
        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':

        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)
        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})

@csrf_exempt
@require_http_methods(['POST', 'GET']) # only get and post
def listblock(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':
        url = request.POST.get('url', None) # take url comes from client. (From an input may be?)
        if not url:
            return JsonResponse({'error': 'Missing  args'})
        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})
        domain = urlparse(url).netloc # parse the url and extract the domain
        unique_id = str(uuid4()) # create a unique ID.

        x = {
            "unique_id": unique_id,
            "type": 'listblock',
        }

        settings = {
            'unique_id': json.dumps(x), # unique ID for each record for DB
            # 'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

        task = scrapyd.schedule('default', 'listBlock',
            settings=settings, url=url, domain=domain)
        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':

        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)
        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})
