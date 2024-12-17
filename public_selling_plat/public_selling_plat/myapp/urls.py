from django.urls import path
from .import views
urlpatterns =[
    # 首页
    path('index', views.index),
    # 登录
    path('login', views.login),
    # 退出登录
    path('log_out', views.log_out),
    # 注册
    path('regist', views.regist),
    # 系统的登录日志
    path('login_log', views.login_log),
    # 用户管理
    path('user_info', views.user_info),
    # 删除用户
    path('user_delete/<str:username>/<str:password>', views.user_delete),
    # 修改用户
    path('user_alter/<str:username>/<str:password>', views.user_alter),
    # 创建信息 guest_profile_edit
    path('guest_profile_edit', views.guest_profile_edit),
    # 完善信息 guest_profile_edit_upload
    path('guest_profile_edit_upload', views.guest_profile_edit_upload),
    # 首页
    path('guest_index', views.guest_index),
    # 信息展示
    path('guest_profile_display', views.guest_profile_display),
    # 测试页面
    path('test', views.test),
    # 找回密码
    path('reset_password', views.reset_password),
    # 修改密码
    path('change_password/<int:user_id>', views.change_password),
    # 业务逻辑
    # 用户管理
    path('manage_users', views.manage_users),
    path('create_user', views.create_user),
    path('update_user/<int:user_id>', views.update_user),
    path('delete_user/<int:user_id>', views.delete_user),
    # 邮件发送
    path('email_editor', views.email_editor),
    # 邮件删除
    path('email_manage/<int:id>', views.email_manage),
    # 邮件展示
    path('email_presentation', views.email_presentation),
    # 邮件单条展示email_single_presentation
    path('email_single_presentation', views.email_single_presentation),
    # 详情 watch
    path('watch/<int:id>', views.watch),
    # 管理员设置问题
    path('upload_question', views.upload_question),
    path('display_questions', views.display_questions),
    path('upload_answer/<int:question_id>',views.upload_answer),
    # 管理问题和答案
    path('manage_questions', views.manage_questions),
    path('delete_question/<int:question_id>', views.delete_question),
    path('create_item', views.create_item, name='create_item'),  # 创建商品
    path('user_items', views.user_items, name='user_items'),  # 查看自己发布的商品
    path('all_available_items', views.all_available_items, name='all_available_items'),  # 查看所有可租赁商品 (分页)
    # 喜欢商品...
    path('like_item/<int:item_id>', views.like_item, name='like_item'),  # 喜欢商品
    path('favorite_item/<int:item_id>', views.favorite_item, name='favorite_item'),  # 收藏商品
    path('rent_item/<int:item_id>', views.rent_item, name='rent_item'),  # 租赁商品
    path('rent_item/<int:item_id>/confirm', views.confirm_rental, name='confirm_rental'),  # 确认租赁
    path('payment/<int:rental_id>', views.payment, name='payment'),  # 支付页面
    path('payment/<int:rental_id>/confirm', views.confirm_payment, name='confirm_payment'),  # 确认支付
    # 展示喜欢 收藏
    path('my_likes', views.my_likes, name='my_likes'),  # 我的喜欢
    path('my_favorites', views.my_favorites, name='my_favorites'),  # 我的收藏
    path('my_rented_items', views.my_rented_items, name='my_rented_items'),  # 展示已租赁的商品
    path('my_orders', views.my_orders, name='my_orders'),  # 展示我的所有订单
    path('delete_item_and_related_data', views.delete_item_and_related_data, name='delete_item_and_related_data'),  # 展示我的所有订单
    path('item_edit/<int:item_id>', views.item_edit, name='item_edit'),
    path('recommended_page', views.recommended_page, name='recommendations'),
    path('item_detail/<int:item_id>', views.item_detail, name='item_detail'),
    path('item_delete/<int:item_id>', views.item_delete, name='item_delete'),
]
