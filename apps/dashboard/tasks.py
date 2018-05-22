# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab
from deveops.conf import ALIYUN_PAGESIZE,REDIS_PORT,REDIS_SPACE,EXPIREDTIME
import redis
import datetime
from deveops.utils import aliyun
from deveops.utils import resolver

connect = redis.StrictRedis(port=REDIS_PORT,db=REDIS_SPACE)

@periodic_task(run_every=crontab(minute='*'))
def aliyunECSExpiredInfoCatch():
    from dashboard.models import ExpiredAliyunECS

    ExpiredAliyunECS.objects.all().delete()
    countNumber = aliyun.fetch_ECSPage()
    threadNumber = int(countNumber/ALIYUN_PAGESIZE)
    now = datetime.datetime.now()
    for num in range(1,threadNumber+1):
        data = aliyun.fetch_Instances(num)
        for dt in data:
            expiredTime = datetime.datetime.strptime(dt['ExpiredTime'],'%Y-%m-%dT%H:%MZ')
            if 0 < (expiredTime-now).days < EXPIREDTIME:
                dt['ExpiredDay'] = (expiredTime-now).days
                ExpiredAliyunECS(**resolver.AliyunECS2Json.decode(dt)).save()


@periodic_task(run_every=crontab(minute='*'))
def aliyunRDSInfoCatch():
    from dashboard.models import ExpiredAliyunRDS

    ExpiredAliyunRDS.objects.all().delete()
    countNumber = aliyun.fetch_RDSPage()
    threadNumber = int(countNumber/ALIYUN_PAGESIZE)
    now = datetime.datetime.now()
    for num in range(1,threadNumber+1):
        data = aliyun.fetch_RDSs(num)
        for dt in data:
            if not dt['DBInstanceId'][0:2] == 'rr':
                expiredTime = datetime.datetime.strptime(dt['ExpireTime'],'%Y-%m-%dT%H:%M:%SZ')
                if 0 < (expiredTime - now).days < EXPIREDTIME:
                    dt['ExpiredDay'] = (expiredTime - now).days
                    ExpiredAliyunRDS(**resolver.AliyunRDS2Json.decode(dt)).save()


@periodic_task(run_every=crontab(minute='*'))
def managerStatusCatch():
    connect.delete('MANAGER_STATUS')
    from manager import models as Manager
    host_count = Manager.Host.objects.count()
    group_count = Manager.Group.objects.count()
    status = {
        'host_count':host_count,
        'group_count':group_count,
    }
    systypes = Manager.System_Type.objects.all()
    for sys in systypes:
        status[sys.name] = sys.hosts_detail.count()

    positions = Manager.Position.objects.all()
    for pos in positions:
        status['pos'+str(pos.id)] = pos.hosts_detail.count()

    groups = Manager.Group.objects.all()
    for group in groups:
        status[group.uuid] = group.hosts.count()

    connect.hmset('MANAGER_STATUS', status)

