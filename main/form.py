from django import forms
from .models import *
from . import models
from django.contrib.admin import widgets
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory

class ScheduleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['ronin_address'].widget.attrs = {'class': 'form-control', 'placeholder':'ronin:4c9fbbd2b0419a469c0dbf620615a5805f8c9dc6',}
        self.fields['name'].widget.attrs = {'class': 'form-control', 'placeholder':'Cr John',}
        self.fields['scholar_share'].widget.attrs = {'class': 'form-control', 'placeholder':'Percentage %',}
        pass

    class Meta:
        model = Scholar
        fields = ('ronin_address', 'name', 'scholar_share')

class PayoutForm(forms.Form):
    scholar = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), required=False)
    ronin_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control ', }), required=False)
    last_update =  forms.DateField()
    manager_fee = forms.FloatField(widget=forms.TextInput(attrs={'class': 'mb-2 form-control', }), required=False)
    scholar_fee = forms.FloatField(widget=forms.TextInput(attrs={'class': 'mb-2 form-control ', }), required=False)
    manager_slp = forms.FloatField(widget=forms.TextInput(attrs={'class': 'mb-2 form-control ', }), required=False)
    scholar_slp = forms.FloatField(widget=forms.TextInput(attrs={'class': 'mb-2 form-control ', }), required=False)
    gas_fee = forms.FloatField(widget=forms.TextInput(attrs={'class': 'mb-2 form-control ', }), required=False)
    rate = forms.FloatField(widget=forms.TextInput(attrs={'class': 'mb-2 form-control ',}), required=False)


    def __init__(self, *args, **kwargs):
        super(PayoutForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['rate'].widget.attrs['readonly'] = True

    def clean_rate(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.rate
        else:
            return self.cleaned_data['rate']


    # ronin_address = models.CharField(max_length=200)
    # updated_on = models.DateTimeField(null=True,blank=True)
    # last_claim_amount = models.FloatField(default=0)
    # last_claim_timestamp = models.DateTimeField(default=timezone.now)
    # ronin_slp = models.IntegerField(default=0)
    # slp_success = models.BooleanField(blank=True, null=True)
    # mmr = models.DateTimeField(blank=True, null=True)
    # total_matches = models.IntegerField(default=0)
    # ign = models.CharField(max_length=200)
    # game_stats_success = models.BooleanField(blank=True, null=True)


class StartPackForm(forms.Form):
    quantity = forms.IntegerField()