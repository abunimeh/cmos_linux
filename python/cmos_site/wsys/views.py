from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from wsys.models import ArticleForm, Article
from django.contrib.auth.decorators import login_required
import datetime as dt
from reversion import revisions as reversion
from reversion.helpers import generate_patch_html

# Create your views here.

ava_obj_lst = Article.objects.order_by('-pub_date')
cat_obj_lst = ava_obj_lst.filter(category__startswith='p').order_by('reporter').values_list('category', flat=True).distinct()
ext_obj_lst = ava_obj_lst.exclude(category__startswith='p').order_by('reporter').values_list('category', flat=True).distinct()

def index(request):
    return render(request, 'wsys/index.html',
                  {'index_lst': Article.objects.all()})

@login_required
def new(request):
    if request.method == 'POST':
        if 'pk' not in request.POST:
            a = Article()
        else:
            a = get_object_or_404(Article, pk=request.POST['pk'])
        form = ArticleForm(request.POST, instance=a)
        if form.is_valid():
            f = form.save(commit=False)
            f.pub_date = dt.datetime.now()
            f.reviser = request.user.username
            if 'pk' not in request.POST:
                f.reporter = request.user.username
            f.save()
            return redirect('wsys:index')
    else:
        form = ArticleForm()
    return render(request, 'wsys/form.html', {'form': form})

def read(request, pk):
    a = get_object_or_404(Article, pk=pk)
    return render(request, 'wsys/read.html',
                  {'fd': get_object_or_404(Article, pk=pk), 'pk': pk})

@login_required
def modi(request, pk):
    a = get_object_or_404(Article, pk=pk)
    form = ArticleForm(instance=a)
    return render(request, 'wsys/form.html', {'form': form, 'pk': pk})

@login_required
def dele(request, pk):
    a = get_object_or_404(Article, pk=pk)
    a.delete()
    return redirect('wsys:index')

def history(request, pk):
    a = get_object_or_404(Article, pk=pk)
    a_ver_lst = reversion.get_for_object(a)
    return render(request, 'wsys/history.html',
                  {'hist_lst': a_ver_lst, 'headline': a.headline, 'pk': pk})

def version(request, vpk, pk):
    a = get_object_or_404(Article, pk=pk)
    a_ver_lst = reversion.get_for_object(a)
    ver = a_ver_lst.get(pk=vpk)
    return render(request, 'wsys/version.html', {'ver': ver.field_dict})

def diff(request, pk):
    a = get_object_or_404(Article, pk=pk)
    a_ver_lst = reversion.get_for_object(a)
    ver_1 = a_ver_lst.get(pk=request.POST['ver_1'])
    ver_2 = a_ver_lst.get(pk=request.POST['ver_2'])
    patch_html = generate_patch_html(ver_1, ver_2, 'content')
    return render(request, 'wsys/diff.html', {'diff': patch_html})
