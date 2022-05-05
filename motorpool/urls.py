from django.urls import path
from django.views.decorators.http import require_POST
from . import views

app_name = 'motorpool'

urlpatterns = [
    # Model: Brand
    path('brand-list/', views.BrandListView.as_view(), name='brand_list'),
    path('brand-detail/<int:pk>/', views.BrandDetailView.as_view(), name='brand_detail'),
    path('brand-create/', views.BrandCreateView.as_view(), name='brand_create'),
    path('brand-update/<int:pk>/', views.BrandUpdateView.as_view(), name='brand_update'),
    path('brand-delete/<int:pk>/', views.BrandDeleteView.as_view(), name='brand_delete'),

    # Model: Auto
    path('auto-create/<int:brand_pk>/', views.AutoCreationView.as_view(), name='auto-create'),

    path('send-email/', views.send_email_view, name='send_email'),
    path('brand-add-to-favorite/', require_POST(views.BrandAddToFavoriteView.as_view()), name='brand_add_to_favorite'),
]