from django.urls import path

from . import views

app_name = "lab"

urlpatterns = [
    path("healthz/", views.health_check, name="health_check"),
    path("", views.home, name="home"),
    path("equipes/", views.team_list, name="team_list"),
    path("equipes/<slug:slug>/", views.team_detail, name="team_detail"),
    path("membres/permanents/", views.members_permanent, name="members_permanent"),
    path("membres/permanents/<int:pk>/", views.member_permanent_detail, name="member_permanent_detail"),
    path("membres/doctorants/", views.members_doctorants, name="members_doctorants"),
    path("membres/doctorants/<int:pk>/", views.member_doctorant_detail, name="member_doctorant_detail"),
    path("membres/associes/", views.members_associates, name="members_associates"),
    path("membres/associes/<int:pk>/", views.member_associate_detail, name="member_associate_detail"),
    path("activites/", views.activities, name="activities"),
    path("production-scientifique/", views.production, name="production"),
    path("formations/", views.formations, name="formations"),
    path("partenaires/", views.partners, name="partners"),
    path("actualites/", views.news_list, name="news_list"),
    path("contact/", views.contact, name="contact"),
]
