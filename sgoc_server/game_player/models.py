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
