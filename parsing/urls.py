# -*- coding: utf-8 -*-
from django.urls import path
from parsing import views


app_name = 'parsing'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    # Site
    path('site/', views.SiteListView.as_view(), name='site-list'),
    path('site/create/', views.SiteCreateView.as_view(), name='site-create'),
    path('site/detail/<slug:slug>', views.SiteDetailView.as_view(), name='site-detail'),
    path('site/update/<slug:slug>', views.SiteUpdateView.as_view(), name='site-update'),
    path('site/delete/<slug:slug>', views.SiteDeleteView.as_view(), name='site-delete'),
    # Sitemap
    path('sitemap/', views.SitemapListView.as_view(), name='sitemap-list'),
    path('sitemap/create/', views.SitemapCreateView.as_view(), name='sitemap-create'),
    path('sitemap/detail/<int:pk>', views.SitemapDetailView.as_view(), name='sitemap-detail'),
    path('sitemap/update/<int:pk>', views.SitemapUpdateView.as_view(), name='sitemap-update'),
    path('sitemap/delete/<int:pk>', views.SitemapDeleteView.as_view(), name='sitemap-delete'),
    # GoodURL
    path('goodurl/', views.GoodurlListView.as_view(), name='goodurl-list'),
    path('goodurl/create/', views.GoodurlCreateView.as_view(), name='goodurl-create'),
    path('goodurl/detail/<int:pk>', views.GoodurlDetailView.as_view(), name='goodurl-detail'),
    path('goodurl/update/<int:pk>', views.GoodurlUpdateView.as_view(), name='goodurl-update'),
    path('goodurl/delete/<int:pk>', views.GoodurlDeleteView.as_view(), name='goodurl-delete'),
]
