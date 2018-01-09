from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add$', views.add),
    url(r'^add_skill_process$', views.add_skill_process),
    url(r'^calculate_process$', views.calculate_process),
    url(r'^calculate_damage_process$', views.calculate_damage_process),


    url(r'^get_class_skill$', views.get_class_skill),
]