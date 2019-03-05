from django.db import models
from django.contrib.auth.models import User


class AcademicInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=255, db_index=True)

    # TODO 如有需要为name字段添加索引
    name = models.CharField(max_length=255, blank=True, null=True)
    amount1 = models.IntegerField(blank=True, null=True)
    amount2 = models.IntegerField(blank=True, null=True)
    h_index = models.IntegerField(blank=True, null=True)
    core = models.CharField(max_length=255, blank=True, null=True)
    cssci = models.CharField(max_length=255, blank=True, null=True)
    rdfybkzl = models.CharField(max_length=255, blank=True, null=True)

    # TODO co_expert更改为ForeignKey字段
    # co_expert = models.ForeignKey(BasicInfo, blank=True, null=True)
    co_expert = models.CharField(max_length=255, blank=True, null=True)
    co_agency = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'academic_info'

    def __str__(self):
        return self.name + " h_index: " + str(self.h_index)


class BasicInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    # TODO 如有需要为name字段添加索引
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    theme_list = models.CharField(max_length=255, blank=True, null=True)
    sub_list = models.CharField(max_length=255, blank=True, null=True)
    resume = models.TextField(blank=True, null=True)
    img_url = models.CharField(max_length=255, blank=True, null=True)
    url1 = models.CharField(max_length=255, blank=True, null=True)
    url2 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'basic_info'
        verbose_name = '专家信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name + " " + self.university


class ExpertIntro(models.Model):
    # TODO 如有需要为name字段添加索引
    name = models.CharField(max_length=255, db_index=True)
    university = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    profile = models.TextField()
    image_url = models.CharField(max_length=255, blank=True, null=True)
    info_url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'expert_intro'

    def __str__(self):
        return self.name + " " + self.profile


class OpinionInfo(models.Model):
    content = models.TextField(blank=True, null=True)
    expert = models.ForeignKey(BasicInfo, models.DO_NOTHING, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'opinion_info'

    def __str__(self):
        return str(self.expert) + " " + str(self.content)


class PaperInfo(models.Model):
    paper_id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    authors = models.CharField(max_length=255, blank=True, null=True)
    author1 = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    author2 = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    author3 = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    author4 = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    author5 = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    # TODO author1~author5更改为authors ForeignKey字段
    # author = models.ForeignKey(BasicInfo, blank=True, bull=True)

    class Meta:
        managed = True
        db_table = 'paper_info'

    def __str__(self):
        return self.title + " " + self.authors


class InfluenceInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    field = models.CharField(max_length=255, blank=True, null=True)
    influ = models.FloatField(blank=True, null=True)
    influ_19 = models.FloatField(blank=True, null=True)
    influ_1990 = models.FloatField(blank=True, null=True)
    influ_1995 = models.FloatField(blank=True, null=True)
    influ_2000 = models.FloatField(blank=True, null=True)
    influ_2005 = models.FloatField(blank=True, null=True)
    influ_2010 = models.FloatField(blank=True, null=True)
    influ_2015 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'influence_info'


class InfluenceTime(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    influ_1989 = models.FloatField(blank=True, null=True)
    influ_1990 = models.FloatField(blank=True, null=True)
    influ_1991 = models.FloatField(blank=True, null=True)
    influ_1992 = models.FloatField(blank=True, null=True)
    influ_1993 = models.FloatField(blank=True, null=True)
    influ_1994 = models.FloatField(blank=True, null=True)
    influ_1995 = models.FloatField(blank=True, null=True)
    influ_1996 = models.FloatField(blank=True, null=True)
    influ_1997 = models.FloatField(blank=True, null=True)
    influ_1998 = models.FloatField(blank=True, null=True)
    influ_1999 = models.FloatField(blank=True, null=True)
    influ_2000 = models.FloatField(blank=True, null=True)
    influ_2001 = models.FloatField(blank=True, null=True)
    influ_2002 = models.FloatField(blank=True, null=True)
    influ_2003 = models.FloatField(blank=True, null=True)
    influ_2004 = models.FloatField(blank=True, null=True)
    influ_2005 = models.FloatField(blank=True, null=True)
    influ_2006 = models.FloatField(blank=True, null=True)
    influ_2007 = models.FloatField(blank=True, null=True)
    influ_2008 = models.FloatField(blank=True, null=True)
    influ_2009 = models.FloatField(blank=True, null=True)
    influ_2010 = models.FloatField(blank=True, null=True)
    influ_2011 = models.FloatField(blank=True, null=True)
    influ_2012 = models.FloatField(blank=True, null=True)
    influ_2013 = models.FloatField(blank=True, null=True)
    influ_2014 = models.FloatField(blank=True, null=True)
    influ_2015 = models.FloatField(blank=True, null=True)
    influ_2016 = models.FloatField(blank=True, null=True)
    influ_2017 = models.FloatField(blank=True, null=True)
    influ_2018 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'influ_time'


class PapersTime(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    paper_1989 = models.FloatField(blank=True, null=True)
    paper_1990 = models.FloatField(blank=True, null=True)
    paper_1991 = models.FloatField(blank=True, null=True)
    paper_1992 = models.FloatField(blank=True, null=True)
    paper_1993 = models.FloatField(blank=True, null=True)
    paper_1994 = models.FloatField(blank=True, null=True)
    paper_1995 = models.FloatField(blank=True, null=True)
    paper_1996 = models.FloatField(blank=True, null=True)
    paper_1997 = models.FloatField(blank=True, null=True)
    paper_1998 = models.FloatField(blank=True, null=True)
    paper_1999 = models.FloatField(blank=True, null=True)
    paper_2000 = models.FloatField(blank=True, null=True)
    paper_2001 = models.FloatField(blank=True, null=True)
    paper_2002 = models.FloatField(blank=True, null=True)
    paper_2003 = models.FloatField(blank=True, null=True)
    paper_2004 = models.FloatField(blank=True, null=True)
    paper_2005 = models.FloatField(blank=True, null=True)
    paper_2006 = models.FloatField(blank=True, null=True)
    paper_2007 = models.FloatField(blank=True, null=True)
    paper_2008 = models.FloatField(blank=True, null=True)
    paper_2009 = models.FloatField(blank=True, null=True)
    paper_2010 = models.FloatField(blank=True, null=True)
    paper_2011 = models.FloatField(blank=True, null=True)
    paper_2012 = models.FloatField(blank=True, null=True)
    paper_2013 = models.FloatField(blank=True, null=True)
    paper_2014 = models.FloatField(blank=True, null=True)
    paper_2015 = models.FloatField(blank=True, null=True)
    paper_2016 = models.FloatField(blank=True, null=True)
    paper_2017 = models.FloatField(blank=True, null=True)
    paper_2018 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'papers_time'


class PaperRelation(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    coid_list = models.CharField(max_length=255, blank=True, null=True)
    year_list = models.CharField(max_length=255, blank=True, null=True)
    score_list = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paper_relation_score'


class OrganizationInfo(models.Model):
    index = models.IntegerField(primary_key=True)
    col = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    attach = models.CharField(max_length=255, blank=True, null=True)
    loc = models.CharField(max_length=255, blank=True, null=True)
    teach = models.CharField(max_length=255, blank=True, null=True)
    con = models.CharField(max_length=255, blank=True, null=True)
    img_url = models.CharField(max_length=255, blank=True, null=True)
    intro = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organization_info'


class OpinionRaw(models.Model):
    id = models.CharField(primary_key=True, max_length=255, db_index=True)
    content = models.TextField(blank=True, null=True)
    expert_id = models.CharField(max_length=255, db_index=True)
    expert_name = models.CharField(max_length=255, blank=True, null=True)
    expert_university = models.CharField(max_length=255, blank=True, null=True)
    expert_college = models.CharField(max_length=255, blank=True, null=True)
    expert_organization = models.CharField(max_length=255, blank=True, null=True)
    source_url = models.CharField(max_length=255, blank=True, null=True)
    article_url = models.TextField(blank=True, null=True)
    article_title = models.TextField(blank=True, null=True)
    article_source = models.TextField(blank=True, null=True)
    article_time = models.TextField(blank=True, null=True)
    article_brief = models.TextField(blank=True, null=True)
    snapshot_url = models.TextField(blank=True, null=True)
    analysis_tag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'opinion_raw'


# 自定义用户模型的作用？？？
class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=False, null=True, db_index=True)
    gender = models.CharField(max_length=10, blank=False, null=True, )
    company = models.CharField(max_length=50, blank=True, null=True, )

    class Meta:
        verbose_name = "自定义用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname


# class CustomUser(AbstractUser):
#     nickname = models.CharField(max_length=255, blank=False, null=True, db_index=True)
#
#     class Meta:
#         verbose_name = "用户信息"
#
#     def __str__(self):
#         return self.nickname


# class ExpertGroup(models.Model):
#     name = models.CharField(max_length=255, verbose_name="专家分组名")
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     expert_id = models.CharField(max_length=255)
#
#     class Meta:
#         verbose_name = "专家分组信息"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.user.username + ":" + self.name
#
#     @classmethod
#     def create(cls, name, user, expert_id):
#         expert_group = cls(name=name, user=user, expert_id=expert_id)
#         return expert_group


class UserFav(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expert_id = models.CharField(max_length=255)

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username + "收藏的" + self.expert_id

    @classmethod
    def create(cls, user, expert_id):
        user_fav = cls(user=user, expert_id=expert_id)
        return user_fav


class Hometown(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    p2id = models.CharField(max_length=255, blank=True, null=True)
    p1id = models.CharField(max_length=255, blank=True, null=True)
    list = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hometown'


class HometownRelation(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    hometown_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hometown_relation'


class ThemeRelation(models.Model):
    hash = models.CharField(primary_key=True, max_length=255)
    theme = models.CharField(max_length=255, blank=True, null=True)
    expert_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'theme_relation'
