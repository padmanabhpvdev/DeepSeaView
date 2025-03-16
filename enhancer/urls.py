from django.urls import path
from django.shortcuts import render
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from django.conf.urls.static import static
from django.conf import settings

current_path = ""
def median_blur_and_save(image_pth, output_folder):
    image = cv2.imread(image_pth)
    median_image = cv2.medianBlur(image, 5)
    median_image_rgb = cv2.cvtColor(median_image, cv2.COLOR_BGR2RGB)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    path = os.path.join(output_folder, 'median_blurred_image.jpg')
    cv2.imwrite(path, cv2.cvtColor(median_image, cv2.COLOR_RGB2BGR))

    return median_image_rgb,path
def normalize_and_save(image_pth, output_folder):
    image = cv2.imread(image_pth)
    normalized_image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    #original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    normalized_image_rgb = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2RGB)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    path = os.path.join(output_folder, 'normalized_image.jpg')
    cv2.imwrite(path, normalized_image_rgb)
    return normalized_image_rgb,path
def white_balance_and_save(image_pth, output_folder):
    try:
        image = cv2.imread(image_pth)
    except:
        image = image_pth
       
    

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    mean_a = np.mean(a)
    mean_b = np.mean(b)
    corrected_a = np.clip(a - (mean_a - 128), 0, 255).astype(np.uint8)
    corrected_b = np.clip(b - (mean_b - 128), 0, 255).astype(np.uint8)
    corrected_lab = cv2.merge((l, corrected_a, corrected_b))
    corrected_image = cv2.cvtColor(corrected_lab, cv2.COLOR_LAB2BGR)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    path = os.path.join(output_folder,'white_image.jpg')
    cv2.imwrite(os.path.join(output_folder,'white_image.jpg'), corrected_image)
    
    return corrected_image,path

def enhance_contrast_and_save(image_pth, output_folder):
    try:
        image = cv2.imread(image_pth)
    except:
        image = image_pth
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
    enhanced_l = clahe.apply(l)
    enhanced_lab = cv2.merge((enhanced_l, a, b))
    enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    path = os.path.join(output_folder, 'enhanced_image.jpg')
    cv2.imwrite(path, enhanced_image)
    return enhanced_image,path
def lace_and_save(image_pth, output_folder):
    image = cv2.imread(image_pth)
    corrected_image = white_balance_and_save(image, output_folder)[0]
    denoised_image = cv2.bilateralFilter(corrected_image, d=9, sigmaColor=75, sigmaSpace=75)
    enhanced_image = cv2.merge((denoised_image[:,:,0], corrected_image[:,:,1], corrected_image[:,:,2]))
    _,path = enhance_contrast_and_save(enhanced_image, output_folder)
    return enhanced_image,path

def index(request):
    if request.method=="POST":
        return render(request,"result.html")
    return render(request,"index.html")

def home(request):
    if request.method=="POST":
        
        return render(request,"result.html")
    return render(request,"home.html")
def products(request):
    
    return render(request,"products.html")


def upload(request):
    global current_path
    res = ""
    path = ""
    file_path=""
    nor_path = ""
    white_path =""
    med_path = ""
    lace_path = ""
    enhance_pth = ""
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        
        file_path = os.path.join('uploads', uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        _,lace_path = lace_and_save(file_path,'uploads')
        _,enhance_pth = enhance_contrast_and_save(file_path,'uploads')
        _,white_path = white_balance_and_save(file_path,'uploads')
        _,med_path = median_blur_and_save(file_path,'uploads')
        _,nor_path = normalize_and_save(file_path,'uploads')
        
    return render(request,'upload.html',{'res':res,'img_loc':file_path,
                                         'nor_loc':nor_path,
                                         "white_loc":white_path,
                                         "med_loc":med_path,
                                         "lace_loc":lace_path,
                                         "enhance_loc":enhance_pth,

                                         })

def median_func(request,file_name):
    global current_path
    res = ""
    path = ""
    file_path = os.path.join(os.getcwd(), 'uploads', file_name)
    with open(file_path, 'wb+') as destination:
        for chunk in file_name.chunks():
            destination.write(chunk)
    _,path = median_blur_and_save(file_path,'uploads')
        
    return render(request,'upload.html',{'res':res,'img_loc':path})


def normalize_func(request,file_name):
    global current_path
    res = ""
    path = ""
    file_path = os.path.join(os.getcwd(), 'uploads', file_name)
    with open(file_path, 'wb+') as destination:
        for chunk in file_name.chunks():
            destination.write(chunk)
    _,path = median_blur_and_save(file_path,'uploads')
        
    return render(request,'upload.html',{'res':res,'img_loc':path})

urlpatterns = [
    path("",index,name="index"),
    path("upload",upload,name="upload"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)