from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('autofillapp.views',
    # Examples:
    # url(r'^$', 'autofill.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name = 'autofill.html')),
    url(r'^test/$', TemplateView.as_view(template_name = 'test.html')),
    url(r'^test1/$', TemplateView.as_view(template_name = 'test1.html')),
    url(r'^distCalc/$', TemplateView.as_view(template_name = 'distanceCalc.html')),
    url(r'^address/$', TemplateView.as_view(template_name = 'addressAutoComplete.html')),    
    url(r'^places/$', TemplateView.as_view(template_name = 'placesAutofill.html')),
    url(r'^search/$', 'searchView'),
    url(r'^browser/$', 'browserView'),
    url(r'^customInput', 'customInputView'),
    url(r'^loadData/$', 'loadData'),
    url(r'^t/$', 'test'),
)
