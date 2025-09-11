from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import Profile


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request,f"{request.user.username}, daha önce login oldunuz!")
        return redirect("/app_monitor")
    content=request.POST
    print(f"content:{content} ")
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get('password')
        print(f"request.method==post girdi")
        user_get=User.objects.get(email=username)
        print(f"user.password:{user_get.password},user.email:{user_get.email}")
        user=authenticate(request,username=username,password=password)
        print(f"user:{user}")
        if user is not None:
            login(request,user)
            messages.success(request,f"{request.user.username}, login oldunuz!")
            return redirect('/app_monitor')
    context=dict()
    return render(request,"app_user_profile/login.html",context)

def logout_view(request):
    logout(request)
    messages.info(request,f"{request.user.username}, logout oldunuz.")
    return redirect('/app_monitor')

def register_view(request):
    if request.method=="POST":
        post_info=request.POST
        email=post_info.get('email')
        email_confirm=post_info.get('email_confirm')
        password=post_info.get('password')
        password_confirm=post_info.get('password_confirm')
        firstname=post_info.get('firstname')
        # firstname_confirm=post_info.get('firstname_confirm')
        lastname=post_info.get('lastname')
        # lastname_confirm=post_info.get('lastname_confirm')
        print('*'*30)
        print(email,email_confirm,password,password_confirm,firstname,lastname)
        if email!=email_confirm:
            messages.info(request,"Lütfen email doğru giriniz.")
            return redirect("app_user_profile:register_view")
        if password!=password_confirm:
            messages.info(request,"Lütfen şifreyi doğru giriniz.")
            return redirect("app_user_profile:register_view")
        user,create=User.objects.get_or_create(username=email)
        print(f"user create yapıldımı:{create}, user:{user}")
        if not create:
            user_login=authenticate(request,username=email,password=password)
            print(f"user_login: {user_login}")
            if user_login is not None:
                login(request,user_login)
                messages.success(request,"Kullanıcı zaten mevcut,yeniden login oldunuz.")
                return redirect('/app_monitor')
            else:
                messages.info(request,"Kullanıcı mevcut ancak login olamadınız,login sayfasına yönlendiriliyorsunuz.")
                print(f"user.password:{user.password},user.email:{user.email}")
                return redirect('/user/login')
        user.email=email
        user.set_password(password)
        user.first_name=firstname
        user.last_name=lastname

        print(f"user.password: {user.password},user.email:{user.email}")

        # print(f"create yapıldı {user}: user.password:{user.password}")

        profile,create_profile=Profile.objects.get_or_create(user=user)
        profile.save()
        user.save()
        print(f"user.save() sonrası user:{user}")
        messages.success(request,f"{user.username} kullanıcısı başarıyla oluşturulmuştur.")
        # user_login=authenticate(request,username=email,password=password)
        # login(request,user_login)
        messages.success(request,f"{user.username} kullanıcı kayıt edildi ve giriş yapmıştır.")
        # return redirect('home_view')
    return render(request,"app_user_profile/register.html")
