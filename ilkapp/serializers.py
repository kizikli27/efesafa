from . models import *
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
        model = User
        fields = ('username','password','email','first_name','last_name','groups')
class ogrenciKayitSerializer(serializers.HyperlinkedModelSerializer):
     class Meta():
         model = ogrenciKayit
         fields = ("__all__")

class kurumsSerializer(serializers.HyperlinkedModelSerializer):
     class Meta():
         model = kurums
         fields = ("__all__")

class ogretmenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
         model = ogretmenKayit
         fields = ("__all__")

class ksinifiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
         model = ksinifi
         fields = ("__all__")

class dersekleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
         model = dersler
         fields = ("__all__")
class birebirSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
         model = birebir
         fields = ("__all__")
         
class haftaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
         model = hafta
         fields = ('gunler',)

class mesajlarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
        model = mesajlar
        fields=("__all__")

class duyurularSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
         model = duyurular
         fields = ("__all__")

class dersprogramiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
         model = dersprogrami
         fields = ("__all__")

class derssaatleriSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
         model = derssaatleri
         fields = ("__all__")

class dersguruplariSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
         model = dersguruplari
         fields = ("__all__")

class odemeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
         model = odeme
         fields = ("__all__")