import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from .models import Venda, ItemsVenda,  VendaStatus
from django.db.models import  Sum, F, FloatField,Min, Max, Avg
from .forms import ItemPedidoForm,ItemPedidoFormModelForm
import logging


my_log = logging.getLogger('django')


class DashboardView(LoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('vendas.ver_dashboard'):
            return HttpResponse('Acesso negado, voce precisa de permissao!')

        return super(DashboardView, self).dispatch(request, *args, **kwargs)
    def get(self, request):
        data = {}
        data['media'] = Venda.objects.media()
        data['media_desc'] = Venda.objects.media_desconto()
        data['min'] = Venda.objects.min()
        data['max'] = Venda.objects.max()
        data['n_ped'] = Venda.objects.num_pedidos()
        data['n_ped_nfe'] = Venda.objects.num_ped_nefe()

        return render( request,'vendas/dashboard.html', data)

class NovoPedido(View):
    def get(self, request):
        return render(request, 'vendas/novo-pedido.html')

    def post(self, request):
        data = {}
        data['form_item'] = ItemPedidoForm()
        data['numero'] = request.POST['numero']
        data['desconto'] = float(request.POST['desconto'].replace(',', '.'))
        data['venda_id'] = request.POST['venda_id']

        if data['venda_id']:
            venda = Venda.objects.get(id=data['venda_id'])
            venda.desconto = data['desconto']
            venda.numero = data['numero']
            venda.save()

        else:
            venda = Venda.objects.create(
                numero=data['numero'], desconto=data['desconto'])

        itens = venda.itemsvenda_set.all()
        data['venda'] = venda
        data['itens'] = itens
        return render(
            request, 'vendas/novo-pedido.html', data)

class NovoItemPedido(View):
    def get(self, request, pk):
        pass

    def post(self, request, venda):
        data = {}
        item = ItemsVenda.objects.filter(produto_id=request.POST['produto_id'], venda_id=venda)
        if item:
            data['mensagem'] = 'Item já incluso no pedido, por favor edite!'
            item = item[0]
        else:
            data['mensagem'] = ''
            item = ItemsVenda.objects.create(
            produto_id=request.POST['produto_id'], quantidade=request.POST['quantidade'],
            desconto=request.POST['desconto'], venda_id=venda)

        data['item'] = item
        data['form_item'] = ItemPedidoForm()
        data['numero'] = item.venda.numero
        data['desconto'] = item.venda.desconto
        data['venda'] = item.venda
        data['itens'] = item.venda.itemsvenda_set.all()

        return render(
            request, 'vendas/novo-pedido.html', data)

class ListaVendas( LoginRequiredMixin, View):
    def get(self, request):
        LoginRequiredMixin.login_url = ''
        my_log.debug('Acessaram a listagem de vendas: ')
        try:
            1/0
        except Exception as e:
            time = datetime.datetime.now()
            my_log.exception(time.strftime("%m/%d/%Y, %H:%M:%S") + '---' + str(request.user))


        vendas = Venda.objects.all()
        count_vendas = vendas.count()
        #count 4
        return render(request, 'vendas/lista-vendas.html', {'vendas': vendas, 'count_vendas':count_vendas})

class EditPedido(View):
    def get(self, request, venda):
        data = {}
        STATUS = VendaStatus

        venda = Venda.objects.get(id=venda)

        data['form_item'] = ItemPedidoForm()
        data['numero'] = venda.numero
        data['desconto'] = float(venda.desconto)
        data['venda'] = venda
        data['itens'] = venda.itemsvenda_set.all()

        if venda.status == 'DC':
            data['status'] = STATUS.DESCONHECIDO.label
        elif venda.status == 'PR':
            data['status'] = STATUS.PROCESSANDO.label
        elif venda.status == 'AB':
            data['status'] = STATUS.ABERTA.label
        elif venda.status == 'FE':
            data['status'] = STATUS.FECHADA.label

        return render(
            request, 'vendas/novo-pedido.html', data)
class DeletePedido(View):
    def get(self, request, venda):
        venda = Venda.objects.get(id=venda)
        return render(
            request, 'vendas/delete-pedido-confirm.html', {'venda': venda})

    def post(self, request, venda):
        venda = Venda.objects.get(id=venda)
        venda.delete()
        return redirect('lista-vendas')


class DeleteItemPedido(View):
    def get(self, request, item):
        item_pedido = ItemsVenda.objects.get(id=item)
        return render(
            request, 'vendas/delete-itempedido-confirm.html', {'item_pedido': item_pedido})

    def post(self, request, item):
        item_pedido = ItemsVenda.objects.get(id=item)
        venda_id = item_pedido.venda.id
        item_pedido.delete()
        return redirect('edit-pedido', venda=venda_id)

class EditItemPedido(View):
    def get(self, request, item):
        item_pedido = ItemsVenda.objects.get(id=item)
        form = ItemPedidoFormModelForm(instance=item_pedido)

        return render(
            request, 'vendas/edit-itempedido.html', {'item_pedido': item_pedido, 'form':form})

    def post(self, request, item):
        item_pedido = ItemsVenda.objects.get(id=item)
        item_pedido.quantidade = request.POST['quantidade']
        item_pedido.desconto = request.POST['desconto']
        item_pedido.save()
        venda_id = item_pedido.venda.id

        return redirect('edit-pedido', venda=venda_id)