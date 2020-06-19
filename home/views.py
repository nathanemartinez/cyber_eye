from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home/home.html'


class ProjectsView(TemplateView):
    template_name = 'home/projects.html'


class AboutView(TemplateView):
    template_name = 'home/about.html'


# *** ERROR PAGES ***
def error_400(request, exception=None):
    return render(request, 'home/error_pages/400.html')


def error_403(request, exception=None):
    return render(request, 'home/error_pages/403.html')


def error_404(request, exception=None):
    return render(request, 'home/error_pages/404.html')


def error_500(request, exception=None):
    return render(request, 'home/error_pages/500.html')


