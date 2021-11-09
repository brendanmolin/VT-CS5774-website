from django.urls import path
from . import views

app_name = 'jobber'
urlpatterns = [
    # Base views
    path('', views.opportunities_index, name="opportunities_index"),
    path('search-results', views.opportunities_search_results, name="opportunities_search_results"),
    # Opportunities
    path('opportunities', views.opportunities_list, name="opportunities_list"),
    path('opportunities/sort', views.opportunities_list_sort_ajax, name="opportunities_list_sort_ajax"),
    path('opportunities/<int:id>', views.opportunities_view_item, name="opportunities_view_item"),
    path('opportunities/<int:id>/edit', views.opportunities_edit_item, name="opportunities_edit_item"),
    path('add-opportunity', views.opportunities_add_item, name="opportunities_add-item"),
    path('opportunities/delete', views.opportunities_delete_item, name="opportunities_delete_item"),
    path('opportunities/add_contact_inplace', views.opportunities_add_contact_ajax,
         name="opportunities_add_contact_ajax"),
    path('opportunities/view_contact_inplace', views.opportunities_view_contact_ajax,
         name="opportunities_view_contact_ajax"),
    # Contacts
    path('contacts', views.contacts_list, name="contacts_list"),
    path('contacts/sort', views.contacts_list_sort_ajax, name="contacts_list_sort_ajax"),
    path('contacts/<int:id>', views.contacts_view_item, name="contacts_view_item"),
    path('contacts/<int:id>/edit', views.contacts_edit_item, name="contacts_edit_item"),
    path('add-contacts', views.contacts_add_item, name="contacts_add-item"),
    path('contacts/delete', views.contacts_delete_item, name="contacts_delete_item"),
    # Events
    path('events', views.events_list, name="events_list"),
    path('events/sort', views.events_list_sort_ajax, name="events_list_sort_ajax"),
    path('events/<int:id>', views.events_view_item, name="events_view_item"),
    path('events/<int:id>/edit', views.events_edit_item, name="events_edit_item"),
    path('add-events', views.events_add_item, name="events_add-item"),
    path('events/delete', views.events_delete_item, name="events_delete_item"),
]
