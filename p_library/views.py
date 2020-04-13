from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from p_library.models import Book, Publisher


def index(request):
    template = loader.get_template("index.html")
    books = Book.objects.all()
    biblio_data = {
        "title": "мою библиотеку", 
        "books": books,
        }
    return HttpResponse(template.render(biblio_data, request))

def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)

def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')

def publisher(request):
    template = loader.get_template('publisher.html')
    publishers = Publisher.objects.all().order_by('name')

    pubinfo = []
    for publisher in publishers:
        publisher_books = Book.objects.filter(publisher=publisher)
        book_info = []
        for book in publisher_books:
            book_info.append(book.title + ' ('+book.author.full_name+')')

        publisher_info = {}
        publisher_info[publisher.name] = book_info
        pubinfo.append(publisher_info)

    biblio_data = {
        "pubinfo": pubinfo,
    }
    return HttpResponse(template.render(biblio_data, request))