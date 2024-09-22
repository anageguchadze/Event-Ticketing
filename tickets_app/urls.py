from django.urls import path
from .views import index, login, register, event_list, create_event, update_event, delete_event, organizer_page, customer_page

urlpatterns = [
    path('', index, name='index'),
    path('login/', login,name='login'),
    path('register/', register, name='register'),
    path('event_list/', event_list, name='event_list'),
    path('create_event/', create_event, name='create_event'),
    path('<int:event_id>/update/', update_event, name='update_event'),
    path('<int:event_id>/delete/', delete_event, name='delete_event'),
    path('organizer_page/', organizer_page, name='organizer_page'),
    path('customer_page/', customer_page, name='customer_page'),
    # path('available_courses/', available_courses, name='available_courses'),
]