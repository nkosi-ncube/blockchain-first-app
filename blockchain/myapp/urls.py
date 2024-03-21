from django.urls import path
from .views import mine_block,display_chain,validate_chain,home

urlpatterns=[   
    path("",home,name="home"),
    path('mine_block/',mine_block,name="mine_block"),
    path("display_chain/",display_chain,name="display_chain"),
    path("validate_chain/",validate_chain,name="validate_chain"),
]