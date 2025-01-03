from django.urls import path
from . import views

app_name = "ads"
urlpatterns = [
    path('', views.AdListView.as_view(), name="all"),
    path('ad/<int:pk>', views.AdDetailView.as_view(), name="ad_detail"),
    path('ad/create', views.AdCreateView.as_view(), name="ad_create"),
    path('ad/<int:pk>/update', views.AdUpdateView.as_view(), name="ad_update"),
    path('ad/<int:pk>/delete', views.AdDeleteView.as_view(), name="ad_delete"),
    path('ad_picture/<int:pk>', views.stream_file, name='ad_picture'),
    path('ad/<int:pk>/comment', views.AdCommentCreateView.as_view(), name="ad_comment_create"),
    path('comment/<int:pk>/delete', views.AdCommentDeleteView.as_view(), name="ad_comment_delete")
]
