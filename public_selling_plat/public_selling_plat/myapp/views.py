from django.shortcuts import render,redirect
from .models import User, log
from datetime import date
from django.shortcuts import redirect
import calendar
from django.http import HttpResponse, HttpResponseRedirect
import time
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # 设置无头后端
import matplotlib.pyplot as plt
# 网页 参数 只能或者说必须含有 request 请求
# get post
# 首页
def index(request):
    if request.method == 'GET':
        user_name = request.session["info"]['name']
        user = User.objects.get(name=user_name)
        print(user.id)
        return render(request,'index.html',locals())
# 前后端 交互 request 请求 get post
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import time
import json
from .models import User, log

from django.views.decorators.csrf import ensure_csrf_cookie
import json
import time
from django.http import JsonResponse
from django.shortcuts import render
from django.middleware.csrf import get_token
from .models import User, log

@ensure_csrf_cookie
def login(request):
    if request.method == 'GET':
        # 返回包含前端 Vue 应用的基础模板
        return render(request, 'login.html')

    if request.method == 'POST':
        # 解析 JSON 数据
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # ORM 查询
        exists = User.objects.filter(name=username, password=password).exists()
        if not exists:
            return JsonResponse({'error': '用户名或密码错误！'}, status=401)

        times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        log.objects.create(name=username, time=times)
        p = User.objects.filter(name=username, password=password).values('role')[0]['role']

        # 设置会话信息
        request.session["info"] = {'name': username}

        # 判断是否是 admin
        if username == 'admin':
            return JsonResponse(
                {'message': '登录成功', 'role': 'admin', 'redirect': '/myapp/index'})
        else:
            return JsonResponse(
                {'message': '登录成功', 'role': p, 'redirect': '/myapp/guest_index'})

# 第三章 功能模块
# 第四章 怎么实线的
# 退出登录

def log_out(request):
    if request.method =='GET':
        # del request.session["info"]
        return redirect('/myapp/login')
# 中间件
# 注册
from django.middleware.csrf import get_token


from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import User
# 其他需要的导入

@ensure_csrf_cookie
def regist(request):
    if request.method == 'GET':
        return render(request, 'regist.html')
    else:
        # 解析 JSON 数据
        data = json.loads(request.body)
        print(data)
        username = data.get('username')  # 用户名
        password = data.get('password')  # 密码
        role = 'guest'  # 默认角色为 guest
        email = data.get('email')  # 邮箱
        sname = data.get('sname')  # 姓名
        school = data.get('school')  # 所在区
        sex = data.get('sex')  # 性别
        phone = data.get('phone')  # 手机号码

        exists = User.objects.filter(name=username).exists()
        if exists:
            return JsonResponse({'error': '该用户名已被注册！'}, status=400)

        # 创建新用户并保存新的字段值
        User.objects.create(
            name=username,
            password=password,
            role=role,
            email=email,
            sname=sname,
            school=school,
            sex=sex,
            phone=phone
        )
        return JsonResponse({'message': 'registered successfully, please log in!'})

# pip freezen > requirements.txt
# 登录日志
def login_log(request):
    if request.method =='GET':
        info = log.objects.all()
        return render(request,'login_log.html',locals())

# 用户管理
def user_info(request):
    if request.method=='GET':
        info = User.objects.all()
        return render(request, 'user_info.html', locals())

# 用户删除
def user_delete(request,username,password):
    if request.method=='GET':
        a = username
        b = password
        p = User.objects.filter(name=a,password=b)
        p.delete()
        # 使用redirect 可以保证url不会错误
        return redirect('/myapp/login')

# 用户修改
def user_alter(request,username,password):
    a = username
    b = password
    if request.method=='GET':
        info  = User.objects.filter(name=a,password=b)
        return render(request,'user_alter.html',locals())
    elif request.method=='POST':
        a = a
        b = b
        c = request.POST['aa']
        d = request.POST['bb']
        User.objects.filter(name=a, password=b).update(name=c, password=d)
        return redirect('/myapp/login')

# 用户创建信息 guest_profile_edit
def guest_profile_edit(request):
    if request.method=='GET':
        user_name = request.session["info"]['name']
        print('用户信息',user_name)
        user = User.objects.get(name=user_name)
        return render(request, 'guest_profile_edit.html', locals())

# 完善信息
def guest_profile_edit_upload(request):
    if request.method == 'POST':
        bio = request.POST['bio']
        signature = request.POST['signature']
        english_name = request.POST['english_name']
        email = request.POST['email']
        sex = request.POST['sex']
        status = request.POST['status']
        uid = request.POST['uid']

        phone = request.POST['phone']
        skills = request.POST['skills']
        user_name = request.session["info"]['name']
        print('用户信息',user_name)
        user_profile = User.objects.get(name=user_name)
        user_profile.bio = bio
        user_profile.signature = signature
        user_profile.english_name = english_name
        user_profile.email = email
        user_profile.sex = sex
        user_profile.status = status
        user_profile.uid = uid
        user_profile.phone = phone
        # if avatar:
        #     user_profile.avatar = file_path
        user_profile.skills = skills
        user_profile.save()
    return render(request, 'guest_index.html',locals())

# 首页
def guest_index(request):
    if request.method == 'GET':
        return render(request,'guest_index.html',locals())

# 信息展示
def guest_profile_display(request):
    if request.method == 'GET':
        user_name = request.session["info"]['name']
        user = User.objects.get(name=user_name)
        return render(request,'guest_profile_display.html',locals())

# 测试页面
def test(request):
    if request.method == 'GET':
        return render(request,'test.html',locals())

# 找回密码
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User

@ensure_csrf_cookie
def reset_password(request):
    if request.method == 'GET':
        return render(request, 'reset_password.html')
    elif request.method == 'POST':
        # 解析 JSON 数据
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')

        user = User.objects.filter(name=username, email=email).first()
        if user:
            # 如果用户名和邮箱匹配，返回成功信息和重定向 URL
            url = f'/myapp/change_password/{user.id}'
            return JsonResponse({'redirect_url': url})
        else:
            # 如果不匹配，返回错误消息
            return JsonResponse({'error': '用户名或邮箱不正确'}, status=400)

# 创建密码重置
@ensure_csrf_cookie
def change_password(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': '用户不存在'}, status=404)

    if request.method == 'GET':
        return render(request, 'change_password.html', {'user': user})
    elif request.method == 'POST':
        # 解析 JSON 数据
        data = json.loads(request.body)
        new_password = data.get('new_password')
        user.password = new_password
        user.save()
        # 返回成功消息
        return JsonResponse({'message': '密码已成功重置，请登录', 'redirect_url': '/myapp/login'})

# 对用户进行管理
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .forms import UserForm

def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/myapp/manage_users')
    else:
        form = UserForm()
    return render(request, 'create_user.html', {'form': form})

def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/myapp/manage_users')
    else:
        form = UserForm(instance=user)
    return render(request, 'update_user.html', {'form': form, 'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('/myapp/manage_users')

from .models import Email
from django.utils import timezone

def email_editor(request):
    if request.method == 'POST':
        recipient = request.POST['recipient']
        subject = request.POST['subject']
        body = request.POST['body']
        sent_time = timezone.now()
        user_name = request.session["info"]['name']
        email = Email(recipient=recipient, subject=subject, body=body, sent_time=sent_time,sender = user_name)
        email.save()

        return redirect('/myapp/guest_index')
    users = User.objects.all()
    return render(request, 'email_editor.html',locals())

# 邮件删除
def email_manage(request,id):
    if request.method == 'GET':
        p = Email.objects.filter(id = id).first()
        p.delete()
        return redirect('/myapp/index')

# 邮件展示
def email_presentation(request):
    if request.method == 'GET':
        info = Email.objects.all()

        return render(request, 'email_presentation.html',locals())


def email_single_presentation(request):
    emails = Email.objects.all()
    subjects = Email.objects.values_list('subject', flat=True).distinct()
    context = {'info': emails, 'subjects': subjects}
    return render(request, 'email_single_presentation.html', context)

def watch(request,id):
    if request.method =='GET':
        email = Email.objects.filter(id = id).first()
        return render(request,'watch.html',locals())

# 设置问题
from django.shortcuts import render, get_object_or_404
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

def upload_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/myapp/index')
    else:
        form = QuestionForm()
    return render(request, 'upload_question.html', {'form': form})

def display_questions(request):
    questions = Question.objects.all()
    return render(request, 'display_questions.html', {'questions': questions})

def upload_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('/myapp/display_questions')
    else:
        form = AnswerForm()
    return render(request, 'upload_answer.html', {'form': form, 'question': question})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Question

def manage_questions(request):
    questions = Question.objects.all()
    return render(request, 'manage_questions.html', {'questions': questions})

def delete_question(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        return redirect('/myapp/manage_questions')
    else:
        return redirect('/myapp/manage_questions')


from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Item

# 创建商品
def create_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        category = request.POST['category']
        location = request.POST['location']
        price_per_day = request.POST['price_per_day']
        available_from = request.POST['available_from']
        available_to = request.POST.get('available_to', None)
        url = request.POST.get('url', None)  # 新增的URL字段

        # 获取当前用户
        owner = User.objects.get(name=request.session["info"]['name'])

        # 创建商品信息
        item = Item.objects.create(
            name=name,
            description=description,
            category=category,
            location=location,
            price_per_day=price_per_day,
            available_from=available_from,
            available_to=available_to,
            owner=owner,
            is_available=True,
            url=url  # 保存URL字段
        )
        item.save()
        return redirect('/myapp/user_items')  # 重定向到查看自己商品信息页面
    return render(request, 'create_item.html', locals())  # 使用guest_layout.html继承


from .models import Item
def user_items(request):
    # 获取当前用户
    user_name = request.session["info"]['name']
    owner = User.objects.get(name=user_name)

    # 获取用户的所有商品信息
    items = Item.objects.filter(owner=owner)

    return render(request, 'user_items.html', locals())  # 使用guest_layout.html继承

from django.core.paginator import Paginator

from django.shortcuts import render
from .models import Item  # 确保导入了 Item 模型

def all_available_items(request):
    # 获取所有可租赁的商品信息
    items = Item.objects.filter(is_available=True).order_by('-created_at')

    # 获取推荐商品（或其他筛选条件下的商品）
    featured_items = Item.objects.filter(is_available=True).order_by('-created_at')[:5]  # 示例：前 5 个推荐商品

    # 分页，每页显示10个商品
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 将 featured_items 传递给模板
    return render(request, 'all_available_items.html', {'page_obj': page_obj, 'featured_items': featured_items})


from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Item, Rental

from django.shortcuts import render, redirect
from .models import Item, Rental
from datetime import datetime


def rent_item(request, item_id):
    item = Item.objects.get(id=item_id)

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        # 将日期字符串转换为日期对象
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # 检查租赁时间是否与已有的租赁冲突
        existing_rentals = Rental.objects.filter(item=item, end_date__gte=start_date, start_date__lte=end_date)
        if existing_rentals.exists():
            # 租赁时间冲突，返回错误
            return render(request, 'rent_item.html', {'item': item, 'error': '租赁时间冲突，请选择其他时间。'})

        # 创建租赁记录
        rental = Rental.objects.create(
            user=User.objects.get(name=request.session["info"]['name']),
            item=item,
            start_date=start_date,
            end_date=end_date
        )
        rental.save()
        return redirect(f'/myapp/payment/{rental.id}')  # 重定向到支付页面

    return render(request, 'rent_item.html', {'item': item})


def confirm_payment(request, rental_id):
    rental = Rental.objects.get(id=rental_id)

    # 模拟支付成功逻辑
    rental.payment_status = 'Completed'
    rental.status = 'Confirmed'  # 更新租赁状态为 "Confirmed"
    rental.save()

    return render(request, 'payment.html', {'rental': rental, 'payment_success': True})



from django.shortcuts import redirect
from .models import Item, Like


def like_item(request, item_id):
    item = Item.objects.get(id=item_id)
    user = User.objects.get(name=request.session["info"]['name'])

    # 检查用户是否已经喜欢该商品
    if not Like.objects.filter(user=user, item=item).exists():
        Like.objects.create(user=user, item=item)

    return redirect('/myapp/all_available_items')


from django.shortcuts import redirect
from .models import Item, Favorite


def favorite_item(request, item_id):
    item = Item.objects.get(id=item_id)
    user = User.objects.get(name=request.session["info"]['name'])

    # 检查用户是否已经收藏该商品
    if not Favorite.objects.filter(user=user, item=item).exists():
        Favorite.objects.create(user=user, item=item)

    return redirect('/myapp/all_available_items')


from django.shortcuts import render
from .models import Rental

def payment(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    return render(request, 'payment.html', {'rental': rental})


from django.shortcuts import render, redirect
from .models import Rental, Item
from datetime import datetime
from django.shortcuts import render, redirect
from .models import Rental, Item
from datetime import datetime

def confirm_rental(request, item_id):
    item = Item.objects.get(id=item_id)

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        # 将日期字符串转换为日期对象
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # 检查租赁时间是否与已有的租赁时间冲突
        existing_rentals = Rental.objects.filter(item=item)

        for rental in existing_rentals:
            if not (end_date < rental.start_date or start_date > rental.end_date):
                # 如果用户选择的时间段与现有的租赁时间冲突
                return render(request, 'rent_item.html', {'item': item, 'error': '租赁时间冲突，请选择其他时间。'})

        # 创建租赁记录
        rental = Rental.objects.create(
            renter=User.objects.get(name=request.session["info"]['name']),
            item=item,
            start_date=start_date,
            end_date=end_date,
            total_price=(end_date - start_date).days * item.price_per_day
        )
        rental.save()

        # 重定向到支付页面
        return redirect(f'/myapp/payment/{rental.id}')

    # 如果是 GET 请求，则返回选择租赁时间页面
    return render(request, 'rent_item.html', {'item': item})



from django.shortcuts import render
from .models import Like, User

def my_likes(request):
    user = User.objects.get(name=request.session["info"]['name'])
    liked_items = Like.objects.filter(user=user)

    return render(request, 'my_likes.html', {'liked_items': liked_items})


from .models import Favorite

def my_favorites(request):
    user = User.objects.get(name=request.session["info"]['name'])
    favorite_items = Favorite.objects.filter(user=user)

    return render(request, 'my_favorites.html', {'favorite_items': favorite_items})


from django.shortcuts import render
from .models import Rental, User


def my_rented_items(request):
    user = User.objects.get(name=request.session["info"]['name'])
    rented_items = Rental.objects.filter(renter=user, status='Confirmed')

    return render(request, 'my_rented_items.html', {'rented_items': rented_items})


from .models import Payment,Review,Message


def my_orders(request):
    user = User.objects.get(name=request.session["info"]['name'])
    orders = Rental.objects.filter(renter=user)

    return render(request, 'my_orders.html', {'orders': orders})

# 将所有的数据全部删除
def delete_item_and_related_data(request):
    Review.objects.all().delete()
    Rental.objects.all().delete()
    Item.objects.all().delete()
    Message.objects.all().delete()
    Favorite.objects.all().delete()
    Like.objects.all().delete()
    return HttpResponse('删除成功')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Item

# 显示编辑商品的表单
def item_edit(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'GET':
        return render(request, 'item_edit.html', {'item': item})

    if request.method == 'POST':
        # 获取表单数据并更新商品信息
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.price_per_day = request.POST['price_per_day']
        item.category = request.POST['category']
        item.location = request.POST['location']
        item.available_from = request.POST['available_from']
        item.available_to = request.POST.get('available_to', None)

        item.save()

        return redirect('/myapp/user_items')  # 保存成功后重定向到商品列表


from django.db.models import Count, Avg

# 实现协同过滤


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


from django.shortcuts import render
from .models import User, Item, Favorite, Like, Review, Rental
from django.db.models import Avg, Count
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def generate_user_item_matrix():
    users = User.objects.all()
    items = Item.objects.all()

    # 初始化用户-商品评分矩阵
    user_item_matrix = {user.id: {item.id: 0 for item in items} for user in users}

    # 添加收藏数据
    favorites = Favorite.objects.values('user_id', 'item_id').annotate(count=Count('id'))
    for fav in favorites:
        user_item_matrix[fav['user_id']][fav['item_id']] += 0.4

    # 添加喜欢数据
    likes = Like.objects.values('user_id', 'item_id').annotate(count=Count('id'))
    for like in likes:
        user_item_matrix[like['user_id']][like['item_id']] += 0.3

    # 添加评分数据
    reviews = Review.objects.values('user_id', 'item_id').annotate(avg_rating=Avg('rating'))
    for review in reviews:
        user_item_matrix[review['user_id']][review['item_id']] += 0.2 * (review['avg_rating'] / 5.0)

    # 添加租赁数据
    rentals = Rental.objects.values('renter_id', 'item_id').annotate(count=Count('id'))
    for rental in rentals:
        user_item_matrix[rental['renter_id']][rental['item_id']] += 0.1

    return user_item_matrix


def recommend_items_for_user(user_id, user_item_matrix):
    user_ids = list(user_item_matrix.keys())
    item_ids = list(user_item_matrix[user_ids[0]].keys())

    matrix = np.array([[user_item_matrix[user][item] for item in item_ids] for user in user_ids])
    user_index = user_ids.index(user_id)

    # 计算用户相似性
    user_similarity = cosine_similarity(matrix)
    similar_users = np.argsort(-user_similarity[user_index])[1:6]  # 获取最相似的5个用户

    # 基于相似用户推荐
    recommended_items = {}
    for similar_user in similar_users:
        similar_user_id = user_ids[similar_user]
        for item_id, score in user_item_matrix[similar_user_id].items():
            if user_item_matrix[user_id][item_id] == 0:  # 当前用户未评分
                if item_id not in recommended_items:
                    recommended_items[item_id] = 0
                recommended_items[item_id] += score * user_similarity[user_index][similar_user]

    # 排序并返回商品ID列表
    recommended_items = sorted(recommended_items.items(), key=lambda x: -x[1])
    return [item[0] for item in recommended_items[:10]]  # 推荐前10个商品


from django.core.paginator import Paginator
from django.shortcuts import render
from .models import User, Item

def recommended_page(request):
    # 获取当前用户
    user = User.objects.get(name=request.session["info"]['name'])

    # 模拟推荐逻辑：获取所有商品（推荐算法替换为推荐的商品列表）
    recommended_items = Item.objects.all()

    # 添加分页功能，每页显示6个商品
    paginator = Paginator(recommended_items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recommended.html', {'page_obj': page_obj})

# 查看指定的物品信息
def item_detail(request, item_id):
    # 获取对应商品，如果不存在返回404
    item = get_object_or_404(Item, id=item_id)

    return render(request, 'item_detail.html', {'item': item})

# 实现物品删除
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Item

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Item, User


def item_delete(request, item_id):
    # 从 session 获取当前用户
    current_user_name = request.session["info"]["name"]
    current_user = User.objects.get(name=current_user_name)

    # 获取商品，如果不存在则返回404
    item = get_object_or_404(Item, id=item_id)

    # 检查是否是商品的所有者
    if item.owner != current_user:
        messages.error(request, "You do not have permission to delete this item.")
        return redirect('item_detail', item_id=item_id)

    # 删除商品
    item.delete()
    messages.success(request, "Item deleted successfully.")

    # 删除后重定向到商品列表或其他页面


    return redirect('/myapp/user_items')