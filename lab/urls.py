from django.urls import path

from . import views

app_name = "lab"

urlpatterns = [
    path("", views.home, name="home"),
    path("equipes/", views.team_list, name="team_list"),
    path("equipes/<slug:slug>/", views.team_detail, name="team_detail"),
    path("thematiques/", views.themes, name="themes"),
    path("membres/permanents/", views.members_permanent, name="members_permanent"),
    path("membres/doctorants/", views.members_doctorants, name="members_doctorants"),
    path("membres/associes/", views.members_associates, name="members_associates"),
    path("partenaires/", views.partners, name="partners"),
    path("actualites/", views.news_list, name="news_list"),
    path("contact/", views.contact, name="contact"),
]
