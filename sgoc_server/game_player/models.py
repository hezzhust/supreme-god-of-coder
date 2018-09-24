# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
import datetime

from game_setting.models import SettingPlayerModel,SettingServantModel,SettingPropModel,BaseModel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User



# Create your models here.
# class BaseModel(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=400, db_index=True)  # 名称  , 指定 db_index=True
#     create_time = models.DateTimeField(default=datetime.datetime.now(), db_index=True)
#     modify_time = models.DateTimeField(default=datetime.datetime.now(), blank=True, null=True)
#     status = models.IntegerField(default=0)  # 0-隐藏，1-有效，-1删除
#     operator_id = models.CharField(max_length=50, blank=True, null=True)  # 操作员id
#     creator_id = models.CharField(max_length=50, blank=True, null=True)  # 创建人id
#     owner_id = models.CharField(max_length=50, blank=True, null=True)  # 所属人id
#
#     def __unicode__(self):
#         # return self.name, self.create_time, self.modify_time, self.status, self.ops_user_id
#         return self.name
#
#     # 将属性和属性值转换成dict 列表生成式
#     def toDict(self):
#         result = dict([(attr, getattr(self, attr)) for attr in
#                        [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
#         result['id'] = str(self.id)  # 对uuid 做转换
#         return result
#
#     class Meta:
#         abstract = True


# 玩家表
class PlayerModel(BaseModel):
    setting_player = models.ForeignKey(SettingPlayerModel, models.DO_NOTHING, blank=True, null=True)
    sys_user = models.ForeignKey(User, models.DO_NOTHING)
    class Meta:
        db_table = "player"
        ordering = ['-create_time']

# 门人(使魔) 表
#
# 凡品，地品，天品，神品 对应N, R, SR, SSR 都可以培养，但是成长系数不同，可以通过九转轮回丹重铸品质
class ServantModel(BaseModel):
    setting_servant = models.ForeignKey(SettingServantModel, models.DO_NOTHING)
    owner = models.ForeignKey(PlayerModel, models.DO_NOTHING) # 所有人
    realm = models.IntegerField(default=0);  # 大境界，0-10 分别为，炼气，筑基，金丹，元婴， 地仙，灵仙，上仙，天仙，金仙， 至尊
    leavel = models.IntegerField(default=0);  # 小等级 0-10，至尊之下，分为初期，中期，后期， 其中初期三级，中期三级，后期三级，每三级对应，境界不稳，境界稳固，巅峰，以及大圆满（半步）

    quality = models.IntegerField(default=0)  # 0-凡品，1-地品，2-天品，3-神品
    linggen = models.IntegerField(default=0);  # 灵根，影响法力值，法力回复速度，修炼速度，渡劫成功率， 共4档，凡，地，天，神，每档分为上中下三阶， 共分12阶
    lingti = models.IntegerField(default=0);  # 灵体，影响生命值，生命恢复速度，防御力，基础攻击力，共4档，凡，地，天，神，每档分为上中下三阶， 共分12阶
    lingzhi = models.IntegerField(default=0);  # 灵智，影响神识，影响会心率,影响法术攻击力，共4档，凡，地，天，神，每档分为上中下三阶， 共分12阶
    hp = models.IntegerField(default=0);  # 基础生命值
    hp_recovery = models.IntegerField(default=0);  # 基础生命恢复速度
    mp = models.IntegerField(default=0);  # 基础法力值
    mp_recovery = models.IntegerField(default=0);  # 基础法力恢复速度
    ep = models.IntegerField(default=0);  # 基础精元值 用于释放神通和激活法宝大招 每场战斗固定数量，战斗中可以通过丹药补充三次

    attack = models.IntegerField(default=0);  # 基础攻击力
    defenses = models.IntegerField(default=0);  # 基础防御力
    speed = models.IntegerField(default=0);  # 基础速度，决定回合攻击的出手顺序
    shenshi = models.IntegerField(default=0);  # 神识，神识大小影响可以装备的法宝数量和品质上限。
    huixin = models.IntegerField(default=0);  # 会心，影响攻击的暴击率。
    main_attribute = models.IntegerField(default=0);  # 五行主属性，1-10分别对应，金木水火土，风雷，光暗，混沌
    special_body = models.CharField(max_length=500, blank=True, null=True);  # 特殊体质，使用枚举值列表

    class Meta:
        db_table = "player_servant"
        ordering = ['-create_time']

# 道具表
class PropModel(BaseModel):
    setting_prop = models.ForeignKey(SettingPropModel, models.DO_NOTHING)
    owner = models.ForeignKey(PlayerModel, models.DO_NOTHING)  # 所有人
    status = models.IntegerField(default=0); #-1,拆解，0-初始，1-装备
    is_locked = models.IntegerField(default=0); #-0否，1-是， 锁定无法拆解
    type =  models.IntegerField(default=0);# 灵器，灵宝，后天仙器，先天仙器，至尊道器  对应1星，2星，3星，4星，5星。
    realm = models.IntegerField(default=0);  # 境界，0-10 分别为，炼气，筑基，金丹，元婴， 地仙，灵仙，上仙，天仙，金仙， 至尊
    attack = models.IntegerField(default=0);  # 基础攻击力
    defenses = models.IntegerField(default=0);  # 基础防御力
    speed = models.IntegerField(default=0);  # 基础速度
    huixin = models.IntegerField(default=0);  # 会心，影响攻击的暴击率。
    shenshi = models.IntegerField(default=0);  # 神识消耗值

    main_attribute = models.IntegerField(default=0);  # 五行主属性，1-10分别对应，金木水火土，风雷，光暗，混沌
    special_body = models.CharField(max_length=500, blank=True, null=True);  # 特殊功能，使用枚举列表

    class Meta:
        db_table = "player_prop"
        ordering = ['-create_time']