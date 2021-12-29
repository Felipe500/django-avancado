from django.urls import path
from .views import produtos_list,Produto_update, Produto_Novo, Produto_Delete


urlpatterns = [
    path('list/', produtos_list, name="produto_list"),

    path('novo/', Produto_Novo, name="Produto_Novo"),
    path('update/<int:id>/', Produto_update, name="produto_update"),
    path('delete/<int:id>/', Produto_Delete, name="Produto_Delete"),
]