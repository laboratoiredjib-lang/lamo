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
    path("activites/conferences/", views.activities_conferences, name="activities_conferences"),
    path("activites/seminaires/", views.activities_seminaires, name="activities_seminaires"),
    path("activites/olympiades/", views.activities_olympiades, name="activities_olympiades"),
    path("activites/participations/", views.activities_participations, name="activities_participations"),
    path("activites/responsabilites-editoriales/", views.activities_editorial, name="activities_editorial"),
    path("production-scientifique/", views.production, name="production"),
    path("production-scientifique/articles/", views.production_articles, name="production_articles"),
    path("production-scientifique/theses/", views.production_theses, name="production_theses"),
    path("production-scientifique/hdr/", views.production_hdr, name="production_hdr"),
    path("production-scientifique/projets/", views.production_projets, name="production_projets"),
    path("formations/", views.formations, name="formations"),
    path("formations/masters/", views.formations_masters, name="formations_masters"),
    path("formations/encadrement-doctoral/", views.formations_doctoral, name="formations_doctoral"),
    path("formations/jurys-de-these/", views.formations_jury, name="formations_jury"),
    path("formations/offres-de-stage/", views.formations_stage, name="formations_stage"),
    path("formations/renforcement-de-capacites/", views.formations_capacity, name="formations_capacity"),
    path("partenaires/", views.partners, name="partners"),
    path("actualites/", views.news_list, name="news_list"),
    path("contact/", views.contact, name="contact"),
]
