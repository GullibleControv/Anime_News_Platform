from django.shortcuts import render, get_object_or_404 

from .models import Article

# This is the Homepage View
def home(request):
    articles = Article.objects.all()
    return render(request, 'news/home.html', {'articles': articles})

def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'news/detail.html', {'article': article})