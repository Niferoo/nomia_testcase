from django.urls import path
from trunk.views import *

urlpatterns = [
    path('form/<slug:template>/', cdbform, name='form'),
]
