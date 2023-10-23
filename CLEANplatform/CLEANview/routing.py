from django.urls import path

from .consumers import GraphConsumer

ws_urlpatterns=[

	path('ws/CLEANview/', GraphConsumer.as_asgi())
	
]