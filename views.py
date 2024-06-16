from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
import dashscope
dashscope.api_key = "sk-5499188e2c7c4fd1bf392dae4686f367"

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Photo, Category
import numpy as np
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings
import os
from django.db import transaction

def find_similar_photos(request):
    user = request.user
    similar_category = Category.objects.filter(name="相似图片集合", user=user).first()
    
    # 排除已经属于“相似图片集合”类别的图片
    if similar_category:
        photos = Photo.objects.filter(category__user=user).exclude(category=similar_category)
    else:
        photos = Photo.objects.filter(category__user=user)

    image_vectors = []
    image_ids = []
    if photos.count() < 2:
        return redirect('gallery')

    # 用于存储相似图片的字典
    similar_photos = {}

    for photo in photos:
        image_path = os.path.join(settings.MEDIA_ROOT, photo.image.name)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        resized_image = cv2.resize(image, (100, 100)).flatten()  # resize and flatten image
        image_vectors.append(resized_image)
        image_ids.append(photo.id)

    similarities = cosine_similarity(image_vectors)

    for i in range(len(similarities)):
        for j in range(i + 1, len(similarities)):
            if similarities[i, j] > 0.9:  # If similarity is greater than 90%
                if image_ids[i] not in similar_photos:
                    similar_photos[image_ids[i]] = []

                # 将相似图片的原始类别记录下来
                original_category_i = photos.get(id=image_ids[i]).category
                original_category_j = photos.get(id=image_ids[j]).category

                similar_photos[image_ids[i]].append((image_ids[j], original_category_j))
    
    if not similar_category:
        similar_category = Category.objects.create(name="相似图片集合", user=user)

    if similar_photos:
        with transaction.atomic():
            for photo_id, similar_info in similar_photos.items():
                photo = Photo.objects.get(id=photo_id)
                photo.save_to_original_category = photo.category  # 保存原始类别
                photo.category = similar_category
                photo.save()

                for similar_id, original_category in similar_info:
                    similar_photo = Photo.objects.get(id=similar_id)
                    similar_photo.save_to_original_category = similar_photo.category  # 保存原始类别
                    similar_photo.category = similar_category
                    similar_photo.save()

    return redirect('gallery')

@login_required
def save_similar_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if photo.save_to_original_category:
        photo.category = photo.save_to_original_category
        photo.save_to_original_category = None
        photo.save()
    return redirect('gallery')


# Create your views here.
@login_required(login_url='login')
def AI_generate_description(request, pk):
    photo = Photo.objects.get(id=pk)
    image_url = "http://www.lockede.me" + photo.image.url
    try:
        messages = [
            {
                "role": "user",
                "content": [
                    {"image": image_url},
                    {"text": "这是什么?"}
                ]
            }
        ]
        response = dashscope.MultiModalConversation.call(model=dashscope.MultiModalConversation.Models.qwen_vl_chat_v1,
                                                        messages=messages)
        new_description = response.output.choices[0].message.content
        print(new_description)
    except:
        new_description = "生成描述失败了,真是不好意思"
    if request.method == 'POST':
        photo.description = new_description
        photo.save()
    return render(request, 'photos/photo.html', {'photo': photo})

@login_required(login_url='login')
def delete_category_view(request, pk):
    user = request.user
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        # 删除该类别下的所有照片
        photos = Photo.objects.filter(
            category__name=category, category__user=user)
        for photo in photos:
            photo.image.delete()  # 删除服务器上的图片文件
            photo.delete()
        # 删除类别
        category.delete()
        return redirect('gallery')
    return render(request, 'photos/delete_category.html', {'category': category})

@login_required(login_url='login')
def edit_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    if request.method == 'POST':
        new_description = request.POST['description']
        photo.description = new_description
        photo.save()
    return render(request, 'photos/photo.html', {'photo': photo})

@login_required(login_url='login')
def delete_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    if request.method == 'POST':
        photo.image.delete()
        photo.delete()
        return redirect('gallery')
    return render(request, 'photos/delete_photo.html', {'photo': photo})

def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')

    return render(request, 'photos/login_register.html', {'page': page})

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('gallery')
        else:
            print("here")
    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)

@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})

@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)