from rest_framework.routers import DefaultRouter
from django.urls import re_path,path
from .views import MarketDetailView,UserView,CityListView,ProvinceView,CityDetailView,MarketByCityView,MarketByDateView
router = DefaultRouter()
router.register("User",UserView)
urlPattenrs =[
	re_path("Market/City/(?P<pk>[^/.]+)/$",MarketByCityView.as_view()),
	re_path("Market/(?P<pk>[^/.]+)/$",MarketDetailView.as_view()),
	re_path("City/(?P<pk>[^/.]+)/$",CityDetailView.as_view()),
	re_path("Province/",ProvinceView.as_view()),
	path("City/",CityListView.as_view()),
	path("Market/",MarketByDateView.as_view())
]+router.urls