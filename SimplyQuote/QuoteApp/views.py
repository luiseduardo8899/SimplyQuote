import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import loader
from django.http import Http404
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from random import *
from .forms import QuoteForm, CustomUserCreationForm, form_Account
import json
from django.http import JsonResponse
from QuoteApp.models import SalesPerson
from QuoteApp.models import Account
from QuoteApp.models import Product
from QuoteApp.models import Quote
from django.conf import settings
from django.core.files.storage import default_storage
import re
import xlwt
import glob
import hashlib
import sys

BUF_SIZE = 65536  #64*1024 = 64kb : Buffer Size large enough to contain images


#START TAXABLE_IDS
CREATED     = 0         #On creation it is saved to /media 
REGISTERED  = 1         #Once it is sent as an email
ACCEPTED    = 2         #Once other party accepts
REJECTED    = 3         #If other party rejects
INVALIDATED = 4         #If both sides agree to invalidate document
LICENSE_LAUNCHED = 5    #If both sides agree to invalidate document


def generate_quote_file(quote):
    filename = quote.quote_name
    book = xlwt.Workbook()
    sh = book.add_sheet(filename)

    #size the columns
    charwidth = 256
    numchar = [6,6,15,70, 20,15,15] #number of characters per column
    for ix in range(7):
        col =  sh.col(ix)
        col.width = charwidth * numchar[ix]

    style_title = xlwt.easyxf('font: bold on, color black, height 200;')
    sh.write(2, 3, "THE COMPANY. INC", style_title)
    sh.write(3, 3, "Austin, TX")
    sh.write(8,0, "To:")
    sh.write(9,0, "Attn:")
    accounts = quote.account.all()
    sh.write(8,1, accounts[0].company_name)
    sh.write(9,1, accounts[0].main_contact)
    sh.write(9,2, accounts[0].email)

    style = xlwt.easyxf('font: bold off, color black; borders: left thin, right thin, top thin, bottom thin; align: horiz center')
    titles = ['SALES PERSON', 'QUOTE EXPIRATION DATE', 'TAXABLE', 'TERMS']
    ix =2
    for title in titles:
        sh.write(13, ix, title, style )
        ix= ix +1

    ix =2
    row = 14
    date_time = datetime.date.today() + datetime.timedelta(quote.validity)
    expiration = date_time.strftime("%m/%d/%Y")
    sales_persons = quote.sales_person.all()
    sales_person_name = sales_persons[0].name+" "+sales_persons[0].last_name
    titles = [sales_person_name, expiration, quote.taxable, quote.term]
    for title in titles:
        sh.write(row, ix, title, style)
        ix= ix +1

    row = 16
    ix =0
    titles = ['ITEM', 'QTY', 'PRODUCT', 'DESCRIPTION', 'LIST PRICE ( per License)', 'DISCOUNT', 'NET PRICE']
    for title in titles:
        sh.write(row, ix, title,  style)
        ix= ix +1

    row = 17
    total_quote = 0
    item = 1
    products = quote.product.all()
    for p in products:
        net_price = ( p.list_price * quote.quantity * quote.discount ) / 100
        total_quote += net_price
        titles = [item, quote.quantity, p.product_code, p.description, p.list_price, quote.discount, net_price ]
        item = item +1
        ix =0
        for title in titles:
            sh.write(row, ix, title, style)
            ix += 1
        row += 1

    titles = ["TOTAL", "", total_quote]
    ix = 4
    for title in titles:
        sh.write(row, ix, title,  style)
        ix= ix +1

    book.save(filename+".xls")
    myfile =  open(filename+".xls", "rb")

    return myfile, filename


def generate_quote(request):
    #user = get_user(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QuoteForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            try: 
                last_quote = Quote.objects.latest('create_date');
                last_id = last_quote.quote_id
            except Quote.DoesNotExist:
                last_id = 0
            q = Quote()
            q.quote_id = last_id + 1
            q.create_date = datetime.datetime.now()
            # process the data in form.cleaned_data as required
            q.state = CREATED
            q.quote_name = form.cleaned_data['quote_name']
            account= form.cleaned_data['account']
            q.quantity = form.cleaned_data['amount']
            #q.taxable = form.cleaned_data['taxable']
            q.taxable = 0
            q.discount = form.cleaned_data['discount']
            #q.term = form.cleaned_data['term']
            q.term = 1
            #q.validity = form.cleaned_data['validity']
            q.validity = 30;
            q.save()
            #Then add manytomany fields
            q.sales_person.add(form.cleaned_data['sales_person'])
            q.product.add(form.cleaned_data['product'])
            q.account.add(form.cleaned_data['account'])
            q.save()

            #generate xls version of the quote / save to media and provide URL
            myfile, filename = generate_quote_file(q)
            file_name = default_storage.save(filename+".xls", myfile)

            #TODO:LUIS: starting_hash = settings.COMPANY_PRIVATE_KEY #Use password authenticatio or 2 factor authentication to retrieve private key
            #TODO:LUIS: Bstarting_hash= str.encode(starting_hash)
            #TODO:LUIS: md5_hash, sha256hash = create_hash(filename+".xls", Bstarting_hash)
            #TODO:LUIS: q.sha256hash = sha256hash
            q.save()

            #TODO:LUIS: B256hash = str.encode(sha256hash)
            #TODO:LUIS: ok = check_hash(filename+".xls", Bstarting_hash, B256hash)

	    #TODO: Send email, save email hash or id to quote and
            # q.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/quotes/view_quote/'+str(q.quote_id)+'/')
        else:
            print("FORM ERRORS:\n\t")
            print(form.errors)


    # if a GET (or any other method) we'll create a blank form
    else:
        form = QuoteForm()

    sales_persons = SalesPerson.objects.all()
    accounts = Account.objects.all()
    products = Product.objects.all()
    return render(request, 'generate_quote.html', {'form': form, 'sales_persons':sales_persons, 'accounts':accounts, 'products':products})

# View details for a specififc function
# Returns kana details
def view_quote(request, id):
    quote  = Quote.objects.get(quote_id=id)
    sales_persons = quote.sales_person.all()
    sales_person_name = sales_persons[0].name+" "+sales_persons[0].last_name
    accounts = quote.account.all()
    account_name = accounts[0].company_name
    products = quote.product.all()
    total = products[0].list_price * quote.discount * quote.quantity #le quite un * que tenia al inicio
    return render(request, "view_quote.html", {'quote':quote, 'sales_person_name':sales_person_name, 'account_name':account_name, 'product':products[0], 'total':total })

def view_all_quotes(request):
    quotes  = Quote.objects.all()
    return render(request, "view_all_quotes.html", {'quotes':quotes })

#Added by Marlon
def registro(request):
    data = { 'form': CustomUserCreationForm()}

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data = request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect(to="login")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

  

class wiew_form_Account(HttpRequest):

    def index(request):
        account = form_Account()
        return render(request, "add_account.html", {"form":account})

    def process_form(request):
        account = form_Account(request.POST)
        # check whether it's valid:
        if account.is_valid():
            try: 
                last_account = Account.objects.latest('create_date');
                last_id = last_account.account_id
            except Account.DoesNotExist:
                last_id = 0
            q = Account()
            q.account_id = last_id + 1
            q.create_date = datetime.datetime.now()
            q.company_name = account.cleaned_data['company_name']
            q.main_contact = account.cleaned_data['main_contact']
            q.email = account.cleaned_data['email']
            
            q.save()
            account = form_Account()
        else:
            print("FORM ERRORS:\n\t")
            print(account.errors)
        
        return render(request, "add_account.html", {"form":account, "message":'Ok'})













