# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
import datetime


# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=400, db_index=True)  # 名称  , 指定 db_index=True
    create_time = models.DateTimeField(default=datetime.datetime.now(), db_index=True)
    modify_time = models.DateTimeField(default=datetime.datetime.now(), blank=True, null=True)
    status = models.IntegerField(default=0)  # 0-隐藏，1-有效，-1删除
    operator_id = models.CharField(max_length=50, blank=True, null=True)  # 操作员id
    creator_id = models.CharField(max_length=50, blank=True, null=True)  # 创建人id
    owner_id = models.CharField(max_length=50, blank=True, null=True)  # 所属人id

    def __unicode__(self):
        # return self.name, self.create_time, self.modify_time, self.status, self.ops_user_id
        return self.name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        result = dict([(attr, getattr(self, attr)) for attr in
                       [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
        result['id'] = str(self.id)  # 对uuid 做转换
        return result

    class Meta:
        abstract = True

class DictModel(BaseModel):
    first_type = models.CharField(max_length=200, blank=True, null=True)  # 一级类型
    second_type = models.CharField(max_length=200, blank=True, null=True)  # 二级类型
    third_type = models.CharField(max_length=200, blank=True, null=True)  # 三级类型
    fourth_type = models.CharField(max_length=200, blank=True, null=True)  # 四级类型
    fifth_type = models.CharField(max_length=200, blank=True, null=True)  # 五级类型
    tags = models.CharField(max_length=200, blank=True, null=True)  # 分类标签
    describe = models.CharField(max_length=2000, blank=True, null=True)  # 描述

    class Meta:
        abstract = True


# 玩家设定表
class SettingPlayerModel(BaseModel):
    class Meta:
        db_table = "setting_player"
        ordering = ['-create_time']

# 门人(使魔) 设定表
class SettingServantModel(BaseModel):
    race = models.CharField(max_length=100, blank=True, null=True) #种族
    sex = models.IntegerField(default=0);  # 0-无性别，1-男， 2-女
    age = models.IntegerField(default=0);  # 年龄
    tags = models.CharField(max_length=500, blank=True, null=True)  # 分类标签
    describe = models.CharField(max_length=2000, blank=True, null=True)  # 生平描述
    head_image = models.CharField(max_length=200, blank=True, null=True)  # 头像
    full_image = models.CharField(max_length=200, blank=True, null=True)  # 立绘
    fight_image = models.CharField(max_length=200, blank=True, null=True)  # 战斗图标
    quality = models.IntegerField(default=0)  # 0-凡品，1-地品，2-天品，3-神品
    base_linggen = models.IntegerField(default=0);  # 灵根，影响法力值，法力回复速度，修炼速度，渡劫成功率， 共4档，凡，地，天，神，每档分为上中下三阶， 共分12阶
    base_lingti = models.IntegerField(default=0);  # 灵体，影响生命值，生命恢复速度，防御力，基础攻击力，共4档，凡，地，天，神，每档分为上中下三阶， 共分12阶
    base_lingzhi = models.IntegerField(default=0);  # 灵智，影响神识，影响会心率,影响法术攻击力，共4档，凡，地，天，神，每档分为上中下三阶， 共分12阶
    base_hp = models.IntegerField(default=0);  # 基础生命值
    base_hp_recovery = models.IntegerField(default=0);  # 基础生命恢复速度
    base_mp = models.IntegerField(default=0);  # 基础法力值
    base_mp_recovery = models.IntegerField(default=0);  # 基础法力恢复速度
    base_ep = models.IntegerField(default=0);  # 基础精元值 用于释放神通和激活法宝大招 每场战斗固定数量，战斗中可以通过丹药补充三次

    base_attack = models.IntegerField(default=0);  # 基础攻击力
    base_defenses = models.IntegerField(default=0);  # 基础防御力
    base_speed = models.IntegerField(default=0);  # 基础速度，决定回合攻击的出手顺序
    base_shenshi = models.IntegerField(default=0);  # 基础神识，神识大小影响可以装备的法宝数量和品质上限。
    base_huixin = models.IntegerField(default=0);  # 基础会心，影响攻击的暴击率。
    main_attribute = models.IntegerField(default=0);  # 五行主属性，1-10分别对应，金木水火土，风雷，光暗，混沌
    special_body = models.CharField(max_length=500, blank=True, null=True);  # 特殊体质，使用枚举值列表


    class Meta:
        db_table = "setting_servant"
        ordering = ['-create_time']

# 道具表
class SettingPropModel(BaseModel):
    tags = models.CharField(max_length=500, blank=True, null=True)  # 分类标签
    describe = models.CharField(max_length=2000, blank=True, null=True)  # 描述
    head_image = models.CharField(max_length=200, blank=True, null=True)  # 头像
    full_image = models.CharField(max_length=200, blank=True, null=True)  # 立绘
    fight_image = models.CharField(max_length=200, blank=True, null=True)  # 战斗图标
    quality = models.IntegerField(default=0)  # 0-凡品，1-地品，2-天品，3-神品
    base_realm = models.IntegerField(default=0)  # 境界，0-10 分别为，炼气，筑基，金丹，元婴， 地仙，灵仙，上仙，天仙，金仙， 至尊
    base_attack = models.IntegerField(default=0);  # 基础攻击力
    base_defenses = models.IntegerField(default=0);  # 基础防御力
    base_speed = models.IntegerField(default=0);  # 基础速度，决定回合攻击的出手顺序
    base_huixin = models.IntegerField(default=0);  # 基础会心，影响攻击的暴击率。
    base_shenshi = models.IntegerField(default=0);  # 基础神识消耗值，等级越高，消耗的神识越大。
    main_attribute = models.IntegerField(default=0);  # 五行主属性，1-10分别对应，金木水火土，风雷，光暗，混沌
    special_body = models.CharField(max_length=500, blank=True, null=True);  # 特殊功能，使用枚举列表

    class Meta:
        db_table = "setting_prop"
        ordering = ['-create_time']
