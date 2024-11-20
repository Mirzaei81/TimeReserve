from rest_framework.serializers import ModelSerializer,StringRelatedField,SlugRelatedField
from .models import  Market,User,City,Province,MarketOneTimeSlot,MarketFeature1
class MarketOneTimeSlotSerializer(ModelSerializer):
	class Meta:
		model=MarketOneTimeSlot
		fields = ("id","start_time","end_time","cost_multiplier","reserveCount","totalReseve","market","day_of_week")


class CitySerializer(ModelSerializer):
	class Meta:
		model =  City
		fields = ["id","name"]

class ProvinceSerializer(ModelSerializer):
	cities = CitySerializer(many=True)
	class Meta:
		model =  Province
		fields = ["id","name","tel_prefix","cities"]
class UserSerializer(ModelSerializer):
	class Meta:
		model =  User
		fields = "__all__"
class MarketSerializer(ModelSerializer):
	first_manager = StringRelatedField()
	second_manager = StringRelatedField()
	images = SlugRelatedField(read_only=True,slug_field="image__url",many=True)
	marketTimeSlots = MarketOneTimeSlotSerializer(many=True)
	city = StringRelatedField()
	province = StringRelatedField()

	class Meta:
		model =  Market
		fields = ["id","uuid","name","province","city","village","first_manager","second_manager","landline_phone",
			"main_street","rest_address","latitude","longitude","images","marketTimeSlots",
			]