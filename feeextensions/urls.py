from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import create_fee_extension, fee_extension_method, FeeExtensionsView

# Create a router and register the FeeExtensionsView
router = DefaultRouter()
router.register(r'fee-extensions', FeeExtensionsView, basename='fee-extensions')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),

    # Define the additional URL patterns
    path('create_fee_extension/<int:student_id>/', create_fee_extension, name='create_fee_extension'),
    path('fee_extension_method/<int:fee_extension_id>/', fee_extension_method, name='fee_extension_method'),
]
