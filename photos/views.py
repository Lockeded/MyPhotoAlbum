from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# Create your views here.
def delete_category_view(request, pk):
    user = request.user
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        # 删除该类别下的所有照片
        photos = Photo.objects.filter(
            category__name=category, category__user=user)
        print(photos)
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
