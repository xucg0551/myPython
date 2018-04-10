from django.db import models

# Create your models here.
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市")
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述", default='')
    tag = models.CharField(default="全国知名", max_length=10, verbose_name=u"机构标签")
    category = models.CharField(default="pxjg", verbose_name=u"机构类别", max_length=20, choices=(("pxjg","培训机构"),("gr","个人"),("gx","高校")))
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    course_nums = models.IntegerField(default=0, verbose_name=u"课程数")
    add_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
