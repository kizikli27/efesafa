from django.shortcuts import render, redirect,HttpResponse
from . models import *
from . forms import *
from django.core.files import File
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . forms import UserForm,ogrenciKayitForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
import io
from django.http import JsonResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table,TableStyle
from reportlab.platypus.tables import TableStyle
from reportlab.lib import colors
from reportlab.platypus import Flowable
from django.http import HttpResponse
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.conf import settings
from django.conf.urls.static import static
from reportlab.lib.enums import TA_RIGHT
from django.db.models import Q
from django.core import serializers
from django.db.models import Aggregate
from django.db.models import OuterRef, Subquery, Sum
from rest_framework import viewsets
from . serializers import *

def pdfolustur(request,adi,gurubu):
        kurum=request.user.last_name
        kurumadi=kurums.objects.get(username=kurum)
        if gurubu=="ogrenci":  
            users = birebir.objects.filter(last_name=kurum,bbogrenci=adi).order_by('bbgun','bbsaati')
            
        elif gurubu=="ogretmen":
            users = birebir.objects.filter(last_name=kurum,bbogretmen=adi).order_by('bbgun','bbsaati')
            
        elif gurubu=="sinif":
            users = ogrenciKayit.objects.filter(last_name=kurum,ksinifi=adi).order_by('id')

        elif gurubu=="muhasebe":
            users = odeme.objects.filter(last_name=kurum,odogrenci=adi).order_by('-odemetarihi')
            
       # krm=kurum.objects.get(username=kurum)
        #kurumadi=krm.first_name
        buffer = io.BytesIO()
        #buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=A4)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        pdfmetrics.registerFont(TTFont('Times', settings.STATIC_DIR/'fonts/arial.ttf'))
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='RightAlign',fontName='Times',fontSize=12,
                    leading=14,
                    spaceAfter=6,))
        styles.add(ParagraphStyle(name='centerAlign',fontName='Times',fontSize=18,
                    leading=22,
                    spaceAfter=6,
                    alignment=TA_CENTER))
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        elements.append(Paragraph(kurumadi.first_name, styles['centerAlign']))
        if gurubu=="ogretmen" or gurubu=="ogrenci":
            elements.append(Paragraph('Sayın '+adi+' Birebir ders programınız aşağıda belirtildiği gibidir. Derslerinize zamanında girmeniz önemlidir. Katılamayacağınız dersleri önceden kurum idaresine bildirmeniz gerekmektedir.', styles['RightAlign']))
            elements.append(Paragraph('Gereğini bilgilerinize rica ederim.', styles['RightAlign']))
           
        elif gurubu=="sinif":
            elements.append(Paragraph(adi+' Sınıfı Öğrenci Listesidir', styles['RightAlign']))
            elements.append(Paragraph('Gereğini bilgilerinize rica ederim.', styles['RightAlign']))
            
        elif gurubu=="muhasebe":
            elements.append(Paragraph(adi+' Ödeme Listesidir', styles['RightAlign']))
            elements.append(Paragraph('Kurum kayıtlarımızla çelien durumlarda kurumdaki kayıtlar esas alınır. Gereğini bilgilerinize rica ederim.', styles['RightAlign']))

        # Need a place to store our table rows
        table_data = []
        if gurubu=="sinif":
            table_data.append(["Sıra","Numarası","Adı Soyadı","Okulu","Alanı"])
        elif gurubu=="ogretmen":
            table_data.append(["Sıra","Günler","Saati","Ders","Öğrenci"])
        elif gurubu=="ogrenci":
            table_data.append(["Sıra","Günler","Saati","Ders","Öğretmen"])
        elif gurubu=="muhasebe":
            table_data.append(["Sıra","Ödeme Tarihi(Y-A-G)","Ödeme Miktarı TL","Açıklama"])
        sira=0
        
        for i, user in enumerate(users):
            sira+=1
            
            if gurubu=="ogrenci" or gurubu=="ogretmen":
            # Add a row to the table
                baslama=str(user.bbsaati)
                bitis=str(user.bbbitissaati)
                saat=str(baslama+' - \n'+bitis)
                if user.bbgun==1:
                    gun="Pazartesi"            
                elif user.bbgun==2:
                    gun="Salı"
                elif user.bbgun==3:
                    gun="Çarşamba"
                elif user.bbgun==4:
                    gun="Perşembe"
                elif user.bbgun==5:
                    gun="Cuma"
                elif user.bbgun==6:
                    gun="Cumartesi"
                elif user.bbgun==7:
                    gun="Pazar"
                else:
                    gun="Hergün"
                
            if gurubu=="ogrenci":  
                table_data.append([sira,gun,saat,user.bbdersadi,user.bbogretmen])
            elif gurubu=="ogretmen":
                table_data.append([sira,gun,saat,user.bbdersadi,user.bbogrenci])
            elif gurubu=="sinif":
                table_data.append([sira,user.id,user.first_name,user.okulu,user.alani])
            elif gurubu=="muhasebe":
                table_data.append([sira,user.odemetarihi.date(),user.taksit,user.aciklama])

        # Create the table
        user_table = Table(table_data)
        user_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                                        ('FONT', (0, 0), (-1, -1), 'Times'),
                                        ]))
        elements.append(user_table,)
        doc.build(elements)

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=adi+'.pdf')


def download(request, resim_id):
    todo = mesajlar.objects.get(pk=resim_id)
    kurum=todo.last_name
    if request.user.last_name==kurum or request.user.username==kurum:    
        dosya=todo.resim.path   
        filename =dosya
        response = FileResponse(open(filename, 'rb'))
        return response
    else: 
        return redirect('erisim')
def index(request):
    if request.method=="POST":
        form=listForm(request.POST or None)
        if form.is_valid:
            form.save()
            liste=ilkapp.objects.all()
            
            return render(request,"ilkapp/index.html",{'liste':liste})
    else:
        liste=ilkapp.objects.all()
        return render(request,"ilkapp/index.html",{'liste':liste})
@login_required 
def index1(request,kurum):
    if request.user.last_name==kurum or request.user.username==kurum: 
        adi=request.user.first_name  
        if request.user.groups.filter(name='kurum').exists():
      
            liste=duyurular.objects.filter(last_name=kurum).order_by('-dtarih')[:5]
            birebirler=birebir.objects.filter(last_name=kurum, bbogretmen=adi).order_by('bbgun','bbsaati')
        elif request.user.groups.filter(name='ogretmenler').exists():
        
            liste=duyurular.objects.filter(last_name=kurum,dogretmen=True).order_by('-dtarih')[:5]
            birebirler=birebir.objects.filter(last_name=kurum, bbogretmen=adi).order_by('bbgun','bbsaati')
        elif request.user.groups.filter(name='ogrenciler').exists():
            liste=duyurular.objects.filter(last_name=kurum,dogrenci=True).order_by('-dtarih')[:5] 
            birebirler=birebir.objects.filter(last_name=kurum, bbogrenci=adi).order_by('bbgun','bbsaati')
        krm=kurums.objects.get(username=kurum)
        return render(request,"ilkapp/index1.html",{'krm':krm,'liste':liste,'birebirler':birebirler})
    else: 
        return redirect('erisim')
def about(request):
    return render(request,"ilkapp/about.html")
def create(request):
    if request.method=="POST":
        form=listForm(request.POST or None)
        if form.is_valid:
            form.save()
            liste=ilkapp.objects.all()
            return render(request,"ilkapp/create.html",{'liste':liste})
    else:
        liste=ilkapp.objects.all()
        return render(request,"ilkapp/create.html",{'liste':liste})
@login_required 
def delete(request,ilkapp_id):
    todo=ilkapp.objects.get(pk=ilkapp_id)
    todo.delete()
    return redirect('index')
@login_required 
def deletesinif(request,ksinifi_id):
    
    deleted=False
    tmm=False
    todo=ksinifi.objects.get(pk=ksinifi_id)
    kurum=todo.last_name
    if request.user.last_name==kurum or request.user.username==kurum:    
        sayisi=ogrenciKayit.objects.filter(ksinifi=todo.ksinifi).count()
    
        if sayisi==0:
            todo.delete()
            tmm=True
            return render(request,"ilkapp/sinifekle.html",{'deleted':deleted,'tmm':tmm})
        else:
            deleted=True
            return render(request,"ilkapp/sinifekle.html",{'deleted':deleted})
    else: 
        return redirect('erisim')
@login_required 
def sinifupdate(request,ksinifi_id):
    tmmupdate=False
    todo=ksinifi.objects.get(pk=ksinifi_id)
    kurum=todo.last_name
    if request.user.last_name==kurum or request.user.username==kurum:
        krm=kurums.objects.get(username=kurum) 
        sayisi=ogrenciKayit.objects.filter(ksinifi=todo.ksinifi,last_name=kurum).count()
        if request.method=="POST":
            if sayisi==0:
                todo=ksinifi.objects.get(pk=ksinifi_id)
                form=ksinifiForm(request.POST or None,instance=todo)
                if form.is_valid:                      
                    form.save()
                    liste=ksinifi.objects.filter(last_name=kurum)
                    return render(request,"ilkapp/sinifekle.html",{'krm':krm,'liste':liste,'tmmupdate':tmmupdate})   
                
            else:
                tmmupdate=True
                liste=ksinifi.objects.filter(id=ksinifi_id)
                return render(request,"ilkapp/sinifekle.html",{'krm':krm,'liste':liste,'tmmupdate':tmmupdate})
            
    
        else:
            
            liste=ksinifi.objects.get(id=ksinifi_id)
            return render(request,"ilkapp/sinifupdate.html",{'krm':krm,'liste':liste,'tmmupdate':tmmupdate})
    else: 
        return redirect('erisim')
@login_required 
def yesFinish(request,ilkapp_id):
    todo=ilkapp.objects.get(pk=ilkapp_id)
    todo.finished=False
    todo.save()
    return redirect('index')
@login_required 
def noFinish(request,ilkapp_id):
    todo=ilkapp.objects.get(pk=ilkapp_id)
    todo.finished=True
    todo.save()
    return redirect('index')
@login_required 
def update(request,ilkapp_id):
    if request.method=="POST":
        todo=ilkapp.objects.get(pk=ilkapp_id)
        form=listForm(request.POST,instance=todo)
        if form.is_valid:
            form.save()
            liste=ilkapp.objects.all()
            #return redirect('index')
            return render(request,"ilkapp/update.html",{'liste':liste})
    else:
        liste=ilkapp.objects.all()
        return render(request,"ilkapp/update.html",{'liste':liste})
@login_required 
def ogrekle(request):   
    if request.method=="POST":
        form=ogrenciform(request.POST or None)
        if form.is_valid:
            form.save()
            liste=ilkapp.objects.all()
            return render(request,"ilkapp/ogrekle.html",{'liste':liste})
    else:
        liste=ilkapp.objects.all()
        return render(request,"ilkapp/ogrekle.html",{'liste':liste})
@login_required 
def goster(request):
        liste=ogrenci.objects.order_by('adi')
        sayfa = request.GET.get('sayfa',1)
        sayfalar = Paginator(liste,3)
        listem = sayfalar.page(int(sayfa))
        return render(request,"ilkapp/goster.html",{'liste':listem})
@login_required 
def ogrFiltre(request): 
        query = request.GET.get('ogrenci_adi')
        liste = ogrenci.objects.filter(adi=query)
        return render(request,"ilkapp/ogrFiltre.html",{'liste':liste})
def erisim(request):
    adi=request.user.first_name
    return render(request,"ilkapp/erisim.html",{'adi':adi})
   
       
        

    
@login_required
def special(request):
    return HttpResponse("You are logged in !")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
@login_required
def register(request,kurum):
    if request.user.last_name==kurum or request.user.username==kurum:
        registered = False
        liste=ksinifi.objects.filter(last_name=kurum)
        krm=kurums.objects.get(username=kurum)
        if request.method == 'POST':
            user_form = UserForm(data=request.POST)
            profile_form = ogrenciKayitForm(data=request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()  
                group = Group.objects.get(name='ogrenciler')
                user.groups.add(group)   
                profile = profile_form.save()
                profile.user = user
                
                if 'profile_pic' in request.FILES:
                    print('found it')
                    profile.profile_pic = request.FILES['profile_pic']
                    profile.save()
                registered = True
            else:
                print(user_form.errors,profile_form.errors)
                    
        else:
            liste=ksinifi.objects.filter(last_name=kurum)
            user_form = UserForm()
            profile_form = ogrenciKayitForm()
        return render(request,'ilkapp/register.html',{'krm':krm,'registered':registered,'liste':liste})
    else: 
        return redirect('erisim')      
@login_required
def kurumkayit(request):
    if request.user.is_superuser:
        registered = False
        if request.method == 'POST':
            user_form = UserForm(data=request.POST)
            kurum_form = kurumsForm(data=request.POST)
            if user_form.is_valid() and kurum_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()  
                group = Group.objects.get(name='kurum')
                user.groups.add(group) 
                group = Group.objects.get(name='idare')
                user.groups.add(group)    
                profile = kurum_form.save()
                profile.user = user
                
                if 'logo' in request.FILES:
                    print('found it')
                    profile.logo = request.FILES['logo']
                    profile.save()
                registered = True
            else:
                print(user_form.errors,kurum_form.errors)
                    
        else:
            user_form = UserForm()
            kurum_form = kurumsForm()
        return render(request,'ilkapp/kurumkayit.html',{'registered':registered})
    else: 
        return redirect('erisim')     
@login_required         
def ogretmenkayit(request,kurum):
    if request.user.last_name==kurum or request.user.username==kurum:
        registered = False
        krm=kurums.objects.get(username=kurum)
        if request.method == 'POST':
            user_form = UserForm(data=request.POST)
            ogretmen_form = ogretmenForm(data=request.POST)
            if user_form.is_valid() and ogretmen_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()  
                
                group = Group.objects.get(name='ogretmenler')
                user.groups.add(group)   
                profile = ogretmen_form.save()
                profile.user = user
                if profile.idareci:
                    group = Group.objects.get(name='idare')
                    user.groups.add(group) 
                if profile.muhasebe:
                    group = Group.objects.get(name='muhasebe')
                    user.groups.add(group) 
                registered = True
                
            else:
                print(user_form.errors,ogretmen_form.errors)
            liste=dersler.objects.filter(last_name=kurum)    
            return render(request,'ilkapp/ogretmenkayit.html',{'krm':krm,'registered':registered,'liste':liste})
        else:
            
            user_form = UserForm()
            liste=dersler.objects.filter(last_name=kurum)    
            ogretmen_form = ogretmenForm()
        return render(request,'ilkapp/ogretmenkayit.html',{'krm':krm,'registered':registered,'liste':liste})
    else: 
        return redirect('erisim')  

def yetkiver(request,ogretmen_id):
    if request.user.groups.filter(name='kurum').exists():
        ogretmen=ogretmenKayit.objects.get(pk=ogretmen_id)
        kurum=ogretmen.last_name
        if request.user.last_name==kurum or request.user.username==kurum:
            krm=kurums.objects.get(username=kurum)
            usernamem=ogretmen.username      
            user = User.objects.get(username = usernamem)
            
            if request.method=="POST":
                
                idare=request.POST.get('idare')
                muhasebe=request.POST.get('muhasebe')
                if idare:
                    group = Group.objects.get(name='idare')
                    user.groups.add(group)
                    
                elif user.groups.filter(name='idare').exists():
                    group = Group.objects.get(name='idare')
                    user.groups.remove(group)
                    idare=False
                if muhasebe:
                    group = Group.objects.get(name='muhasebe')
                    user.groups.add(group)
                    
                elif user.groups.filter(name='muhasebe').exists():
                    group = Group.objects.get(name='muhasebe')
                    user.groups.remove(group)
                    muhasebe=False
            
                sayi=ogretmenKayit.objects.filter(last_name=kurum).count()
                liste=ogretmenKayit.objects.filter(last_name=kurum)
                return render(request,"ilkapp/ogretmenlistesi.html",{'krm':krm,'liste':liste,'sayi':sayi})

            else:             
                if user.groups.filter(name='muhasebe').exists():
                    muhasebe=True
                else:
                    muhasebe=False            
                if user.groups.filter(name='idare').exists():
                    idare=True
                else:
                    idare=False
                if user.groups.filter(name='ogretmenler').exists():   
                    ogretmenler=True
                else:
                    ogretmenler=False
                return render(request,"ilkapp/yetkiver.html",{'krm':krm,'ogretmen':ogretmen,'muhasebe':muhasebe,'idare':idare,'ogretmenler':ogretmenler})
        else: 
            return redirect('erisim')  

    else: 
            return redirect('erisim')  



def user_login(request):
    registered=False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_superuser:
                login(request,user)
                return HttpResponseRedirect(reverse('kurumkayit'))
            elif user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                registered=True
                return render(request,'ilkapp/login1.html',{'registered':registered})
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            registered=True
            return render(request,'ilkapp/login1.html',{'registered':registered})
    else:
        return render(request, 'ilkapp/login1.html', {})
@login_required 
def ogrenciprofil(request):
    
    return HttpResponse('deneme')
@login_required         
def sinifekle(request,kurum):
    if request.user.last_name==kurum or request.user.username==kurum:
        krm=kurums.objects.get(username=kurum)
        if request.method=="POST":
            form=ksinifiForm(request.POST or None)
            if form.is_valid:
                form.save()
                liste=ksinifi.objects.filter(last_name=kurum)
                return render(request,"ilkapp/sinifekle.html",{'krm':krm,'liste':liste})

        else:
        
            say=0
            liste1=ogrenciKayit.objects.all()
            liste=ksinifi.objects.filter(last_name=kurum)
            liste2= ogrenciKayit.objects.count()
            liste3=ogrenciKayit.objects.filter(ksinifi='12 Sayısal xxx').count()
            return render(request,"ilkapp/sinifekle.html",{'krm':krm,'liste':liste,'liste1':liste1, 'liste2':liste2,  'liste3':liste3})
    else: 
        return redirect('erisim')
@login_required        
def siniflisteleri(request,kurum,ksinifi_id):
    if request.user.last_name==kurum or request.user.username==kurum:
        #todo=ilkapp.objects.get(pk=ilkapp_id)
        krm=kurums.objects.get(username=kurum)
        sayi=ogrenciKayit.objects.filter(ksinifi=ksinifi_id , last_name=kurum).count()
        liste=ogrenciKayit.objects.filter(ksinifi=ksinifi_id , last_name=kurum).order_by('id')
        return render(request,"ilkapp/siniflisteleri.html",{'krm':krm,'liste':liste, 'sinif':ksinifi_id, 'sayi':sayi})
    else: 
        return redirect('erisim')
@login_required 
def ogrencibilgileri(request,kurum,ogrenci_id):
        #todo=ilkapp.objects.get(pk=ilkapp_id)
    if request.user.last_name==kurum or request.user.username==kurum:       
        todo=ogrenciKayit.objects.get(last_name=kurum, first_name=ogrenci_id)
       
        krm=kurums.objects.get(username=kurum) 
        aldigibb=birebir.objects.filter(bbogrenci=ogrenci_id, last_name=kurum).count()
        return render(request,"ilkapp/ogrencibilgileri.html",{'krm':krm,'todo':todo,'aldigibb':aldigibb})
    else: 
       return redirect('erisim')
@login_required 
def dersekle(request,kurum):
    if request.user.last_name==kurum or request.user.username==kurum:  
        krm=kurums.objects.get(username=kurum) 
        if request.method=="POST":
            form=dersekleForm(request.POST or None)
            if form.is_valid:
                form.save()
                liste=dersler.objects.filter(last_name=kurum)
                return render(request,"ilkapp/dersekle.html",{'krm':krm,'liste':liste})

        else:             
            liste=dersler.objects.filter(last_name=kurum)
            return render(request,"ilkapp/dersekle.html",{'krm':krm,'liste':liste})
    else: 
        return redirect('erisim')
@login_required 
def deleteders(request,kurum,ders_id):
    tmm=False
    if request.user.last_name==kurum or request.user.username==kurum:  
        todo=dersler.objects.get(pk=ders_id)
        ders=todo.dersadi
        sayi=(ogretmenKayit.objects.filter(Q(bransi=ders,last_name=kurum) | Q(yanbransi=ders,last_name=kurum))).count()
        if sayi==0:
            todo.delete()
            liste=dersler.objects.filter(last_name=kurum)
            
            return render(request,"ilkapp/dersekle.html",{'liste':liste, 'tmm':tmm})
        else:
            tmm=True
            sayi=(ogretmenKayit.objects.filter(Q(bransi=ders,last_name=kurum) | Q(yanbransi=ders,last_name=kurum))).count()
            liste=dersler.objects.filter(last_name=kurum)
            return render(request,"ilkapp/dersekle.html",{'liste':liste, 'tmm':tmm, 'sayi':sayi})
    else: 
        return redirect('erisim')
@login_required 
def ogretmenlistesi(request,ders_adi,kurum):
        #todo=ilkapp.objects.get(pk=ilkapp_id)
        if request.user.last_name==kurum or request.user.username==kurum:  
            krm=kurums.objects.get(username=kurum)
            if ders_adi=="hepsi":
                sayi=ogretmenKayit.objects.filter(last_name=kurum).count()
                liste=ogretmenKayit.objects.filter(last_name=kurum)
            else:     
                sayi=(ogretmenKayit.objects.filter(bransi=ders_adi,last_name=kurum) | ogretmenKayit.objects.filter(yanbransi=ders_adi,last_name=kurum)).count()
                liste=ogretmenKayit.objects.filter(bransi=ders_adi,last_name=kurum) | ogretmenKayit.objects.filter(yanbransi=ders_adi,last_name=kurum) 
            return render(request,"ilkapp/ogretmenlistesi.html",{'krm':krm,'liste':liste, 'ders':ders_adi, 'sayi':sayi})
        else: 
            return redirect('erisim')
@login_required 
def birebirekle(request,kurum):
    if request.user.last_name==kurum or request.user.username==kurum:
        registered=False
        if request.method=="POST":
            form=birebirForm(request.POST or None)
            if form.is_valid:
                form.save()
                #liste=ksinifi.objects.filter(last_name=kurum)
                liste1=ogrenciKayit.objects.filter(last_name=kurum)
                liste=dersler.objects.filter(last_name=kurum)
                liste2=ogretmenKayit.objects.filter(last_name=kurum) 
                liste5=hafta.objects.all()
                krm=kurums.objects.get(username=kurum)
                registered=True
                return render(request,"ilkapp/birebirekle.html",{'krm':krm,'liste5':liste5,'liste':liste,'liste2':liste2,'registered':registered})

        else:
            form=birebirForm(request.POST or None)
            say=0
            liste1=ogrenciKayit.objects.filter(last_name=kurum)
            liste=dersler.objects.filter(last_name=kurum)
            liste2=ogretmenKayit.objects.filter(last_name=kurum) 
            liste5=hafta.objects.all()
            liste3=ogrenciKayit.objects.filter(ksinifi='12 Sayısal xxx').count()
            krm=kurums.objects.get(username=kurum)
            return render(request,"ilkapp/birebirekle.html",{'krm':krm,'liste5':liste5,'form':form, 'liste':liste,'liste1':liste1, 'liste2':liste2,  'liste3':liste3})
    else: 
        return redirect('erisim')
@login_required        
def ogrencilistesi(request,kurum):
    if request.user.last_name==kurum or request.user.username==kurum:
        #todo=ilkapp.objects.get(pk=ilkapp_id)
        krm=kurums.objects.get(username=kurum)
        sayi=ogrenciKayit.objects.filter(last_name=kurum).count()
        liste=ogrenciKayit.objects.filter(last_name=kurum).order_by('ksinifi','id')
        
        return render(request,"ilkapp/ogrencilistesi.html",{'krm':krm,'liste':liste, 'sayi':sayi})
    else: 
        return redirect('erisim')
@login_required 
def ogrencibbdp(request,kurum,ogrenci_id):
    if request.user.last_name==kurum or request.user.username==kurum:
        #todo=ilkapp.objects.get(pk=ilkapp_id)
        krm=kurums.objects.get(username=kurum)
        ogrenci=ogrenciKayit.objects.get(first_name=ogrenci_id, last_name=kurum)
        adi=ogrenci.first_name

           
        pazartesi=birebir.objects.filter(bbogrenci=adi,last_name=kurum,bbgun=1).order_by('bbsaati') 
        sali=birebir.objects.filter(bbogrenci=adi,last_name=kurum,bbgun=2).order_by('bbsaati') 
        carsamba=birebir.objects.filter(bbogrenci=adi,last_name=kurum,bbgun=3).order_by('bbsaati') 
        persembe=birebir.objects.filter(bbogrenci=adi,last_name=kurum,bbgun=4).order_by('bbsaati') 
        cuma=birebir.objects.filter(bbogrenci=adi,last_name=kurum,bbgun=5).order_by('bbsaati') 
        cumartesi=birebir.objects.filter(bbogrenci=adi,last_name=kurum,bbgun=6).order_by('bbsaati') 
        pazar=birebir.objects.filter(bbogrenci=adi,last_name=kurum,bbgun=7).order_by('bbsaati')   
        aldigibb=birebir.objects.filter(bbogrenci=adi,last_name=kurum).count()
        liste=birebir.objects.filter(bbogrenci=adi,last_name=kurum).order_by('bbgun','bbsaati')
       
        return render(request,"ilkapp/ogrencibbdp.html",{'krm':krm,'pazartesi':pazartesi,'sali':sali,'carsamba':carsamba,'persembe':persembe,'cuma':cuma,'cumartesi':cumartesi,'pazar':pazar,'liste':liste,'aldigibb':aldigibb,'adi':adi})
    else: 
        return redirect('erisim')
@login_required 
def ogretmenbbdp(request,kurum,ogrenci_id):
        #todo=ilkapp.objects.get(pk=ilkapp_id)
    if request.user.last_name==kurum or request.user.username==kurum:
        krm=kurums.objects.get(username=kurum)
        ogretmen=ogretmenKayit.objects.get(first_name=ogrenci_id,last_name=kurum)
        adi=ogretmen.first_name     
        pazartesi=birebir.objects.filter(bbogretmen=adi,last_name=kurum,bbgun=1).order_by('bbsaati') 
        sali=birebir.objects.filter(bbogretmen=adi,last_name=kurum,bbgun=2).order_by('bbsaati') 
        carsamba=birebir.objects.filter(bbogretmen=adi,last_name=kurum,bbgun=3).order_by('bbsaati') 
        persembe=birebir.objects.filter(bbogretmen=adi,last_name=kurum,bbgun=4).order_by('bbsaati') 
        cuma=birebir.objects.filter(bbogretmen=adi,last_name=kurum,bbgun=5).order_by('bbsaati') 
        cumartesi=birebir.objects.filter(bbogretmen=adi,last_name=kurum,bbgun=6).order_by('bbsaati') 
        pazar=birebir.objects.filter(bbogretmen=adi,last_name=kurum,bbgun=7).order_by('bbsaati')                       
        aldigibb=birebir.objects.filter(bbogretmen=adi,last_name=kurum).count()
        liste=birebir.objects.filter(bbogretmen=adi,last_name=kurum).order_by('bbgun','bbsaati')

        return render(request,"ilkapp/ogretmenbbdp.html",{'krm':krm,'pazartesi':pazartesi,'sali':sali,'carsamba':carsamba,'persembe':persembe,'cuma':cuma,'cumartesi':cumartesi,'pazar':pazar,'liste':liste,'aldigibb':aldigibb,'adi':adi})
    else: 
        return redirect('erisim')
@login_required 
def deletebb(request,kurum,bb_id,gurup):
    if request.user.last_name==kurum or request.user.username==kurum:
        deleted=False
        todo=birebir.objects.get(pk=bb_id)
        adi=todo.bbogrenci
        todo.delete()       
        aldigibb=birebir.objects.filter(bbogrenci=adi,last_name=kurum).count()
        liste=birebir.objects.filter(bbogrenci=adi,last_name=kurum)
        deleted=True 
        krm=kurums.objects.get(username=kurum)   
        if gurup=="ogrenci":
            return render(request,"ilkapp/ogrencibbdp.html",{'krm':krm,'liste':liste,'aldigibb':aldigibb,'adi':adi,'deleted':deleted})
        elif gurup=="ogretmen":
            return render(request,"ilkapp/ogretmenbbdp.html",{'krm':krm,'liste':liste,'aldigibb':aldigibb,'adi':adi,'deleted':deleted})
        #return redirect('index')
    else: 
        return redirect('erisim')
@login_required 
def ogrbirebirekle(request,kurum,ogrenci_id,gurubu):
    if request.user.last_name==kurum or request.user.username==kurum:
        registered=False
        krm=kurums.objects.get(username=kurum)   
    
        form=birebirForm(request.POST or None)
        say=0
        if gurubu=="ogrenci":

                ogrenci=ogrenciKayit.objects.get(pk=ogrenci_id,last_name=kurum)
                aldigibb=birebir.objects.filter(bbogrenci=ogrenci.first_name,last_name=kurum).count()
                liste4=birebir.objects.filter(bbogrenci=ogrenci.first_name,last_name=kurum).order_by('bbgun','bbsaati')           
                liste1=ogrenciKayit.objects.filter(last_name=kurum)
                liste=dersler.objects.filter(last_name=kurum)
                liste2=ogretmenKayit.objects.filter(last_name=kurum) 
                liste5=hafta.objects.all()
                
                registered=False
                grup="ogrenci"
                return render(request,"ilkapp/ogrbirebirekle.html",{'krm':krm,'ogrenci':ogrenci,'liste5':liste5,'aldigibb':aldigibb,'liste4':liste4,'liste':liste,'liste2':liste2,'registered':registered,'grup':grup})
        elif gurubu=="ogretmen":
                ogrenci=ogretmenKayit.objects.get(pk=ogrenci_id,last_name=kurum)
                aldigibb=birebir.objects.filter(bbogretmen=ogrenci.first_name,last_name=kurum).count()
                liste4=birebir.objects.filter(bbogretmen=ogrenci.first_name,last_name=kurum).order_by('bbgun','bbsaati')           
                liste1=ogretmenKayit.objects.filter(last_name=kurum)
                liste=dersler.objects.filter(last_name=kurum)
                liste2=ogrenciKayit.objects.filter(last_name=kurum) 
                liste5=hafta.objects.all()
                registered=False
                grup="ogretmen"
                return render(request,"ilkapp/ogrbirebirekle.html",{'krm':krm,'ogrenci':ogrenci,'liste5':liste5,'aldigibb':aldigibb,'liste4':liste4,'liste':liste,'liste2':liste2,'registered':registered,'grup':grup})
    else: 
        return redirect('erisim')
@login_required 
def ogrbirebireklekaydet(request,kurum,ogrenci_id,gurubu):
    
   
    if request.method=="POST":
        
        if request.is_ajax and request.method == "POST":
        # get the form data
            form=birebirForm(request.POST or None)
        # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
            # serialize in new friend object in json
                ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)

        
            
@login_required 
def gunekle(request):
    if request.method=="POST":
        form=haftaForm(request.POST or None)
        if form.is_valid:
            form.save()
           
            return render(request,"ilkapp/gunekle.html")
    else:
        
        return render(request,"ilkapp/gunekle.html")        
@login_required 
def message(request,kurum,sinif):#sınıfa ve öğrenciye mesaj gönderme
    if request.user.last_name==kurum or request.user.username==kurum:
        if request.method=="POST":
            form=mesajlarForm(request.POST or None, request.FILES or None)
            if form.is_valid:
                mesaj=form.save()
                
                if 'resim' in request.FILES:                    
                    mesaj.resim = request.FILES['resim']
                    mesaj.save()                
                krm=kurums.objects.get(username=kurum)                
                return render(request,"ilkapp/gelenmesaj.html",{'krm':krm,'sinif':sinif})
        else:           
            krm=kurums.objects.get(username=kurum)            
            return render(request,"ilkapp/message.html",{'krm':krm,'sinif':sinif})
    else: 
        return redirect('erisim')


@login_required
def gelenmesaj(request,kurum):#sınıfa gelen mesajlar öğrencilere dağıtılacak
    if request.user.last_name==kurum or request.user.username==kurum:
        krm=kurums.objects.get(username=kurum)  
        adi=request.user.first_name
        if request.user.groups.filter(name='ogretmenler').exists():
            todo=ogretmenKayit.objects.get(last_name=kurum,first_name=adi)
            sinifi=todo.first_name

        elif request.user.groups.filter(name='ogrenciler').exists():
            todo=ogrenciKayit.objects.get(last_name=kurum,first_name=adi)
            sinifi=todo.ksinifi
        elif request.user.groups.filter(name='kurum').exists():
            todo=kurums.objects.get(username=kurum,first_name=adi)
            sinifi=todo.first_name
        liste=mesajlar.objects.filter (Q(alici=sinifi) | Q(alici=adi) | Q(gonderen=adi)).order_by('-tarih')       
        sayi=mesajlar.objects.filter(Q(alici=sinifi) | Q(alici=adi) | Q(gonderen=adi)).count() 
        return render(request,"ilkapp/gelenmesaj.html",{'krm':krm,'liste':liste, 'sayi':sayi})
    else: 
        return redirect('erisim')


def mesajoku(request,mesaj_id):#sınıfa gelen mesajlar öğrencilere dağıtılacak

    todo=mesajlar.objects.get(pk=mesaj_id)
    kurum=todo.last_name
    if request.user.last_name==kurum or request.user.username==kurum:
        krm=kurums.objects.get(username=kurum)
        return render(request,"ilkapp/mesajoku.html",{'krm':krm,'todo':todo})
    else: 
        return redirect('erisim')
        
def ajaxdeneme(request):
    form = FriendForm()
    friends = Friend.objects.all()
    return render(request, "ilkapp/ajaxdeneme.html", {"form": form, "friends": friends})

def postFriend(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = FriendForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)

def checkNickName(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        nick_name = request.GET.get("nick_name", None)
        # check for the nick name in the database.
        if Friend.objects.filter(nick_name = nick_name).exists():
            # if nick_name found return not valid new friend
            return JsonResponse({"valid":False}, status = 200)
        else:
            # if nick_name not found, then user can create a new friend.
            return JsonResponse({"valid":True}, status = 200)

    return JsonResponse({}, status = 400)

def checkusername(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        username = request.GET.get("username", None)
        # check for the nick name in the database.
        if ogrenciKayit.objects.filter(username = username).exists():
            # if nick_name found return not valid new friend
            return JsonResponse({"valid":False}, status = 200)
        else:
            # if nick_name not found, then user can create a new friend.
            return JsonResponse({"valid":True}, status = 200)

    return JsonResponse({}, status = 400)

@login_required 
def duyuru(request,kurum):#duyuru ekleme
    if request.user.last_name==kurum or request.user.username==kurum:
        krm=kurums.objects.get(username=kurum)
        if request.method=="POST":
            form=duyurularForm(request.POST or None)
            if form.is_valid:
                form.save()
            liste=duyurular.objects.filter(last_name=kurum).order_by('-dtarih')[:5]
            return render(request,"ilkapp/index1.html",{'krm':krm,'liste':liste})   
            #return render(request,"ilkapp/duyuru.html",{'kurum':kurum})
        else:
            liste=duyurular.objects.filter(last_name=kurum).order_by('-dtarih')
            return render(request,"ilkapp/duyuru.html",{'krm':krm,'liste':liste,'kurum':kurum})   
    else: 
        return redirect('erisim')
@login_required 
def deleteduyuru(request,kurum,duyuru_id):   
    if request.user.last_name==kurum or request.user.username==kurum:
        krm=kurums.objects.get(username=kurum)
        todo=duyurular.objects.get(pk=duyuru_id)
        todo.delete()
        liste=duyurular.objects.all().order_by('-dtarih')[:5]
        return render(request,"ilkapp/index1.html",{'krm':krm,'liste':liste})
    else: 
        return redirect('erisim')
       

@login_required 
def updateduyuru(request,kurum,duyuru_id):
    if request.user.last_name==kurum or request.user.username==kurum:
        krm=kurums.objects.get(username=kurum)
        if request.method=="POST":
            todo=duyurular.objects.get(pk=duyuru_id)
            form=duyurularForm(request.POST,instance=todo)
            if form.is_valid:
                form.save()
                liste=duyurular.objects.all().order_by('-dtarih')[:5]
                #return redirect('index')
                return render(request,"ilkapp/index1.html",{'krm':krm,'liste':liste})
        else:
            todo=duyurular.objects.get(pk=duyuru_id)
            return render(request,"ilkapp/updateduyuru.html",{'krm':krm,'todo':todo})  
    else: 
        return redirect('erisim')

@login_required 
def ogrenciara(request,kurum):
    if request.user.last_name==kurum or request.user.username==kurum:
        krm=kurums.objects.get(username=kurum)
        aranan=request.GET.get('ogrenci')
        if aranan != "":
            todo=ogrenciKayit.objects.filter(first_name__icontains=aranan,last_name=kurum)
            return render(request,"ilkapp/ogrenciara.html",{'krm':krm,'todo':todo}) 
        else:
            return render(request,"ilkapp/ogrenciara.html",{'krm':krm}) 
    else: 
        return redirect('erisim')

@login_required 
def ogrenciduzenle(request,kurum,ogrenci_id):
        #todo=ilkapp.objects.get(pk=ilkapp_id)
    if request.user.last_name==kurum or request.user.username==kurum:  
        lst=ogrenciKayit.objects.get(pk=ogrenci_id)        
        krm=kurums.objects.get(username=kurum)
        if request.method == 'POST':
            profile_form = ogrenciKayitForm(request.POST or None,instance=lst)
            if profile_form.is_valid():                                 
                profile = profile_form.save()               
                if 'profile_pic' in request.FILES:
                    print('found it')
                    profile.profile_pic = request.FILES['profile_pic']
                    profile.save()
                registered = True
            else:
                print(user_form.errors,profile_form.errors)

            sayi=ogrenciKayit.objects.filter(last_name=kurum).count()
            liste=ogrenciKayit.objects.filter(last_name=kurum).order_by('ksinifi','id')
        
            return render(request,"ilkapp/ogrencilistesi.html",{'krm':krm,'liste':liste, 'sayi':sayi})          
        else:
            todo=ogrenciKayit.objects.get(last_name=kurum, pk=ogrenci_id)
            siniflar=ksinifi.objects.filter(last_name=kurum)
            krm=kurums.objects.get(username=kurum) 
            aldigibb=birebir.objects.filter(bbogrenci=ogrenci_id, last_name=kurum).count()
            return render(request,"ilkapp/ogrenciduzenle.html",{'krm':krm,'todo':todo,'aldigibb':aldigibb,'siniflar':siniflar})
    else: 
        return redirect('erisim')

@login_required 
def muhasebe(request,kurum,ogrenci_id):
    if request.user.groups.filter(name='muhasebe').exists() or request.user.groups.filter(name='kurum').exists():
        if request.user.last_name==kurum or request.user.username==kurum:
            krm=kurums.objects.get(username=kurum)
            ogrenci=ogrenciKayit.objects.get(pk=ogrenci_id)
            adi=ogrenci.first_name
            if request.method=="POST":
                form=odemeForm(request.POST or None)
                if form.is_valid:
                    form.save()
                liste=ogrenciKayit.objects.get(pk=ogrenci_id,last_name=kurum)
                liste1=odeme.objects.filter(last_name=kurum,odogrenci=adi).order_by('-odemetarihi')
                result = odeme.objects.filter(last_name=kurum,odogrenci=adi).aggregate(
                    toplam=Sum('taksit')
                    )['toplam']
                ucreti=ogrenci.ucret
                if result == None:
                    result=0
                kalan=ucreti-result
                return render(request,"ilkapp/muhasebe.html",{'kalan':kalan,'result':result,'krm':krm,'liste1':liste1,'liste':liste,'kurum':kurum})   
                #return render(request,"ilkapp/duyuru.html",{'kurum':kurum})
            else:
                liste=ogrenciKayit.objects.get(pk=ogrenci_id,last_name=kurum)
                liste1=odeme.objects.filter(last_name=kurum,odogrenci=adi).order_by('-odemetarihi')

                result = odeme.objects.filter(last_name=kurum,odogrenci=adi).aggregate(
                    toplam=Sum('taksit')
                    )['toplam']
                ucreti=ogrenci.ucret
                if result == None:
                    result=0
                kalan=ucreti-result
                return render(request,"ilkapp/muhasebe.html",{'kalan':kalan,'result':result,'krm':krm,'liste1':liste1,'liste':liste,'kurum':kurum}) 
        else: 
            return redirect('erisim') 
    else:
        return redirect('erisim')


@login_required        
def odemebilgi(request,kurum):
    if request.user.last_name==kurum or request.user.username==kurum:
        
        #todo=ilkapp.objects.get(pk=ilkapp_id)
        krm=kurums.objects.get(username=kurum)
        
        liste=odeme.objects.filter(last_name=kurum).order_by('-odemetarihi')
        return render(request,"ilkapp/odemebilgi.html",{'krm':krm,'liste':liste})
    else: 
        return redirect('erisim')
@login_required        
def ogrencisil(request,ogrenci_id):
    ogrenci=ogrenciKayit.objects.get(pk=ogrenci_id)
    kurum=ogrenci.last_name
    if request.user.last_name==kurum or request.user.username==kurum:
        ogrenciadi=ogrenci.first_name
        
        if birebir.objects.filter(last_name=kurum,bbogrenci=ogrenciadi):
            brb=birebir.objects.get(last_name=kurum,bbogrenci=ogrenciadi)
            brb.delete()
        user = User.objects.get(last_name=kurum,first_name=ogrenciadi)
        user.is_active=False
        user.save()
        
        ogrenci.delete()

  
        #todo=ilkapp.objects.get(pk=ilkapp_id)
        krm=kurums.objects.get(username=kurum)
        sayi=ogrenciKayit.objects.filter(last_name=kurum).count()
        liste=ogrenciKayit.objects.filter(last_name=kurum).order_by('ksinifi','id')
        
        return render(request,"ilkapp/ogrencilistesi.html",{'krm':krm,'liste':liste, 'sayi':sayi})
    else: 
        return redirect('erisim')
@login_required        
def sifredegistir(request,ogrenci_id):
    ogrenci=ogrenciKayit.objects.get(pk=ogrenci_id)
    kurum=ogrenci.last_name
    if request.user.last_name==kurum or request.user.username==kurum:
        parola=User.objects.make_random_password()
        ogrenciadi=ogrenci.first_name
        userim = User.objects.get(last_name=kurum,first_name=ogrenciadi)
        userim.set_password(parola)
        userim.save()           
        krm=kurums.objects.get(username=kurum)
        sayi=ogrenciKayit.objects.filter(last_name=kurum).count()
        liste=ogrenciKayit.objects.filter(last_name=kurum).order_by('ksinifi','id')
        return render(request,"ilkapp/ogrencilistesi.html",{'krm':krm,'liste':liste, 'sayi':sayi,'parola':parola,'userim':userim})
        
    else: 
        return redirect('erisim')

@login_required
def odemem(request,kurum):
    if request.user.groups.filter(name='muhasebe').exists() or request.user.groups.filter(name='kurum').exists():     
        if request.user.last_name==kurum or request.user.username==kurum:
            krm=kurums.objects.get(username=kurum)
            liste=odeme.objects.filter(last_name=kurum).order_by('odogrenci','-odemetarihi')
            return render(request,"ilkapp/odemem.html",{'krm':krm,'liste':liste})
           
    else: 
        return redirect('erisim')
