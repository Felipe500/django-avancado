from django import forms
from .models import ItemsVenda

class ItemPedidoForm(forms.Form):
    produto_id = forms.CharField(label='ID do Produto', max_length=100)
    quantidade = forms.IntegerField(label='Quantidade')
    desconto = forms.DecimalField(label='Desconto', max_digits=7, decimal_places=2)


class ItemPedidoFormModelForm(forms.ModelForm):
    class Meta:
        model = ItemsVenda
        fields = ['quantidade','desconto']

