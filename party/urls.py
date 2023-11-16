from django.urls import path
from party import views


list_parties_urlpatterns = [
   path("", views.PartyListPage.as_view(), name="page_party_list"),
]

urlpatterns = list_parties_urlpatterns
