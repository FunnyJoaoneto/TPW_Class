from django.shortcuts import render
from datetime import datetime
from app.models import *

# Create your views here.

def home(request):
    tparams = {
        'title': 'Home Page',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def authorins(request):
    if not request.user.is_authenticated or request.user.username != 'joaoneto':
        return redirect('login')
    if request.method == 'POST':
        form = AuthorinsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            a = Author(name=name, email=email)
            a.save()
            return HttpResponse("<h1>Author Inserted!!!</h1>")
    else:
        form = AuthorinsForm()
    return render(request, 'authorins.html', {'form': form})


def contact(request):
    tparams = {
        'title': 'Contact',
        'message': 'Your contact page.',
        'year': datetime.now().year,
    }
    return render(request, 'contact.html', tparams)


def about(request):
    tparams = {
        'title': 'About',
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'about.html', tparams)

def books(request):
    tparams = {
        'title': 'Books',
        'message': 'Your books page.',
        'year': datetime.now().year,
        'total_books': Book.objects.all().count(),
        'boks': Book.objects.all(),
    }
    return render(request, 'books.html', tparams)

def authors(request):
    tparams = {
        'title': 'Authors',
        'message': 'Your authors page.',
        'year': datetime.now().year,
        'total_authors': Author.objects.all().count(),
        'authors': Author.objects.all(),
    }
    return render(request, 'authors.html', tparams)

def book_detail(request, id):
    book = Book.objects.get(id=id)
    tparams = {
        'title': book.title,
        'date': book.date,
        'authors': book.authors.all(),
        'publisher': book.publisher,
    }
    return render(request, 'book_detail.html', tparams)

def booksearch(request):
    if 'query' in request.POST:
        query = request.POST['query']
        if query:
            books = Book.objects.filter(title__icontains=query)
            return render(request, 'books.html',{'boks':books, 'query':query})
        else:
            return render(request, 'booksearch.html',{'error':True})
    else:
        return render(request, 'booksearch.html',{'error':False})

def authorssearch(request):
    if 'query' in request.POST:
        query = request.POST['query']
        if query:
            auts = Author.objects.filter(name__icontains=query)
            return render(request, 'authors.html',{'auts':auts, 'query':query})
        else:
            return render(request, 'authorssearch.html',{'error':True})
    else:
        return render(request, 'authorssearch.html',{'error':False})

def autpubsearch(request):
    if 'autquery' and 'pubquery' in request.POST:
        aut = request.POST['autquery']
        pub =request.POST['pubquery']
        if aut and pub:
            print("aut and pub")
            bookauts = Book.objects.filter(authors__name__icontains=aut)
            bookpubs = Book.objects.filter(publisher__name__icontains=pub)
            bookauts = bookauts & bookpubs

            return render(request, 'authorspa.html',{'boks':bookauts, 'autq':aut, 'pubq':pub})
        elif aut and not pub:
            print("aut")
            bookauts = Book.objects.filter(authors__name__icontains=aut)
            return render(request, 'authorspa.html',{'boks':bookauts, 'autq':aut})
        elif pub and not aut:
            print("pub")
            bookpubs = Book.objects.filter(publisher__name__icontains=pub)
            return render(request, 'authorspa.html',{'boks':bookpubs, 'pubq':pub})
        else:
            print("womp womp")
            return render(request, 'autpubsearch.html',{'error':True})
    else:
        print("womp womp master")
        return render(request, 'autpubsearch.html',{'error':False})
