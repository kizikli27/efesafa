
from django.urls import path ,include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import url,include
from django.contrib.auth.models import User
#from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from django.contrib.auth import views as auth_views
#from django.contrib.auth.views import PasswordChangeDoneView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('index1/<kurum>', views.index1, name="index1"),
    path('create/', views.create, name="create"),
    path('delete/<ilkapp_id>', views.delete, name="delete"),
    path('yesFinish/<ilkapp_id>', views.yesFinish, name="yesFinish"),
    path('noFinish/<ilkapp_id>', views.noFinish, name="noFinish"),
    path('update/<ilkapp_id>', views.update, name="update"),
    path('ogrekle/', views.ogrekle, name="ogrekle"),
    path('goster/', views.goster, name="goster"),
    path('ogrFiltre/', views.ogrFiltre, name="ogrFiltre"),
    
    path('user_login/', views.user_login, name="user_login"),
    path('register/<kurum>', views.register, name="register"),
    path('kurumkayit/', views.kurumkayit, name="kurumkayit"),
    path('ogretmenkayit/<kurum>', views.ogretmenkayit, name="ogretmenkayit"),
    path('special/',views.special,name="special"),
   
    path('logout/$', views.user_logout, name="logout"),
    path('ogrenciprofil', views.ogrenciprofil, name="ogrenciprofil"),
    path('accounts/password/',auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/change-password-done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    path('avatar/', include('avatar.urls')),
    path('ogrenciprofil', views.ogrenciprofil, name="ogrenciprofil"),
    path('sinifekle/<kurum>', views.sinifekle, name="sinifekle"),
    path('deletesinif/<ksinifi_id>', views.deletesinif, name="deletesinif"),
    path('sinifupdate/<ksinifi_id>', views.sinifupdate, name="sinifupdate"),
    path('siniflisteleri/<kurum>/<ksinifi_id>', views.siniflisteleri, name="siniflisteleri"),
    path('ogrencibilgileri/<kurum>/<ogrenci_id>', views.ogrencibilgileri, name="ogrencibilgileri"),
    path('dersekle/<kurum>', views.dersekle, name="dersekle"),
    path('deleteders/<kurum>/<ders_id>', views.deleteders, name="deleteders"),
    path('ogretmenlistesi/<ders_adi>/<kurum>', views.ogretmenlistesi, name="ogretmenlistesi"),
    path('birebirekle/<kurum>', views.birebirekle, name="birebirekle"),
    path('ogrencilistesi/<kurum>', views.ogrencilistesi, name="ogrencilistesi"),
    path('ogrencibbdp/<kurum>/<ogrenci_id>', views.ogrencibbdp, name="ogrencibbdp"),
    path('ogretmenbbdp/<kurum>/<ogrenci_id>', views.ogretmenbbdp, name="ogretmenbbdp"),
    path('deletebb/<kurum>/<bb_id>/<gurup>/', views.deletebb, name="deletebb"),
    path('ogrbirebirekle/<kurum>/<ogrenci_id>/<gurubu>', views.ogrbirebirekle, name="ogrbirebirekle"),
    path('gunekle', views.gunekle, name="gunekle"),
    path('pdfolustur/<adi>/<gurubu>', views.pdfolustur, name="pdfolustur"),
    path('message/<kurum>/<sinif>/',views.message, name="message"),
    path('download/<resim_id>/',views.download, name="download"),
    path('gelenmesaj/<kurum>', views.gelenmesaj, name="gelenmesaj"),
    path('mesajoku/<mesaj_id>', views.mesajoku, name="mesajoku"),
    path('ajaxdeneme', views.ajaxdeneme, name="ajaxdeneme"),
    path('post/ajax/friend', views.postFriend, name = "post_friend"),
    path('get/ajax/validate/nickname', views.checkNickName, name = "validate_nickname"),
    path('post/ajax/ogrbirebireklekaydet/<kurum>/<ogrenci_id>/<gurubu>',views.ogrbirebireklekaydet, name="ogrbirebireklekaydet"),
    path('get/ajax/validate/checkusername', views.checkusername, name = "checkusername"),
    path('duyuru/<kurum>/',views.duyuru, name="duyuru"),
    path('deleteduyuru/<kurum>/<duyuru_id>',views.deleteduyuru, name="deleteduyuru"),
    path('ogrenciara/<kurum>',views.ogrenciara, name="ogrenciara"),
    path('updateduyuru/<kurum>/<duyuru_id>',views.updateduyuru, name="updateduyuru"),
    path('ogrenciduzenle/<kurum>/<ogrenci_id>', views.ogrenciduzenle, name="ogrenciduzenle"),
    path('muhasebe/<kurum>/<ogrenci_id>', views.muhasebe, name="muhasebe"),
    path('erisim/', views.erisim, name="erisim"),
    path('yetkiver/<ogretmen_id>', views.yetkiver, name="yetkiver"),
    path('ogrencisil/<ogrenci_id>', views.ogrencisil, name="ogrencisil"),
    path('sifredegistir/<ogrenci_id>', views.sifredegistir, name="sifredegistir"),
    path('odemem/<kurum>', views.odemem, name="odemem"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


