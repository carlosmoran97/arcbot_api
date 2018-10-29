from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from arclight.views import TrainModelView, ParseMessageView

app_name = 'arclight'

urlpatterns = [
    url('^trainmodel', csrf_exempt(TrainModelView.as_view()), name='trainmodel'),
    url('^parsemessage', csrf_exempt(ParseMessageView.as_view()), name='parsemessage')
]
