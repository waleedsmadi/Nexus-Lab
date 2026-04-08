from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('product.urls', namespace='product')),
    path('', include('comment.urls', namespace='comment')),
    path('', include('pages.urls', namespace='pages')),
    path('wallet/', include('wallet.urls', namespace='wallet')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('reports/', include('reports.urls', namespace='reports')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

