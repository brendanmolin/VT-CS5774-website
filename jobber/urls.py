from django.urls import path
from . import views
app_name = 'jobber'
urlpatterns = [
    # opportunities views
    path('', views.opportunities_index, name="opportunities_index"),
    path('opportunities', views.opportunities_list, name="opportunities_list"),
    path('opportunities/<int:id>', views.opportunities_view_item, name="opportunities_view_item"),
    path('opportunities/<int:id>/edit', views.opportunities_edit_item, name="opportunities_edit_item"),
    path('add-item', views.opportunities_add_item, name="opportunities_add-item"),
    path('search-results', views.opportunities_search_results, name="opportunities_search_results"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout")
]
