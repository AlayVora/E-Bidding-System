from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Max
from blog.models import CATEGORY, PRODUCT, TRANSACT, SOLD, UserProfile, BIDFORYOU
from blog.forms import CustomerForm, BidBuy, ProductForm, LoginForm, UpdateForm, passwordForm
from django.contrib.auth import logout
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import authentication, permissions
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.cache import never_cache
import json


def handle_uploaded_file(f, fileName, category_name):
    with open('blog/static/blog/images/' + category_name + '/' + fileName, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def searchproducts(query):
    products_obj = PRODUCT.objects.filter(product_name__icontains=query)
    products = []
    for p in products_obj:
        products.append(p)
        # info_dict = {'products': products, 'error': ''}
    return products



class autobid(APIView):
    renderer_classes = (JSONRenderer, )

    @never_cache
    def get(self, request, format="json"):
        userid=request.user.id
        bidvalue=request.GET['bid_val']
        productid=request.GET['product_id']
        flag=request.GET['flag']
        transact_obj, created = BIDFORYOU.objects.get_or_create(product_id=productid, bidder_id=userid)
        transact_obj.bid_value = bidvalue
        transact_obj.save()
        return Response({'auto_bid_val':transact_obj.bid_value})

    @never_cache
    def post(self, request, format="json"):
        userid=request.user.id
        bidvalue=request.POST['bid_val']
        productid=request.POST['product_id']
        flag=request.POST['flag']
        transact_obj, created = BIDFORYOU.objects.get_or_create(product_id=productid, bidder_id=userid)
        transact_obj.bid_value = bidvalue
        transact_obj.save()
        return Response({'auto_bid_val':transact_obj.bid_value})


def bidforyou():
    # products_obj = PRODUCT.objects.all()
    #transact_obj = TRANSACT.objects.all()

    bidforyou_obj = BIDFORYOU.objects.all()

    for b in bidforyou_obj:
        print b.product_id
        transact_obj,created = TRANSACT.objects.get_or_create(product_id=b.product_id, bidder_id=b.bidder_id)

        bidder_obj = TRANSACT.objects.filter(product_id=b.product_id).aggregate(Max('bid_value'))
        max_bid = bidder_obj['bid_value__max']
        if transact_obj.bid_value < max_bid:
            newbid = max_bid + 1
            #print newbid
            transact_obj.bid_value = newbid
            #print newbid
            if newbid <= b.bid_value:
                userprof = UserProfile.objects.get(user_id=b.bidder_id)
                userprof.bids = transact_obj.bid_value + userprof.bids
                userprof.bids = int(userprof.bids) - int(newbid)
                error = ''
                if userprof.bids >= 0:
                    userprof.save()
                    transact_obj.save()
                error = 'You do not have enough balance'



def index(request):
    return render(request, 'blog/index.html')


def category(request):
    if request.user.is_authenticated():
        cat = CATEGORY.objects.all()
        CHOICES = []
        for c in cat:
            CHOICES.append((c.id, c.category_name))
        context = {'choices': tuple(CHOICES)}
        return render(request, 'blog/category.html', context)
    else:
        return HttpResponseRedirect(reverse('loginform'))


def loginform(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    cat = CATEGORY.objects.all()
                    CHOICES = []
                    for c in cat:
                        CHOICES.append((c.id, c.category_name))
                    products_obj = PRODUCT.objects.filter(category_id_id=1, status=1).exclude(owner=request.user.id)
                    products = []
                    for p in products_obj:
                        products.append(p)
                    info_dict = {'products': products, 'error': '', 'choices': tuple(CHOICES)}
                    return render(request, 'blog/products_in_category.html', info_dict)
                # return HttpResponseRedirect(reverse('products_in_category',kwargs={'category_id':1})
                else:
                    msg = "Dear ", user.get_full_name(), ", your account is not active!"
                    form = LoginForm()
                    return render(request, 'blog/login.html', {'error': 'Invalid Credentials', 'form': form})
            else:
                msg = "hello"
                form = LoginForm()
                return render(request, 'blog/login.html', {'error': 'Invalid Credentials', 'form': form})
        else:
            form = LoginForm()
            return render(request, 'blog/login.html', {'error': 'Invalid Credentials', 'form': form})

    elif request.user and request.user.id is not None:
        # msg = 'hell'
        #profile = UserProfile.objects.filter(user_id=request.user.id)
        if UserProfile.objects.filter(user_id=request.user.id).exists():
            msg = 'helolo'

        else:
            profile1 = UserProfile.objects.create(user_id=request.user.id);
            profile1.save()
        #profile = UserProfile.objects.create(user_id=request.user.id, card_no='76868768', exp_date=0000-00-00, cvv='111')
        #profile.save();
        return HttpResponseRedirect(reverse('account_management'))
    else:
        form = LoginForm()
        context = RequestContext(request, {'request': request, 'user': request.user, 'form': form})
        return render_to_response('blog/login.html', context_instance=context)
        # return render(request, 'blog/login.html', {'form': form})


def changePassword(request):
    if request.method == 'POST':
        form = passwordForm(request.POST)
        if form.is_valid():
            old = form.cleaned_data['oldpassword']
            new = form.cleaned_data['password']
            new1 = form.cleaned_data['password1']
            if request.user.is_authenticated():
                if request.user.is_active:
                    user = User.objects.get(pk=request.user.id)
                    user1 = authenticate(username=user.username, password=old)
                    if user1 is not None:
                        if user.is_active:
                            if new == new1:
                                user.set_password(new)
                                user.save()
                                return HttpResponseRedirect(reverse('account_management'))
                            else:
                                form = passwordForm()
                                return render(request, 'blog/changePassword.html', {'form': form})
                        else:
                            form = passwordForm()
                            return render(request, 'blog/changePassword.html', {'form': form})
                    else:
                        form = passwordForm()
                        return render(request, 'blog/changePassword.html', {'form': form})
                else:
                    return HttpResponseRedirect(reverse('loginform'))
        else:
            form = passwordForm()
            return render(request, 'blog/changePassword.html', {'form': form})
    else:

        form = passwordForm()
        return render(request, 'blog/changePassword.html', {'form': form})


def account_management(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = UpdateForm(request.POST)
            if form.is_valid():

                firstname = form.cleaned_data['firstname']
                lastname = form.cleaned_data['lastname']
                emailid = form.cleaned_data['emailid']
                username = form.cleaned_data['username']
                # password = form.cleaned_data['password']
                card_no = form.cleaned_data['card_no']
                exp_date = form.cleaned_data['exp_date']
                cvv = form.cleaned_data['cvv']
                user = User.objects.get(pk=request.user.id)
                profile = UserProfile.objects.get(user_id=request.user.id)
                user.first_name = firstname
                user.last_name = lastname
                user.email = emailid
                user.username = username
                #user.set_password(password)
                user.save()
                profile.card_no = card_no
                profile.exp_date = exp_date
                profile.cvv = cvv
                profile.save()

                return HttpResponseRedirect(reverse('account_management'))
            else:
                return HttpResponseRedirect(reverse('account_management'))
        else:


            user = User.objects.get(pk=request.user.id)
            profile = UserProfile.objects.get(user_id=request.user.id)

            form = UpdateForm(initial={'firstname': user.first_name, 'lastname': user.last_name, 'emailid': user.email,
                                       'username': user.username, 'card_no': profile.card_no,
                                       'exp_date': profile.exp_date, 'cvv': profile.cvv})

            return render(request, 'blog/account.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('loginform'))


def home(request):
    if request.user and request.user.id is not None:
        msg = 'hell'
        # profile = UserProfile.objects.filter(user_id=request.user.id)
        if UserProfile.objects.filter(user_id=request.user.id).exists():
            msg = 'helolo'

        else:
            profile1 = UserProfile.objects.create(user_id=request.user.id);
            profile1.save()
        #profile = UserProfile.objects.create(user_id=request.user.id, card_no='76868768', exp_date=0000-00-00, cvv='111')
        #profile.save();
        return HttpResponseRedirect(reverse('account_management'))
    context = RequestContext(request, {'request': request, 'user': request.user})
    return render_to_response('blog/home.html', context_instance=context)


def process_register(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            emailid = form.cleaned_data['emailid']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            card_no = form.cleaned_data['card_no']
            exp_date = form.cleaned_data['exp_date']
            cvv = form.cleaned_data['cvv']
            new_user = User.objects.create_user(username, emailid, password)
            new_user.first_name = firstname
            new_user.last_name = lastname
            new_user.save()
            profile = UserProfile.objects.create(user=new_user, card_no=card_no, exp_date=exp_date, cvv=cvv)
            return HttpResponseRedirect(reverse('buy_bids'))
    else:
        form = CustomerForm()
    return render(request, 'blog/register.html', {'form': form})


def addproduct(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                productname = form.cleaned_data['productname']
                product_desc = form.cleaned_data['product_desc']
                price = form.cleaned_data['price']
                expdatetime = form.cleaned_data['expdatetimehidden']
                expdatetime= expdatetime.replace("/" , "-")
                category_id = form.cleaned_data['category']
                file1 = request.FILES['fileName']
                fileName = request.FILES['fileName'].name
                category_obj = CATEGORY.objects.get(pk=category_id)
                handle_uploaded_file(file1, fileName, category_obj.category_name)
                product_path = 'blog/images/' + category_obj.category_name + '/' + fileName
                product_obj = PRODUCT(product_name=productname, product_desc=product_desc, price=price,
                                      product_path=product_path, category_id=category_obj, owner=request.user.id,
                                      status=1,expdatetime=expdatetime)
                product_obj.save()
                CHOICES = []
                cat = CATEGORY.objects.all()
                CHOICES = []
                for c in cat:
                    CHOICES.append((c.id, c.category_name))
                products_obj = PRODUCT.objects.filter(category_id_id=category_id, status=1).exclude(
                    owner=request.user.id)
                products = []
                for p in products_obj:
                    products.append(p)
                info_dict = {'products': products, 'error': '', 'choices': tuple(CHOICES)}
                return render(request, 'blog/products_in_category.html', info_dict)
            # return HttpResponseRedirect(reverse('category'))
            else:
                form = ProductForm()
                info_dict = {'form': form, 'error': 'Please provide valid inputs.'}
                return render(request, 'blog/addproduct.html', info_dict)
        else:
            form = ProductForm()
            info_dict = {'form': form, 'error': ''}
            return render(request, 'blog/addproduct.html', info_dict)
    else:
        return HttpResponseRedirect(reverse('loginform'))


def mybidproducts(request):
    if request.user.is_authenticated():
        cat = CATEGORY.objects.all()
        CHOICES = []
        for c in cat:
            CHOICES.append((c.id, c.category_name))
        userid = request.user.id
        products_obj = PRODUCT.objects.exclude(owner=userid)
        # products_obj = products_obj.exclude(owner=userid)
        products = []
        for p in products_obj:
            trans_obj = TRANSACT.objects.filter(bidder_id=userid, product_id=p.id).count()
            if trans_obj > 0:
                products.append(p)

        info_dict = {'products': products, 'error': '', 'choices': tuple(CHOICES)}
        return render(request, 'blog/mybidproducts.html', info_dict)
    else:
        return HttpResponseRedirect(reverse('loginform'))


def orderhistory(request):
    if request.user.is_authenticated():
        # bidforyou()
        #autobid()
        pid_obj = PRODUCT.objects.filter(status=0)
        sid_obj = SOLD.objects.filter(new_owner=request.user.id)
        orders = []
        products = []
        for p in pid_obj:
            for s in sid_obj:
                if p.id == s.product_id:
                    products.append(p)
                    orders.append(s)
        info_dict = {'products': products, 'error': '', 'orders': orders}
        return render(request, 'blog/orderhistory.html', info_dict)
    else:
        return HttpResponseRedirect(reverse('loginform'))


def viewproduct(request, category_id):
    if request.user.is_authenticated():
        cat = CATEGORY.objects.all()
        CHOICES = []
        for c in cat:
            CHOICES.append((c.id, c.category_name))
        products = PRODUCT.objects.filter(id=category_id)
        info_dict = {'products': products, 'error': '', 'choices': tuple(CHOICES)}
        return render(request, 'blog/viewproduct.html', info_dict)
    else:
        return HttpResponseRedirect(reverse('loginform'))


def products_in_category(request, category_id):
    if request.user.is_authenticated():
        cat = CATEGORY.objects.all()
        CHOICES = []
        for c in cat:
            CHOICES.append((c.id, c.category_name))
        userid = request.user.id
        products_obj = PRODUCT.objects.filter(category_id_id=category_id, status=1).exclude(owner=userid)
        # products_obj = products_obj.exclude(owner=userid)
        products = []
        for p in products_obj:
            trans_obj = TRANSACT.objects.filter(id=p.id, bidder_id=userid).count()
            #if trans_obj>0:
            products.append(p)

        info_dict = {'products': products, 'error': '', 'choices': tuple(CHOICES)}
        return render(request, 'blog/products_in_category.html', info_dict)
    else:
        return HttpResponseRedirect(reverse('loginform'))


def sold(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            product_id = request.POST['product_id']
            products_obj = PRODUCT.objects.get(pk=product_id)
            bidder_obj = TRANSACT.objects.filter(product=products_obj).aggregate(Max('bid_value'))
            max_bid = bidder_obj['bid_value__max']
            if max_bid is None:
                new_exp_date = datetime.now() + timedelta(minutes=60)
                products_obj.expdatetime = str(new_exp_date)
                products_obj.save();
                response_data = {'new_expdatetime': str(new_exp_date)}
            else:
                bidder_obj = TRANSACT.objects.filter(product=products_obj, bid_value=max_bid)[0]
                sold_obj = SOLD.objects.create(product_id=products_obj.id, bid_value=max_bid,
                                               old_owner=products_obj.owner, new_owner=bidder_obj.bidder_id)
                products_obj.status = 0
                products_obj.save()
                TRANSACT.objects.filter(product=products_obj).delete()
                bidder_cust_obj = User.objects.get(pk=bidder_obj.bidder_id)
                response_data = {"sold": "Product is sold to " + bidder_cust_obj.username}
            return HttpResponse(json.dumps(response_data), content_type="application/json")


def processbids(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            customer_id = request.user.id
            product_id = request.POST['product_id']
            bid_val = request.POST['bid_val']

            products_obj = PRODUCT.objects.get(pk=product_id)
            userprof = UserProfile.objects.get(user_id=customer_id)
            transact_obj, created = TRANSACT.objects.get_or_create(product=products_obj, bidder_id=customer_id)
            userprof.bids = transact_obj.bid_value + userprof.bids
            transact_obj.bid_value = bid_val
            userprof.bids = int(userprof.bids) - int(bid_val)
            error = ''
            if userprof.bids >= 0:
                userprof.save()
                transact_obj.save()
                error = 'You do not have enough balance'
            bidder_obj = TRANSACT.objects.filter(product_id=product_id).aggregate(Max('bid_value'))
            max_bid = bidder_obj['bid_value__max']
            bidder_obj = TRANSACT.objects.filter(product=products_obj, bid_value=max_bid)[0]
            bidder_cust_obj = User.objects.get(pk=bidder_obj.bidder_id)
            response_data = {'username': bidder_cust_obj.username, 'bid_val': max_bid, 'error': error}

            return HttpResponse(json.dumps(response_data), content_type="application/json")


"""
def getmaxbidder(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			product_id = request.POST['product_id']
			products_obj = PRODUCT.objects.get(pk=product_id)
			bidder_obj = TRANSACT.objects.filter(product=products_obj).aggregate(Max('bid_value'))
			max_bid = bidder_obj['bid_value__max']
			if max_bid is None:
				response_data = {'username': '', 'bid_val': 0}
			else:
				bidder_obj = TRANSACT.objects.filter(product=products_obj, bid_value=max_bid)[0]
				bidder_cust_obj = User.objects.get(pk=bidder_obj.bidder_id)
				response_data = {'username': bidder_cust_obj.username, 'bid_val': max_bid}
			return HttpResponse(json.dumps(response_data), content_type="application/json")
"""


class search(APIView):
    renderer_classes = (JSONRenderer, )

    @never_cache
    def get(self, request, format="json"):
        if request.user.is_authenticated():
            query_string = request.GET['search_string']
            products = searchproducts(query_string)
            response_data = {}
            for p in products:
                response_data[p.id] = p.product_name
                # print response_data[p.id]
            return Response(response_data)
        else:
            response_data = {'403': 'Accesss Forbidden!'}
            return Response(response_data)

    @never_cache
    def post(self, request, format="json"):
        if request.user.is_authenticated():
            query_string = request.POST['search_string']
            products = searchproducts(query_string)
            response_data = {}
            for p in products:
                response_data[p.id] = p.product_name
                # print response_data[p.id]
            return Response(response_data)
        else:
            response_data = {'403': 'Accesss Forbidden!'}
            return Response(response_data)


class getmaxbidder(APIView):
    renderer_classes = (JSONRenderer, )

    @never_cache
    def get(self, request, format="json"):
        bidforyou()
        product_id = request.GET['product_id']
        products_obj = PRODUCT.objects.get(pk=product_id)
        bidder_obj = TRANSACT.objects.filter(product=products_obj).aggregate(Max('bid_value'))
        max_bid = bidder_obj['bid_value__max']
        if max_bid is None:
            response_data = {'username': '', 'bid_val': 0}
        else:
            bidder_obj = TRANSACT.objects.filter(product=products_obj, bid_value=max_bid)[0]
            bidder_cust_obj = User.objects.get(pk=bidder_obj.bidder_id)
            response_data = {'username': bidder_cust_obj.username, 'bid_val': max_bid}
        return Response(response_data)


    @never_cache
    def post(self, request, format="json"):
        bidforyou()
        product_id = request.POST['product_id']
        products_obj = PRODUCT.objects.get(pk=product_id)
        bidder_obj = TRANSACT.objects.filter(product=products_obj).aggregate(Max('bid_value'))
        max_bid = bidder_obj['bid_value__max']
        if max_bid is None:
            response_data = {'username': '', 'bid_val': 0}
        else:
            bidder_obj = TRANSACT.objects.filter(product=products_obj, bid_value=max_bid)[0]
            bidder_cust_obj = User.objects.get(pk=bidder_obj.bidder_id)
            response_data = {'username': bidder_cust_obj.username, 'bid_val': max_bid}
        return Response(response_data)


def logoutview(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse('loginform'))


class CurrrentDateTime(APIView):
    renderer_classes = (JSONRenderer, )

    @never_cache
    def get(self, request, format="json"):
        return Response(dict(CurrentDateTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


def buy_bids(request):
    if request.user.is_authenticated():
        return render(request, 'blog/buybid.html')
    else:
        return HttpResponseRedirect(reverse('loginform'))


class buybidservice(APIView):
    renderer_classes = (JSONRenderer, )

    @never_cache
    def get(self, request, format="json"):
        if request.user.is_authenticated():
            no_of_bids = request.GET['no_of_bids']
            profile = UserProfile.objects.get(user=request.user)
            profile.bids = int(profile.bids) + int(no_of_bids)
            profile.save()
            response_data = {'available_bids': profile.bids}
            return Response(response_data)
        else:
            response_data = {'403': 'Accesss Forbidden!'}
            return Response(response_data)



    @never_cache
    def post(self, request, format="json"):
        if request.user.is_authenticated():
            no_of_bids = request.POST['no_of_bids']
            profile = UserProfile.objects.get(user=request.user)
            profile.bids = int(profile.bids) + int(no_of_bids)
            profile.save()
            response_data = {'available_bids': profile.bids}
            return Response(response_data)
        else:
            response_data = {'403': 'Accesss Forbidden!'}
            return Response(response_data)


"""def processbids(request):
		if request.method == 'POST':
			form = ProductForm(request.POST)
			if form.is_valid():
				customer_id=form.cleaned_data['customer_id']
				product_id=form.cleaned_data['product_id']
				bid_val=form.cleaned_data['bid_val']
				cust_obj=CUSTOMER.objects.get(pk=customer_id)
				products_obj=PRODUCT.objects.get(pk=product_id)
				transact_obj, created=TRANSACT.objects.get_or_create(product=products_obj,bidder_id=customer_id)
				transact_obj.bid_value=bid_val
				transact_obj.save()
				bidder_obj=TRANSACT.objects.filter(product=products_obj).aggregate(Max('bid_value'))
				max_bid=bidder_obj.bid_value__max
				bidder_obj=TRANSACT.objects.filter(product=products_obj,bid_value=max_bid)[0]
				bidder_cust_obj=CUSTOMER.objects.get(pk=bidder_obj.bidder_id)
				response_data={'username':bidder_cust_obj.username,'bid_val':max_bid}
		return HttpResponse(response_data,content_type="application/json")
	"""








