from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api import views


router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='streamplatform')


urlpatterns = [
    path('', views.WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', views.WatchDetailAV.as_view(), name='movie-detail'),    
    path('', include(router.urls)),

    path('<int:pk>/reviews/create/', views.ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', views.ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),

    path('user-reviews/', views.UserReview.as_view(), name='user-review-detail'),

]











# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# # from watchlist_app.api.views import movie_list, movie_details
# from watchlist_app.api.views import WatchListAV,WatchDetailAV,StreamPlatformAV,StreamPlatformDetailAV,ReviewList
# from watchlist_app.api.views import ReviewDetail,ReviewCreate,StreamPlatformVS,UserReview,WatchList
# router=DefaultRouter()
# router.register('stream',StreamPlatformVS,basename='streamplatform')

# urlpatterns = [
#     path('list/', WatchListAV.as_view(), name='movie-list'),
#     path('list2/', WatchList.as_view(), name='watch-list-new'),
#     path('<int:pk>', WatchDetailAV.as_view(), name='movie-detail'),
#     path('',include(router.urls)),

#     # path('stream/',StreamPlatformAV.as_view(),name='stream'),
#     # path('stream/<int:pk>',StreamPlatformDetailAV.as_view(),name='streamdetail'),
    
#     # path('review/',ReviewList.as_view(),name='review-list'),
#     # path('review/<int:pk>',ReviewDetail.as_view(),name='review-detail'),

#     path('<int:pk>/review-create/',ReviewCreate.as_view(),name='review-create'),
#     path('review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),
#     path('<int:pk>/reviews/',ReviewList.as_view(),name='review-list'),
#     path('reviews/',UserReview.as_view(),name='user-review-detail'),


# ]