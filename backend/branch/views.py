from rest_framework.viewsets import ReadOnlyModelViewSet,ModelViewSet
from rest_framework import status
from rest_framework.response  import Response
from rest_framework.generics import GenericAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView
from .models import  Market,User,City,Province,MarketOneTimeSlot,MarketReserved
from .serilizers import  MarketSerializer,UserSerializer,CitySerializer,ProvinceSerializer
from django.db.models import Q
from datetime import datetime
from melipayamak import Api
import jdatetime
import json 
from django.db import connection
# RestApi = Api(os.getenv("sms_username"),os.getenv("sms_password")).sms()
class MarketByCityView(GenericAPIView):
	queryset = Market
	def get(self,*args,**kwargs):
		pk = kwargs["pk"]
		qs = Market.objects.filter(city__pk=int(pk),market_type="mo") # حالت مارکتی که مد نظر برای فیلتر را انتخاب کنید 
		cursor = connection.cursor()
		cursor.execute("SELECT * from (SELECT marketFeature2.*,marketFeature1.* FROM marketFeature2 JOIN marketFeature1 where marketFeature2.info_id = marketFeature1.id) as X join centers_market WHERE X.market_ptr_id = centers_market.id")
		rows =cursor.fetchall()
		return Response(json.loads(rows))

class MarketByDateView(GenericAPIView):
	queryset = Market
	def get(self,*args,**kwargs):
		startTimeString = self.request.query_params.get("date")
		startTime=datetime.strptime(startTimeString, "%a, %d %b %Y %H:%M:%S %Z")
		endTimeString = self.request.query_params.get("time")
		endTime = datetime.strptime(endTimeString, "%a, %d %b %Y %H:%M:%S %Z")
		qs = Market.objects.filter(Q(marketTimeSlots__start_time__gte=startTime)|Q(marketTimeSlots__start_time__lte=endTime),market_type="mo") # حالت مارکتی که مد نظر برای فیلتر را انتخاب کنید 
		

		data = MarketSerializer(qs,many=True)
		return Response(data.data)
		
class MarketDetailView(RetrieveAPIView,UpdateAPIView):
	queryset = Market
	serializer_class = MarketSerializer
	def patch(self, request, *args, **kwargs):
		pk = kwargs["pk"]
		user = self.request.user
		market = MarketOneTimeSlot.objects.get(id=pk)
		cursor = connection.cursor()
		cursor.execute("SELECT X.h from (SELECT marketFeature2.*,marketFeature1.* FROM marketFeature2 JOIN marketFeature1 where marketFeature2.info_id = marketFeature1.id) as X join centers_market WHERE X.market_ptr_id = centers_market.id")
		totalReseveCount  =cursor.fetchall()[0]
		currentReserve = MarketReserved.objects.get(timeSlot__pk=pk)
		currentReserveCount =currentReserve.count
		date = market.date
		formatedDate = jdatetime.date.fromgregorian(year=date.year,month=date.month,day=date.day)
		if(currentReserveCount<totalReseveCount):
			currentReserve.count+=1
			# RestApi.send(user.username,"0911111111",f"رزور شما در تاریخ {market.market.name} در مرکز {formatedDate} با موفقیت انجام شد")
			market.save()
			currentReserve.save()
			return Response({"data":"با موفقیت انجام شد"},status=status.HTTP_200_OK)
		else:
			return Response({"data":"تعداد رزرو ها پر شده است"},status=status.HTTP_400_BAD_REQUEST)


class UserView(ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class ProvinceView(ReadOnlyModelViewSet):
	queryset = Province.objects.all()
	serializer_class = ProvinceSerializer
class CityDetailView(GenericAPIView):
	queryset = City
	serializer_class = CitySerializer
	def get(self,*args,**kwargs):
		cityNames = []
		pk = kwargs["pk"]
		for city in City.objects.filter(province__pk=pk):
			c = {}
			c["name"] = city.name
			c["id"] = city.id
			cityNames.append(c)
		return  Response(cityNames)

class CityListView(ListAPIView):
	queryset = City.objects.all()
	serializer_class = CitySerializer