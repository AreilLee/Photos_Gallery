from django.shortcuts import render, redirect
from albumapp import models
from albumapp import forms
from django.contrib.auth import authenticate
from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

def index(request):
	albums = models.AlbumModel.objects.all().order_by('-id')  #Read all the album
	totalalbum = len(albums)  #numbers of albums
	photos = []  #First picture of every album
	lengths = []  #The numbers of each album
	for album in albums:
		photo = models.PhotoModel.objects.filter(palbum__atitle=album.atitle).order_by('-id')  #Read the pictures
		lengths.append(len(photo))  #Pictures that add in in taltal
		if len(photo) == 0:  #if no pictures, add""
			photos.append('')
		else:
			photos.append(photo[0].purl)  #Add in 1st picture
	return render(request, "index.html", locals())
	
def albumshow(request, albumid=None):
	album = albumid  #以區域變數傳送給html
	photos = models.PhotoModel.objects.filter(palbum__id=album).order_by('-id')  #Read All the pictures
	monophoto = photos[0]  #1st picture
	totalphoto = len(photos)  #total numbers of pictures
	return render(request, "albumshow.html", locals())
	
def albumphoto(request, photoid=None, albumid=None):  #Show the single picture
	album = albumid  #use area iteration to sent html
	photo = models.PhotoModel.objects.get(id=photoid)  #get the picture
	photo.phit += 1  #click +1
	photo.save()
	return render(request, "albumphoto.html", locals())

def login(request):
	messages = ''  #empty at the first
	if request.method == 'POST':  #Deal with it's POST function
		postform = forms.PostForm(request.POST)
		if postform.is_valid():
			name = postform.cleaned_data['username']
			password = postform.cleaned_data['password']
			user1 = authenticate(username=name, password=password)  #verify
			if user1 is not None:  #verify pass
				auth.login(request, user1) #login
				postform = forms.PostForm()
				return redirect('/adminmain/')  #open the admin page
			else:  #account error
				message = 'The account not exist！'
		else:  #do not pass veryfy
			message = 'Login Failed！'
	else:
		message = 'Account, password and captcha need to put in'
		postform = forms.PostForm()
	return render(request, "login.html", locals())

def logout(request):
	auth.logout(request)
	return redirect('/index/')

def adminmain(request, albumid=None):
	if albumid == None:
		albums = models.AlbumModel.objects.all().order_by('-id')
		totalalbum = len(albums)
		photos = []
		lengths = []
		for album in albums:
			photo = models.PhotoModel.objects.filter(palbum__atitle=album.atitle).order_by('-id')
			lengths.append(len(photo))
			if len(photo) == 0:
				photos.append('')
			else:
				photos.append(photo[0].purl)
	else:  #delete album
		album = models.AlbumModel.objects.get(id=albumid)  #get the album
		photo = models.PhotoModel.objects.filter(palbum__atitle=album.atitle).order_by('-id')  #get all the pictures
		for photounit in photo:  #delete all the files
			os.remove(os.path.join(settings.MEDIA_ROOT, photounit.purl ))
		album.delete()  #remove the album
		return redirect('/adminmain/')
	return render(request, "adminmain.html", locals())

def adminadd(request):  #add new album
	message = ''
	title = request.POST.get('album_title', '')  #get the input info
	location = request.POST.get('album_location', '')
	desc = request.POST.get('album_desc', '')
	if title=='':  #click add new album botton to get into the page
		message = '相簿名稱一定要填寫...'
	else:  #click to add
		unit = models.AlbumModel.objects.create(atitle=title, alocation=location, adesc=desc)
		unit.save()
		return redirect('/adminmain/')
	return render(request, "adminadd.html", locals())

def adminfix(request, albumid=None, photoid=None, deletetype=None):  #manage album
    album = models.AlbumModel.objects.get(id=albumid)  #get certain album
    photos = models.PhotoModel.objects.filter(palbum__id=albumid).order_by('-id')
    totalphoto = len(photos)
    if photoid != None:  #Did not get here form admin page
        if photoid == 999999:  #click update and upload botton
            album.atitle = request.POST.get('album_title', '')  #update album info
            album.alocation = request.POST.get('album_location', '')
            album.adesc = request.POST.get('album_desc', '')
            album.save()
            files = []  #upload pictures list
            descs = []  #pictures describe list
            picurl = ["ap_picurl1", "ap_picurl2", "ap_picurl3", "ap_picurl4", "ap_picurl5"]
            subject = ["ap_subject1", "ap_subject2", "ap_subject3", "ap_subject4", "ap_subject5"]
            for count in range(0,5):
                files.append(request.FILES.get(picurl[count], ''))
                descs.append(request.POST.get(subject[count], ''))
            i = 0
            for upfile in files:  
                if upfile != '' and descs[i] != '':
                    fs = FileSystemStorage()  #upload file
                    filename = fs.save(upfile.name, upfile)
                    unit = models.PhotoModel.objects.create(palbum=album, psubject=descs[i], purl=upfile)  #put in the info stock
                    unit.save()
                    i += 1
            return redirect('/adminfix/' + str(album.id) + '/')
        elif deletetype == 'update':  #discriptions of update picture
            photo = models.PhotoModel.objects.get(id=photoid)
            photo.psubject = request.POST.get('ap_subject', '')  #get the picture discription
            photo.save()  #save into the stock
            return redirect('/adminfix/' + str(album.id) + '/')
        elif deletetype=='delete':  #delete the pictures
            photo = models.PhotoModel.objects.get(id=photoid)
            os.remove(os.path.join(settings.MEDIA_ROOT, photo.purl ))  #delete the picture file
            photo.delete()  #remove from the stock
            return redirect('/adminfix/' + str(album.id) + '/')
    return render(request, "adminfix.html", locals())
