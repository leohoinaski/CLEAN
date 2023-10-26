from django.urls import path
from .views import CLEANcalibrationNewDevice


urlpatterns =[
	path('', CLEANcalibrationNewDevice, name='CLEANcalibrationNewDevice'),

]
