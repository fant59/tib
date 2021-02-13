from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import Stock
from .models import Portfolio, PortfolioStock, DirectionChoices, \
    PortfolioStockLine


class PortfolioForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label=_('Название'),
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
        }),
    )
    description = forms.CharField(
        required=True,
        label=_('Описание'),
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-sm',
        }),
    )

    class Meta:
        model = Portfolio
        fields = [
            'name',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.user = self.user
        return super().save(commit)


class PortfolioStockForm(forms.ModelForm):
    stock = forms.ModelChoiceField(
        required=True,
        queryset=Stock.objects,
        label=_('Акция'),
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm',
            'data-type': 'ajax-select',
        }),
    )
    direction = forms.ChoiceField(
        required=True,
        choices=DirectionChoices.choices,
        label=_('Направление'),
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm',
        }),
    )
    fee = forms.FloatField(
        required=False,
        initial=0.00,
        label=_('Комиссия брокера'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'step': '0.01',
        }),
        help_text=_('Укажите комиссию. Это очень важно для точных рассчетов.')
    )
    portfolio = forms.ModelChoiceField(
        queryset=Portfolio.objects,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = PortfolioStock
        fields = [
            'stock',
            'direction',
            'fee',
            'portfolio',
        ]


class PortfolioStockLineForm(forms.ModelForm):
    portfolio_stock = forms.ModelChoiceField(
        queryset=PortfolioStock.objects,
        widget=forms.HiddenInput()
    )
    date = forms.DateField(
        required=True,
        initial=lambda: timezone.now(),
        label=_('Дата покупки'),
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-sm',
        }),
    )
    price = forms.FloatField(
        required=True,
        label=_('Цена'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'step': '0.01',
        }),
    )
    quantity = forms.IntegerField(
        required=True,
        label=_('Количество'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
        }),
    )

    class Meta:
        model = PortfolioStockLine
        fields = [
            'portfolio_stock',
            'date',
            'price',
            'quantity',
        ]
