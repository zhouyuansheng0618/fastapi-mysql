# -*- coding: utf-8 -*-
# @Author : zhouys
# @Contact:zhouys618@163.com
# @Software : blog_server
# @File : nblog_model
# @Time : 2021/12/20 23:07
from django.db import models


# 关于我的
class About(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)
    name_zh = models.CharField(max_length=255, blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'about'




# 标签
class BlogTag(models.Model):
    blog_id = models.BigIntegerField()
    tag_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'blog_tag'


# 分类
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'category'


# 访客城市
class CityVisitor(models.Model):
    city = models.CharField(primary_key=True, max_length=255)
    uv = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'city_visitor'


# 评论
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    create_time = models.DateTimeField(blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    is_published = models.TextField()  # This field type is a guess.
    is_admin_comment = models.TextField()  # This field type is a guess.
    page = models.IntegerField()
    is_notice = models.TextField()  # This field type is a guess.
    blog_id = models.BigIntegerField(blank=True, null=True)
    parent_comment_id = models.BigIntegerField()
    website = models.CharField(max_length=255, blank=True, null=True)
    qq = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


# 异常日志
class ExceptionLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    uri = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    param = models.CharField(max_length=2000, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    ip_source = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField()
    user_agent = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exception_log'




# 登录日志
class LoginLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255)
    ip = models.CharField(max_length=255, blank=True, null=True)
    ip_source = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    description = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField()
    user_agent = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'login_log'



# 操作日志
class OperationLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255)
    uri = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    param = models.CharField(max_length=2000, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    ip_source = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    times = models.IntegerField()
    create_time = models.DateTimeField()
    user_agent = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operation_log'




# 定时任务日志
class ScheduleJobLog(models.Model):
    log_id = models.BigAutoField(primary_key=True)
    job_id = models.BigIntegerField()
    bean_name = models.CharField(max_length=255, blank=True, null=True)
    method_name = models.CharField(max_length=255, blank=True, null=True)
    params = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    error = models.TextField(blank=True, null=True)
    times = models.IntegerField()
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedule_job_log'



# 访问日志
class VisitLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36, blank=True, null=True)
    uri = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    param = models.CharField(max_length=2000)
    behavior = models.CharField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    ip_source = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    times = models.IntegerField()
    create_time = models.DateTimeField()
    user_agent = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visit_log'




# 访问记录
class VisitRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    pv = models.IntegerField()
    uv = models.IntegerField()
    date = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'visit_record'

# 配置信息
class SiteSetting(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)
    name_zh = models.CharField(max_length=255, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_setting'


# 标签颜色
class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag_name = models.CharField(max_length=255)
    color = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'


# 用户
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    role = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user'

####################   为完成 ###################
# 游客
class Visitor(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    ip = models.CharField(max_length=255, blank=True, null=True)
    ip_source = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField()
    last_time = models.DateTimeField()
    pv = models.IntegerField(blank=True, null=True)
    user_agent = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visitor'
# 定时任务
class ScheduleJob(models.Model):
    job_id = models.BigAutoField(primary_key=True)
    bean_name = models.CharField(max_length=255, blank=True, null=True)
    method_name = models.CharField(max_length=255, blank=True, null=True)
    params = models.CharField(max_length=255, blank=True, null=True)
    cron = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedule_job'

# 时刻
class Moment(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    create_time = models.DateTimeField()
    likes = models.IntegerField(blank=True, null=True)
    is_published = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'moment'


# 博客
class Blog(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    first_picture = models.CharField(max_length=255)
    content = models.TextField()
    description = models.TextField()
    is_published = models.TextField()  # This field type is a guess.
    is_recommend = models.TextField()  # This field type is a guess.
    is_appreciation = models.TextField()  # This field type is a guess.
    is_comment_enabled = models.TextField()  # This field type is a guess.
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    views = models.IntegerField()
    words = models.IntegerField()
    read_time = models.IntegerField()
    category_id = models.BigIntegerField()
    is_top = models.TextField()  # This field type is a guess.
    password = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blog'


# 朋友
class Friend(models.Model):
    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    is_published = models.TextField()  # This field type is a guess.
    views = models.IntegerField()
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'friend'
