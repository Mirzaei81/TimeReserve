from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator,MinValueValidator,MaxValueValidator
import uuid
class Province(models.Model):
    name = models.CharField(max_length=200)
    tel_prefix = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, default='no-slug')    
    province = models.ForeignKey(Province,on_delete=models.PROTECT,related_name="cities")
    def __str__(self) -> str:
        return self.name

class MarketManagers(models.Model):  #جدول مربوط به مسئول مارکت ها 
    TYPES = [
        ('mco', 'مسئول مارکت اول'),
    ]

    phone_number = models.CharField(max_length=11, validators=[
        RegexValidator(regex=r'^\d{11}$', message='شماره تلفن صحیح نیست', code='invalid_phone_number')])
    national_code = models.CharField(max_length=10, validators=[
        RegexValidator(regex=r'^\d{10}$', message='شماره ملی صحیح نیست', code='invalid_phone_number')])
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
#    انواع کاربر مرکز داریم که شما فقط با مسئول مارکت اول که تایپش mco است کار دارید. برای ارسال پیامک و غیره
    user_type = models.CharField(choices=TYPES, null=True, blank=True, max_length=5) 
    market = models.ManyToManyField('branch.MarketFeature2', blank=True, related_name='users')
    phone_confirmed = models.BooleanField(default=False, verbose_name='تایید شده توسط ادمین')
    employee_market_id = models.IntegerField(blank=False, default=0)    
    def __str__(self):
        return self.first_name+ " "+self.last_name
    class Meta:
        unique_together = ('phone_number', 'user_type','employee_market_id')

class Market(models.Model):
    market_types = [
        ('mo', 'مارکت اول'),
        ('mt', 'مارکت دوم'),
        ('mh', 'مارکت سوم')
    ]# شما فقط نوع مارکت اول رو دارین کار میکنین. یعنی جستجو در این مدل فقط مارکتهایی است که تایپ آنها mo میباشد
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name='نام مارکت')
    province = models.ForeignKey(Province,on_delete=models.CASCADE,max_length=200, verbose_name='استان')
    city = models.ForeignKey(City,on_delete=models.CASCADE,max_length=200, verbose_name='شهر')
    village = models.CharField(max_length=200, verbose_name='روستا', null=True, blank=True)
    first_manager = models.ForeignKey(MarketManagers, related_name='market_one', on_delete=models.CASCADE, verbose_name='مسئول مارکت')
    second_manager = models.ForeignKey(MarketManagers, null=True, blank=True, related_name='market_two',
                                       on_delete=models.SET_NULL)
    market_sheba = models.CharField(max_length=22, verbose_name='شماره شبا', validators=[
        RegexValidator(regex=r'^\d{22}$', message='شماره شبا صحیح نیست', code='invalid_phone_number')])
    sheba_owner_name = models.CharField(max_length=200, verbose_name='نام و نام خانوادگی صاحب شبا')
    landline_phone = models.CharField(max_length=15, validators=[
        RegexValidator(regex=r'^\d{11}$', message='شماره تلفن صحیح نیست', code='invalid_phone_number')],
                                      verbose_name='تلفن ثابت')
    main_street = models.CharField(max_length=200, verbose_name='خیابان اصلی')
    rest_address = models.CharField(max_length=500, verbose_name='بقیه ادرس')
    latitude = models.DecimalField(max_digits=60, decimal_places=30)
    longitude = models.DecimalField(max_digits=60, decimal_places=30)
    market_type = models.CharField(max_length=2, choices=market_types)  #نام مارکت تایپی که شما کار میکنید روش mo میباشد
    confirmed_person_national_code = models.CharField(max_length=10, verbose_name='کد ملی تایید کننده')
    is_confirmed_by_admin = models.BooleanField(default=False, verbose_name='تایید شده توسط ادمین')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    confirmed_date = models.DateTimeField(verbose_name='تاریخ تایید ادمین', null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save()
        if self.first_manager:
            self.first_manager.role_in_market = 'mgo'
            self.first_manager.save()
        if self.second_manager:
            self.second_manager.role_in_market = 'mgt'
            self.second_manager.save()
class MarketFeature1(models.Model):
    a = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    b = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    c = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    d = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    e = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    f = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    g = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    h = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)]) #تعداد رزرو همزمان مرکز
    i = models.BooleanField()  
    j = models.BooleanField()   
    k = models.BooleanField()   
    l = models.BooleanField()   
    ml = models.BooleanField(default = True)            
class MarketFeature2(models.Model):
    info = models.OneToOneField(MarketFeature1, on_delete=models.SET_NULL, related_name='markets_one', null=True,
                                blank=True)
    n = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000000)])
    m = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(40)])

class MarketImages(models.Model):
    image = models.ImageField(upload_to='market/images')
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='images')
class MarketOneTimeSlot(models.Model):
    market1 = models.ForeignKey(MarketFeature2, on_delete=models.CASCADE, related_name='time_slots', verbose_name='مارکت اول')
    day_of_week = models.CharField(
        max_length=20, 
        choices=[
            ('شنبه', 'شنبه'), 
            ('یکشنبه', 'یکشنبه'),
            ('دوشنبه', 'دوشنبه'),
            ('سه‌شنبه', 'سه‌شنبه'),
            ('چهارشنبه', 'چهارشنبه'),
            ('پنج‌شنبه', 'پنج‌شنبه'),
            ('جمعه', 'جمعه')
        ],
        verbose_name='روز هفته'
    )
    start_time = models.TimeField(verbose_name='ساعت شروع')
    end_time = models.TimeField(verbose_name='ساعت پایان')
    date = models.DateField(verbose_name="تاریخ")
    cost_multiplier = models.FloatField(
        default=1.0, 
        verbose_name='ضریب هزینه'
    )
    reserveCount = models.IntegerField(default=0)
    totalReseve = models.IntegerField(verbose_name="تعداد کل رزرو")
    market= models.ForeignKey(Market,on_delete=models.SET_NULL,related_name="marketTimeSlots",null=True)


    class Meta:
        unique_together = ('market1', 'day_of_week', 'start_time', 'end_time')
        verbose_name = 'بازه زمانی مارکت اول'
        verbose_name_plural = 'بازه‌های زمانی مارکت های اول'

    def __str__(self):
        return f"{self.day_of_week} ({self.start_time} - {self.end_time})"



class SmsBodyId(models.Model):
    name = models.CharField(max_length=200)
    sms_panel_username = models.CharField(max_length=200)
    sms_panel_password = models.CharField(max_length=200)
    text = models.TextField()
    body_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'اطلاعات پنل پیامکی'
        verbose_name_plural = 'اطلاعات پنلهای پیامکی'

    def save(self, *args, **kwargs):
        if self.is_active == True:
            SmsBodyId.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

class User(AbstractUser):
    username = models.CharField(max_length=11, validators=[
        RegexValidator(regex=r'^\d{11}$', message='شماره تلفن صحیح نیست', code='invalid_phone_number')],
                                verbose_name='شماره تلفن', unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='نام')
    last_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='نام خانوادگی')
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True, verbose_name='استان')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name='شهر')
    national_code = models.CharField(max_length=10, verbose_name='کد ملی')