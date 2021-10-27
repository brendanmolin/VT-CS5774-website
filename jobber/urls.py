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
    path('opportunities/delete', views.opportunities_delete_item, name="opportunities_delete_item"),
    path('opportunities/add_contact', views.opportunities_add_contact, name="opportunities_add_contact"),
    path('opportunities/add_contact_inplace', views.opportunities_add_contact_ajax, name="opportunities_add_contact_ajax"),
    path('opportunities/view_contact_inplace', views.opportunities_view_contact_ajax, name="opportunities_view_contact_ajax"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout")
]
