from django.shortcuts import render


def render_index_page(request):
    return render(request, 'index/index.html')


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

def noticeboard(request):
    return render(request, 'noticeboard.html')
