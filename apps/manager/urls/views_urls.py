# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from ..views import group,host,storage,dashboard
urlpatterns = [
    #Resource dashboard url
    url(r'^$', dashboard.ManagerDashboardView.as_view(), name='dashboard'),

    #Resource host url
    url(r'^host/$', host.ManagerHostListView.as_view(), name='host'),
    url(r'^host/create/$',host.ManagerHostCreateView.as_view(),name='hostcreate'),
    url(r'^host/(?P<pk>[0-9]+)/update/$',host.ManagerHostUpdateView.as_view(),name='hostupdate'),
    url(r'^host/(?P<pk>[0-9])/delete/$',host.ManagerHostDeleteView.as_view(),name='hostdelete'),
    url(r'^host/(?P<pk>[0-9]+)/detail/$',host.ManagerHostDetailView.as_view(),name='hostdetail'),
    url(r'^host/(?P<pk>[0-9]+)/shell/$',host.ManagerHostShellView.as_view(),name='hostshell'),

    #Resource group url
    url(r'^group/$', group.ManagerGroupListView.as_view(), name='group'),
    url(r'^group/create/$', group.ManagerGroupCreateView.as_view(), name='groupcreate'),
    url(r'^group/(?P<pk>[0-9]+)/update/', group.ManagerGroupUpdateView.as_view(), name='groupupdate'),
    url(r'^group/(?P<pk>[0-9]+)/detail/',group.ManagerGroupDetailView.as_view(),name='groupdetail'),
    url(r'^group/(?P<pk>[0-9])/delete/$', group.ManagerGroupDeleteView.as_view(), name='groupdelete'),

    #Resource storage url
    url(r'^storage/$', storage.ManagerStorageListView.as_view(), name='storage'),
    url(r'^storage/create/$', storage.ManagerStorageCreateView.as_view(), name='storagecreate'),
    url(r'^storage/(?P<pk>[0-9]+)/update/', storage.ManagerStorageUpdateView.as_view(), name='storageupdate'),
    url(r'^storage/(?P<pk>[0-9]+)/delete/', storage.ManagerStorageDeleteView.as_view(), name='storagedelete'),

    url(r'^search$', dashboard.ManagerSearchListView.as_view(), name='search'),
]