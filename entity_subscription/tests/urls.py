from django.conf.urls import patterns, url

def test(request):
    return ''

urlpatterns = patterns(
    '',
    url(r'^user/(?P<pk>\d+)/$', test, name='user_page'),
    url(r'^team/(?P<pk>\d+)/$', test, name='team_page'),
)
