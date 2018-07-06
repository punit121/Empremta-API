from django.shortcuts import render
import subprocess, sys, shlex
from subprocess import check_output
import os
from subprocess import Popen, PIPE
# Create your views here.
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
#from .serializers import EmbedSerializer
from .forms import UploadImageForm
from .models import ImageModel
from django.core.files.storage import FileSystemStorage
from django.core.management import call_command
from io import StringIO
from io import BytesIO
import json
import time
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.parse import urlparse
import urllib.request
from os.path import basename
from urllib.request import urlretrieve, urlcleanup
from urllib.parse import urlsplit
from django.http import HttpResponse
#import cStringIO # *much* faster than StringIO
import urllib
from PIL import Image
import requests
#
# Created By Punit
#
def get_text_value():
	f = open('data.txt','r')
	message = f.read()
	return message

def get_json_data():
	with open('data.txt') as data_file:
		value = json.load(data_file)
	return value
#Saving the Image from the Url
def save_img_url(url):


	#file = urllib.request.urlopen(url)
	#im = io.StringIO(file.read())
	path, filename = os.path.split(url)
	filepath='media/'+filename
	urllib.request.urlretrieve(url,filepath)

	uploaded_file_url = filename


	return uploaded_file_url

# Checking Subcategory 
def subcat(request):
	url = request.GET['url']


	print(url)

	img_url=save_img_url(url)
	
	os.chdir('hawkeye/TensorFlow_Image_Classification')

	img = "../../media/"+img_url

	cmd = "python classify_image.py --image_file "+img

	print(cmd)
	args = shlex.split(cmd)

	p=subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	out=p.communicate()
	print(out)
	value = get_json_data()
	os.chdir('..')
	os.chdir('..')	


	return HttpResponse(json.dumps(value), content_type="application/json")
# Checking if Image contains any Nude content or not {This returns in form of SFW and NSFW}
def nude(request):
	url = request.GET['url']


	print(url)

	img_url=save_img_url(url)
	
	os.chdir('hawkeye/nude_detection')

	img = "../../media/"+img_url

	cmd = "python classify_nsfw.py -m data/open_nsfw-weights.npy "+img

	print(cmd)
	args = shlex.split(cmd)

	p=subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	out=p.communicate()
	print(out)
	value = get_json_data()
	os.chdir('..')
	os.chdir('..')	


	return HttpResponse(json.dumps(value), content_type="application/json")

#This functions is for extracting text from the image
def check_text(request):
	url = request.GET['url']


	print(url)

	img_url=save_img_url(url)
	
	os.chdir('hawkeye/TextPredictor')

	img = "../../media/"+img_url

	cmd = "python text_predictor.py "+img

	print(cmd)
	args = shlex.split(cmd)

	p=subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	out=p.communicate()
	print(out)
	value = get_json_data()
	os.chdir('..')
	os.chdir('..')	


	return HttpResponse(json.dumps(value), content_type="application/json")

# This Function is for Checking Watermark on the given Image {currently we are testing for OLX } 
def check_watermark(request):
	url = request.GET['url']


	print(url)

	img_url=save_img_url(url)
	
	os.chdir('hawkeye/WatermarkPredictor')

	img = "../../media/"+img_url

	cmd = "pythonw detect_watermark.py "+img

	print(cmd)
	args = shlex.split(cmd)

	p=subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	out=p.communicate()
	print(out)
	value = get_json_data()
	os.chdir('..')
	os.chdir('..')	


	return HttpResponse(json.dumps(value), content_type="application/json")		

	
#We are Using Index just for testing. seperate functions have been created for different APIs 
def index(request):
	if request.method == "POST":
		image_form = UploadImageForm(request.POST, request.FILES)
		if image_form.is_valid():
			image_file = request.FILES['image']
			fs = FileSystemStorage()
			filename = fs.save(image_file.name, image_file)
			uploaded_file_url = fs.url(filename)
			#m = ImageModel.objects.get(pk=id)
			#m.image = form.cleaned_data['image']
			#m.save()

		#parser_classes = (MultiPartParser, FormParser)


		img_url= uploaded_file_url
		#file_serializer = FileSerializer(data=request.data)

		print(img_url)

		os.chdir('hawkeye/TensorFlow_Image_Classification')
		#out = StringIO()
		img = "../.."+img_url

		cmd = "python classify_image.py --image_file "+img
		#call_command('python classify_image.py --image_file test_images/car_test.jpeg', stdout=out)
		#data = request.get('python classify_image.py --image_file test_images/car_test.jpeg')
		print(cmd)
		args = shlex.split(cmd)
		#p = subprocess.Popen(args)
		#(out,err) = p.communicate()[0]
		p=subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
		out=p.communicate()
		print(out)
		#value = p.stdout.read()
		#print (p.stdout.readlines())
		#out = p.stderr.read(1)
		#value1 = json.dumps(p.communicate())
		value = get_json_data()

		print("Tensor Flow print done \n now returning value")
		#value = json.loads(out)
		#print(out)
		#value=out
		os.chdir('..')
		os.chdir('..')
		#time.sleep(6)
		os.chdir('hawkeye/nude.py')
		cmd_nude="python main.py "+img
		print(cmd_nude)
		q=subprocess.Popen(cmd_nude, shell=True, stderr=subprocess.PIPE)
		out1=q.communicate()
		print(out1)
		nude_value = get_text_value()
		print(nude_value)
		os.chdir('..')
		os.chdir('..')

		os.chdir('hawkeye/TextPredictor')
		cmd_watermark_text="python text_predictor.py "+img
		print(cmd_watermark_text)
		watermark_text=subprocess.Popen(cmd_watermark_text, shell=True, stderr=subprocess.PIPE)
		out2=watermark_text.communicate()
		print(out2)
		text_value=get_text_value()
		print(text_value)
		os.chdir('..')
		os.chdir('..')

		os.chdir('hawkeye/WatermarkPredictor')
		cmd_watermark_text="pythonw detect_watermark.py "+img
		print(cmd_watermark_text)
		watermark_text=subprocess.Popen(cmd_watermark_text, shell=True, stderr=subprocess.PIPE)
		out2=watermark_text.communicate()
		print(out2)
		watermark_value=get_json_data()
		print(watermark_value)
		os.chdir('..')
		os.chdir('..')






		return render(request, 'hawkeye/result.html',{'value':value,'text_value':text_value,'nude_value':nude_value, 'watermark_value':watermark_value} )

	else:
		return render(request, 'hawkeye/index.html')	


