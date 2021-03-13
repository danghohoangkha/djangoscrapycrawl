from django.conf import settings
from django.conf.urls import url,static
from django.views.generic import TemplateView
from api import views
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^api/crawl', views.crawl, name='crawl'),
    url(r'^api/newsuni', views.crawlnewsuni, name='newsuni'),
    url(r'^api/lastestnewsuni', views.crawllastestnewsuni, name='lastestnewsuni'),
    url(r'^api/benchmarks', views.crawluni, name='uni'),
    url(r'^api/major', views.crawlmajor, name='major'),
    url(r'^api/logo', views.crawldetailuni, name='detailuni'),
    url(r'^api/tuitionuni', views.tuitionuni, name='tuitionuni'),
    url(r'^api/listblock', views.listblock, name='tuitionuni'),
]
# This is required for static files while in development mode. (DEBUG=TRUE)
# No, not relevant to scrapy or crawling :)
if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)