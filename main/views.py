from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect
from django.views import generic
from django.shortcuts import render, redirect
from .models import  *
from django.views.generic.edit import FormView
from .form import *
import requests
import json
from datetime import datetime
import random

name = "main"


def starter_pack(request):
    context = {}
    context['form'] = StartPackForm()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StartPackForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            qty =int(form.data['quantity'])
            for x in range(qty):
                LL,LW,LT = 0,0,0
                ran_number = random.randint(1,100)
                if ran_number < 50:
                    rooster_class = 1
                elif ran_number > 50 and ran_number < 80 :
                    rooster_class = 2
                elif ran_number > 80 and ran_number < 95 :
                    rooster_class = 3
                elif ran_number > 95 and ran_number < 100 :
                    rooster_class = 4

                ran_number = random.randint(1, 100)
                if ran_number < 60:
                    LL = 1
                ran_number = random.randint(1, 100)
                if ran_number < 60:
                    LW = 1
                ran_number = random.randint(1, 100)
                if ran_number < 60:
                    LT = 1

                Rooster.objects.create(info = f"{rooster_class}{LL}{LW}{LT}")
            return HttpResponseRedirect('/rooster')
        # if a GET (or any other method) we'll create a blank form

    return render(request, 'main/test.html',context)



def market_place(request):
    context = {
        'discount': "test",
        'company': "company"
    }
    return render(request, 'main/talpak.html', context)

def cockpit(request):
    context = {
        'discount': "test",
        'company': "company"
    }
    return render(request, 'main/talpak.html', context)

def my_rooster(request):

    rooster = Rooster.objects.all()

    context = {
        'rooster': rooster,
        'company': "company"
    }
    return render(request, 'main/rooster_V2.html', context)


def breeding(request):
    context = {
        'discount': "test",
        'company': "company"
    }
    return render(request, 'main/talpak.html', context)

class ScholarView(generic.CreateView):
    model = Scholar
    template_name = 'main/scholar.html'
    success_url = reverse_lazy('home')
    form_class = ScheduleForm

    def form_valid(self, form):
        install_obj = form.save(commit=False)
        install_obj.user = self.request.user
        install_obj.ronin_address = str(form.cleaned_data['ronin_address']).replace("ronin:","")
        response = requests.get(url=f"https://api.lunaciarover.com/stats/0x{scholar.ronin_address}")
        json_response = response.json()
        install_obj.updated_on = datetime.utcfromtimestamp(int(json_response['updated_on'])).strftime(
            '%Y-%m-%d %H:%M:%S')
        install_obj.last_claim_amount = json_response['last_claim_amount']
        install_obj.last_claim_timestamp = datetime.utcfromtimestamp(
            int(json_response['last_claim_timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
        install_obj.ronin_slp = json_response['ronin_slp']
        install_obj.total_slp = json_response['total_slp']
        install_obj.in_game_slp = json_response['in_game_slp']
        install_obj.slp_success = json_response['slp_success']
        install_obj.mmr = json_response['mmr']
        install_obj.total_matches = json_response['total_matches']
        install_obj.ign = json_response['ign']
        install_obj.total_matches = json_response['total_matches']
        install_obj.game_stats_success = json_response['game_stats_success']
        install_obj.last_update = datetime.now().date()
        print(response.text)

        install_obj.save()

        return super(ScholarView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(ScholarView, self).get_context_data(**kwargs)
        scholar_obj = Scholar.objects.filter(user=self.request.user)
        for scholar in scholar_obj:
            past = datetime.strptime(scholar.last_update.strftime('%Y-%m-%d'), '%Y-%m-%d')
            if  past.date() <= datetime.now().date():
                response = requests.get(url=f"https://api.lunaciarover.com/stats/0x{scholar.ronin_address}")
                if response.status_code == 200:
                    print("response.status_coderesponse.status_coderesponse.status_coderesponse.status_code")
                    print(response.text)
                    json_response = response.json()
                    scholar.updated_on = datetime.utcfromtimestamp(int(json_response['updated_on'])).strftime('%Y-%m-%d %H:%M:%S')
                    scholar.last_claim_amount = float(json_response['last_claim_amount'])
                    scholar.last_claim_timestamp =  datetime.utcfromtimestamp(int(json_response['last_claim_timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
                    scholar.ronin_slp =float(json_response['ronin_slp'])
                    scholar.total_slp = float(json_response['total_slp'])
                    scholar.in_game_slp = float(json_response['in_game_slp'])
                    scholar.slp_success = bool(json_response['slp_success'])
                    # scholar.mmr = float(json_response['mmr'])
                    scholar.total_matches = int(json_response['total_matches'])
                    scholar.ign = str(json_response['ign'])
                    scholar.game_stats_success = bool(json_response['game_stats_success'])
                    scholar.last_update = datetime.now().strftime('%Y-%m-%d')
                    scholar.save()
            else:
                print("FALSE")

        context['scholar_obj'] = scholar_obj
        return context


class PayoutView(FormView):
    template_name = 'main/payout.html'
    success_url 	= '../../scholar'
    form_class = PayoutForm

    def get_initial(self):
        initial = super().get_initial()
        scholar_obj = Scholar.objects.get(pk=self.kwargs['pk'])
        rate = scholar_obj.get_rate()
        initial['scholar'] = scholar_obj.id
        initial['ronin_address'] = scholar_obj.ronin_address
        initial['last_update'] = datetime.now().today()
        initial['manager_fee'] = scholar_obj.get_manager_fee()[0] * rate
        initial['scholar_fee'] = scholar_obj.get_scholar_fee()[0]* rate
        initial['manager_slp'] = scholar_obj.get_manager_fee()[1]
        initial['scholar_slp'] =scholar_obj.get_scholar_fee()[1]
        initial['gas_fee'] =  0
        initial['rate'] = 50

        return initial

    def form_valid(self, form):
        print("valid")
        Invoice.objects.create(
            scholar_id=form.cleaned_data['scholar'],
            ronin_address=form.cleaned_data['ronin_address'],
            last_update =form.cleaned_data['last_update'],
            manager_fee= form.cleaned_data['manager_fee'],
            scholar_fee= form.cleaned_data['scholar_fee'],
            manager_slp=form.cleaned_data['manager_slp'],
            scholar_slp=form.cleaned_data['scholar_slp'],
            gas_fee=form.cleaned_data['gas_fee'],
            rate=form.cleaned_data['rate'])

        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(PayoutView, self).get_context_data(*args, **kwargs)
        context['title'] = "Product Price Update"
        context['crypto_obj'] = Crypto.objects.get(symbol="SLPUSDT")


        return context


