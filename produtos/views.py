from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produto
from .forms import ProdutoForm



@login_required
def produtos_list(request):
    produtos = Produto.objects.using('default').all()
    return render(request, 'produtos/produtos_list.html', {'produtos': produtos})


def Produto_update(request, id):
    produto_id = get_object_or_404(Produto, pk=id)
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto_id)

    if form.is_valid():
        form.save()
        return redirect('produto_list')

    return render(request, 'produtos/produto_update.html', {'form': form})

@login_required
def Produto_Novo(request):
    produto_id = get_object_or_404(Produto, pk=id)
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto_id)

    if form.is_valid():
        form.save()
        return redirect('produto_list')

    return render(request, 'produtos/produto_update.html', {'form': form})

@login_required
def Produto_Delete(request, id):
    person = Produto.objects.using('default').get(id=id)

    if request.method == 'POST':
        person.delete(using='default')
        return redirect('person_list')

    return render(request, 'produto_delete.html', {'person': person})