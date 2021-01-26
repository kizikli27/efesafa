from django import forms
from . models import *
from django.contrib.auth.models import User
import datetime

class listForm(forms.ModelForm):
    class Meta:
        model = ilkapp
        fields=("title","description","finished","date")
    

#class ogrenciform(forms.ModelForm):
 #   class Meta:
  #      model=ogrenci
   #     fields=("adi","telefonu","sinifi","numarasi")



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email','first_name','last_name','groups')
class ogrenciKayitForm(forms.ModelForm):
     class Meta():
         model = ogrenciKayit
         fields = ("__all__")

class kurumsForm(forms.ModelForm):
     class Meta():
         model = kurums
         fields = ("__all__")

class ogretmenForm(forms.ModelForm):
    class Meta():
         model = ogretmenKayit
         fields = ("__all__")

class ksinifiForm(forms.ModelForm):
    class Meta():
         model = ksinifi
         fields = ("last_name","ksinifi")

class dersekleForm(forms.ModelForm):
    class Meta():
         model = dersler
         fields = ("last_name","dersadi")
class birebirForm(forms.ModelForm):
    class Meta():
         model = birebir
         fields = ("__all__")
         
class haftaForm(forms.ModelForm):
    class Meta():
         model = hafta
         fields = ('gunler',)

class mesajlarForm(forms.ModelForm):
    class Meta():
        model = mesajlar
        fields=("__all__")

class FriendForm(forms.ModelForm):
    ## change the widget of the date field.
    dob = forms.DateField(
        label='What is your birth date?', 
        # change the range of the years from 1980 to currentYear - 5
        widget=forms.SelectDateWidget(years=range(1980, datetime.date.today().year-5))
    )
    
    def __init__(self, *args, **kwargs):
        super(FriendForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Friend
        fields = ("__all__")

class duyurularForm(forms.ModelForm):
    class Meta():
         model = duyurular
         fields = ("__all__")

class dersprogramiForm(forms.ModelForm):
    class Meta():
         model = dersprogrami
         fields = ("__all__")

class derssaatleriForm(forms.ModelForm):
    class Meta():
         model = derssaatleri
         fields = ("__all__")

class dersguruplariForm(forms.ModelForm):
    class Meta():
         model = dersguruplari
         fields = ("__all__")

class odemeForm(forms.ModelForm):
    class Meta():
         model = odeme
         fields = ("__all__")