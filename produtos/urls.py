from django.urls import path
from .views import produtos_list,Produto_update


urlpatterns = [
    path('list/', produtos_list, name="produto_list"),
path('update/<int:id>/', Produto_update, name="produto_update"),

]