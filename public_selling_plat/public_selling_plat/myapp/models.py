from django.db import models
from django.utils import timezone

class User(models.Model):
    # id
    # 创建用户模型 int text date
    # 字段名
    name = models.CharField("用户名", max_length=50, default='', null=False)
    sname = models.CharField("真实姓名", max_length=50, default='', null=False)
    password = models.CharField("密码", max_length=50, default='', null=False)
    role = models.CharField("角色", max_length=50, default='', null=False)
    bio = models.CharField("个人介绍", max_length=500, default='', null=True)
    signature = models.CharField("个性签名", max_length=50, default='', null=True)
    english_name = models.CharField("英文名", max_length=50, default='', null=True)
    phone = models.CharField("手机号码", max_length=50, default='', null=True)
    avatar = models.CharField("头像url", max_length=200, default='', null=True)
    skills = models.CharField("职业技能", max_length=50, default='', null=True)
    uid = models.CharField("编号", max_length=50, default='', null=True)
    status = models.CharField("状态", max_length=50, default='', null=True)
    email = models.EmailField("邮箱", max_length=100, unique=True, null=False)
    sex = models.CharField("性别", max_length=50, default='', null=True)
    school = models.CharField("地区", max_length=50, default='', null=True)

    def __str__(self):
        return self.name
# orm技术
# 用户日志类
class log(models.Model):
    name = models.CharField("用户名", max_length=50, default='', null=False)
    time = models.CharField("登陆时间", max_length=50, default='', null=False)

# 人工客服
class Email(models.Model):
    recipient = models.CharField(max_length=200, verbose_name="收件人")
    subject = models.CharField(max_length=200, verbose_name="主题")
    body = models.TextField(verbose_name="正文")
    sent_time = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")
    sender = models.CharField(max_length=200, verbose_name="发件人")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "邮件"
        verbose_name_plural = "邮件"

# 设置问答问题

class Question(models.Model):
    title = models.CharField("Title", max_length=200)
    description = models.TextField("Description")

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.TextField("公告")

    def __str__(self):
        return f"Answer to {self.question.title}"

class Item(models.Model):
    name = models.CharField("商品名称", max_length=200)
    description = models.TextField("商品描述")
    category = models.CharField("商品类别", max_length=100)
    location = models.CharField("存放地点", max_length=200)
    price_per_day = models.DecimalField("日租金", max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    available_from = models.DateField("可租赁开始日期")
    available_to = models.DateField("可租赁结束日期", null=True, blank=True)
    is_available = models.BooleanField("是否可租赁", default=True)
    url = models.URLField("商品链接", max_length=300, null=True, blank=True)  # 新增字段
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Rental(models.Model):
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    start_date = models.DateField("租赁开始日期")
    end_date = models.DateField("租赁结束日期")
    status = models.CharField("租赁状态", max_length=50, default="Pending")  # Pending, Confirmed, Cancelled
    total_price = models.DecimalField("总租金", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.renter.name} - {self.item.name}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField("评分", default=0)  # 1到5
    comment = models.TextField("评价内容", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.name} on {self.item.name}"

class Payment(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    amount = models.DecimalField("支付金额", max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField("支付日期", auto_now_add=True)
    payment_status = models.CharField("支付状态", max_length=50, default="Pending")  # Pending, Completed, Failed

    def __str__(self):
        return f"Payment for {self.rental.item.name} by {self.rental.renter.name}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField("消息内容")
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.name} to {self.recipient.name}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} 收藏了 {self.item.name}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} 喜欢了 {self.item.name}"

