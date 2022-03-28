from django.db import models


# Create your models here.

# 教师信息模板
class teacherModel(models.Model):
    id = models.IntegerField(primary_key=True)
    t_Name = models.CharField(max_length=20)
    t_sex = models.CharField(max_length=2)
    t_work = models.CharField(max_length=200)
    t_education = models.CharField(max_length=20)
    t_level = models.CharField(max_length=20)
    t_title = models.CharField(max_length=20)
    t_ID_card = models.CharField(max_length=50)
    t_age = models.IntegerField()
    t_from = models.CharField(max_length=30)
    t_province = models.CharField(max_length=20)
    t_school = models.CharField(max_length=20)
    t_introduction = models.TextField()


# 课程信息模板
class courseModel(models.Model):
    id = models.AutoField(primary_key=True)
    t_id = models.ForeignKey(teacherModel, on_delete=models.CASCADE)
    c_name = models.CharField(max_length=50)
    c_type = models.CharField(max_length=20)


# 身份信息模板
class identity(models.Model):
    id = models.AutoField(primary_key=True)
    identity = models.CharField(max_length=30)


# 省份信息模板
class province(models.Model):
    id = models.AutoField(primary_key=True)
    t_province = models.CharField(max_length=20)


# 性别模板
class sex(models.Model):
    id = models.AutoField(primary_key=True)
    t_sex = models.CharField(max_length=20)


# 教育程度模板
class education(models.Model):
    id = models.AutoField(primary_key=True)
    t_education = models.CharField(max_length=20)


# 职称模板
class level(models.Model):
    id = models.AutoField(primary_key=True)
    t_level = models.CharField(max_length=20)


# 级别模板
class title(models.Model):
    id = models.AutoField(primary_key=True)
    t_title = models.CharField(max_length=20)


# 机关部门模板
class fromWhere(models.Model):
    id = models.AutoField(primary_key=True)
    t_from = models.CharField(max_length=20)


# 校内外模板模板
class school(models.Model):
    id = models.AutoField(primary_key=True)
    t_school = models.CharField(max_length=20)


# 所有选项的json数据
class allOptions(models.Model):
    id = models.AutoField(primary_key=True)
    t_Name = models.JSONField()
    t_sex = models.JSONField()
    t_work = models.JSONField()
    t_education = models.JSONField()
    t_level = models.JSONField()
    t_title = models.JSONField()
    t_ID_card = models.JSONField()
    t_age = models.JSONField()
    t_from = models.JSONField()
    t_province = models.JSONField()
    t_school = models.JSONField()
    t_introduction = models.JSONField()


# 课程信息模板
class courseCategoryModel(models.Model):
    id = models.IntegerField(primary_key=True)
    c_name = models.CharField(max_length=100)
    c_outORin = models.CharField(max_length=100)
    c_category = models.CharField(max_length=100)
    c_month = models.CharField(max_length=200)
    c_cycle = models.CharField(max_length=20)
    c_people = models.CharField(max_length=20)
    c_year = models.CharField(max_length=20)


# 培训班类别1
class courseCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=100)


# 培训班类别2
class courseCategory2(models.Model):
    id = models.IntegerField(primary_key=True)
    category2 = models.CharField(max_length=100)

# 年份
class allyears(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.CharField(max_length=100)