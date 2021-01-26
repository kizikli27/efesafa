from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class ilkapp(models.Model):
    title= models.CharField(max_length=100, blank=True, null=True)
    description=models.TextField(max_length=1000, blank=True, null=True)
    finished=models.BooleanField(default=False)
    date=models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return self.title
#class ogrenci(models.Model):
 #   adi=models.CharField(max_length=100, blank=True, null=True)
  #  telefonu=models.CharField(max_length=100, blank=True, null=True)
   # sinifi=models.CharField(max_length=100, blank=True, null=True)
    #numarasi=models.CharField(max_length=100, blank=True, null=True)
    #def __str__(self):
     #   return self.adi

class ogrenciKayit(models.Model):
    #user = models.OneToOneField(User,on_delete=models.CASCADE)
    username=models.CharField(max_length=50, blank=True, null=True)
    first_name=models.CharField(max_length=100, blank=True, null=True)
    last_name=models.CharField(max_length=100, blank=True, null=True)
    email=models.CharField(max_length=100, blank=True, null=True)
    telefonu=models.CharField(max_length=15, blank=True, null=True)
    sinifi=models.CharField(max_length=10, blank=True, null=True)
    veliadi=models.CharField(max_length=100, blank=True, null=True)
    velitelefonu=models.CharField(max_length=100, blank=True, null=True)
    birebirsaati=models.CharField(max_length=5, blank=True, null=True)
    alani=models.CharField(max_length=100, blank=True, null=True)
    okulu=models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile',blank=True)
    ksinifi=models.CharField(max_length=100, blank=True, null=True)
    ucret=models.PositiveSmallIntegerField(blank=True, null=True)
    taksitsayisi=models.PositiveSmallIntegerField(blank=True, null=True)
    ogrenciadres=models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
         return self.username

class kurums(models.Model):
    
    
    username=models.CharField(max_length=50, blank=True, null=True)
    first_name=models.CharField(max_length=100, blank=True, null=True)
    last_name=models.CharField(max_length=100, blank=True, null=True)
    email=models.CharField(max_length=100, blank=True, null=True)
    telefonu=models.CharField(max_length=15, blank=True, null=True)
    adres=models.CharField(max_length=100, blank=True, null=True)
    ili=models.CharField(max_length=100, blank=True, null=True)
    ilcesi=models.CharField(max_length=100, blank=True, null=True)
    logo=models.ImageField(upload_to='logom', blank=True, null=True)
    vergidairesi=models.CharField(max_length=100, blank=True, null=True)
    verginumarasi=models.CharField(max_length=100, blank=True, null=True)
    #def image_thumb(self):
     #   return '<img src="%s" height="200" width="300"/>' %(self.logo.url)
    
    def __str__(self):
         return self.username

class ogretmenKayit(models.Model):
    #user = models.OneToOneField(User,on_delete=models.CASCADE)
    username=models.CharField(max_length=50, blank=True, null=True)
    first_name=models.CharField(max_length=100, blank=True, null=True)
    last_name=models.CharField(max_length=100, blank=True, null=True)
    email=models.CharField(max_length=100, blank=True, null=True)
    telefonu=models.CharField(max_length=15, blank=True, null=True)
    adres=models.CharField(max_length=10, blank=True, null=True)
    bransi=models.CharField(max_length=100, blank=True, null=True)
    yanbransi=models.CharField(max_length=100, blank=True, null=True)
    iban=models.CharField(max_length=100, blank=True, null=True)
    idareci=models.BooleanField(default=False)
    muhasebe=models.BooleanField(default=False)
    birebirsaati=models.CharField(max_length=5, blank=True, null=True)
    
   
    def __str__(self):
         return self.username

class ksinifi(models.Model):
    last_name=models.CharField(max_length=100, blank=True, null=True)
    ksinifi=models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
         return self.last_name

class dersler(models.Model):
    last_name=models.CharField(max_length=100, blank=True, null=True)
    dersadi=models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
         return self.last_name

class birebir(models.Model):
    last_name=models.CharField(max_length=100, blank=True, null=True)
    bbdersadi=models.CharField(max_length=100, blank=True, null=True)
    bbogrenci=models.CharField(max_length=100, blank=True, null=True)
    bbogrenciid=models.CharField(max_length=100, blank=True, null=True)
    bbogretmen=models.CharField(max_length=100, blank=True, null=True)
    bbogretmenid=models.CharField(max_length=100, blank=True, null=True)
    bbgun=models.PositiveSmallIntegerField(blank=True, null=True)
    bbsaati=models.CharField(max_length=10, blank=True, null=True)
    bbbitissaati=models.CharField(max_length=10, blank=True, null=True)
    bbonay=models.BooleanField(default=False) 
    
      
    #bbgun=models.PositiveSmallIntegerField(max_length=1,blank=True, null=True)
    def __str__(self):
         return self.last_name

class hafta(models.Model):
    gunler=models.CharField(max_length=10, blank=True, null=True)
    def __str__(self):
         return self.gunler

class mesajlar(models.Model):
    last_name=models.CharField(max_length=100, blank=True, null=True)
    gonderen=models.CharField(max_length=100, blank=True, null=True)
    alici=models.CharField(max_length=100, blank=True, null=True)
    mesaj=models.TextField(max_length=1000, blank=True, null=True)
    baslik=models.CharField(max_length=100, blank=True, null=True)
    resim=models.FileField(upload_to='mesajfile',blank=True)
    tarih=models.DateTimeField(default=datetime.now, blank=True, null=True)
    okundu=models.BooleanField(default=False) 
    def __str__(self):
         return self.gonderen

class Friend(models.Model):
    # NICK NAME should be unique
    nick_name = models.CharField(max_length=100, unique =  True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    likes = models.TextField(max_length=2000, blank=True, null=True)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    lives_in = models.CharField(max_length=150, null = True, blank = True)

    def __str__(self):
        return self.nick_name

class duyurular(models.Model):
    last_name=models.CharField(max_length=100, blank=True, null=True)
    dgonderen=models.CharField(max_length=100, blank=True, null=True)
    duyuru=models.TextField(max_length=2000, blank=True, null=True)
    dbaslik=models.CharField(max_length=100, blank=True, null=True)
    dtarih=models.DateTimeField(default=datetime.now, blank=True, null=True)
    dogretmen=models.BooleanField(default=True) 
    dogrenci=models.BooleanField(default=True) 
    def __str__(self):
         return self.dbaslik

class dersprogrami(models.Model):
    last_name=models.CharField(max_length=100, blank=True, null=True)
    dpsinif=models.CharField(max_length=100, blank=True, null=True)
    dpogretmen=models.CharField(max_length=100, blank=True, null=True)
    dpsaat=models.CharField(max_length=10, blank=True, null=True)
    dpders=models.CharField(max_length=100, blank=True, null=True)
    dpgun=models.CharField(max_length=100, blank=True, null=True)
    dersgurubu=models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
         return self.last_name

class derssaatleri(models.Model):
    last_name=models.CharField(max_length=100, blank=True, null=True)
    dersgurubu=models.CharField(max_length=100, blank=True, null=True)
    derssirasi=models.CharField(max_length=10, blank=True, null=True)
    baslamasaati=models.CharField(max_length=10, blank=True, null=True)
    bitissaati=models.CharField(max_length=10, blank=True, null=True)
    def __str__(self):
         return self.last_name

class dersguruplari(models.Model):
    last_name=models.CharField(max_length=100, blank=True, null=True)
    dersgurubu=models.CharField(max_length=100, blank=True, null=True)
    derssayisi=models.PositiveSmallIntegerField(blank=True, null=True)
    aciklama=models.TextField(max_length=2000, blank=True, null=True)
    def __str__(self):
         return self.last_name

class odeme(models.Model):
    last_name=models.CharField(max_length=100, blank=True, null=True)
    odogrenci=models.CharField(max_length=100, blank=True, null=True)
    taksit=models.FloatField(blank=True, null=True)
    aciklama=models.CharField(max_length=150, blank=True, null=True)
    odendi=models.BooleanField(default=False)
    odemetarihi=models.DateTimeField(default=datetime.now, blank=True, null=True)
    odemeyialan=models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
         return self.odogrenci
