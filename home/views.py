from django.shortcuts import render


def home(request):
    return render(request, 'home/home.html')


def projects(request):
    return render(request, 'home/projects.html')


def about(request):
    return render(request, 'home/about.html')


# *** ERROR PAGES ***
def error_400(request, exception=None):
    return render(request, 'home/error_pages/400.html')


def error_403(request, exception=None):
    return render(request, 'home/error_pages/403.html')


def error_404(request, exception=None):
    return render(request, 'home/error_pages/404.html')


def error_500(request, exception=None):
    return render(request, 'home/error_pages/500.html')


