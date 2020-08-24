from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from parsing import models


class MainView(generic.TemplateView):
    template_name = 'parsing/base.html'


class SiteListView(generic.ListView):
    model = models.Site
    template_name = 'parsing/site_list.html'
    paginate_by = 10


class SiteDetailView(SuccessMessageMixin, generic.DetailView):
    model = models.Site


class SiteCreateView(SuccessMessageMixin, generic.CreateView):
    model = models.Site
    fields = ['brand', 'url', 'schedule', 'enabled']
    success_message = "%(brand)s was created successfully"
    success_url = reverse_lazy('parsing:site-list')


class SiteUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = models.Site
    fields = ['brand', 'url', 'schedule', 'enabled']
    success_message = "%(brand)s was updated successfully"
    success_url = reverse_lazy('parsing:site-list')


class SiteDeleteView(SuccessMessageMixin, generic.DeleteView):
    model = models.Site
    success_message = "%(barnd)s was deleted successfully"
    success_url = reverse_lazy('parsing:site-list')


class SitemapListView(generic.ListView):
    model = models.Sitemap
    paginate_by = 10


class SitemapDetailView(generic.DetailView):
    model = models.Sitemap


class SitemapCreateView(SuccessMessageMixin, generic.CreateView):
    model = models.Sitemap
    fields = ['site', 'url', 'schedule', 'enabled']
    success_message = "%(url)s was created successfully"
    success_url = reverse_lazy('parsing:sitemap-list')


class SitemapUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = models.Sitemap
    fields = ['site', 'url', 'schedule', 'enabled']
    success_message = "%(url)s was updated successfully"
    success_url = reverse_lazy('parsing:sitemap-list')


class SitemapDeleteView(SuccessMessageMixin, generic.DeleteView):
    model = models.Sitemap
    success_message = "%(url)s was deleted successfully"
    success_url = reverse_lazy('parsing:sitemap-list')


class GoodurlListView(SuccessMessageMixin, generic.ListView):
    model = models.GoodURL
    paginate_by = 50


class GoodurlDetailView(SuccessMessageMixin, generic.DetailView):
    model = models.GoodURL


class GoodurlCreateView(SuccessMessageMixin, generic.CreateView):
    model = models.GoodURL
    fields = ['sitemap', 'url']
    success_message = "%(url)s was created successfully"
    success_url = reverse_lazy('parsing:goodurl-list')


class GoodurlUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = models.GoodURL
    fields = ['sitemap', 'url']
    success_message = "%(url)s was updated successfully"
    success_url = reverse_lazy('parsing:goodurl-list')


class GoodurlDeleteView(SuccessMessageMixin, generic.DeleteView):
    model = models.GoodURL
    success_message = "%(url)s was deleted successfully"
    success_url = reverse_lazy('parsing:goodurl-list')
