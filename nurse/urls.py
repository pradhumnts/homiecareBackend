from django.urls import path
from nurse import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nearby/', views.nearby_nurses, name='nearby_nurses'),
    path('get_nurse/', views.nurse_profile, name='get_nurse'),
    path('update-nurse/', views.UpdateNurse.as_view()),
    path('messages/', views.GetMessage.as_view()),
    path('messages-user-list/', views.GetMessageUsersList.as_view()),
    path('update-message-status/', views.UpdateMessageStatus.as_view()),
    path('add-message/', views.AddMessage.as_view()),
    path('add-review/', views.AddReview.as_view()),
    path('get-review/', views.GetReview.as_view()),
    path('get-user-review/', views.GetUserReviews.as_view()),
    path('get-nurse-qualifications/', views.GetQualifications.as_view()),
    path('update-nurse-qualifications/', views.UpdateOrCreateQualifications.as_view()),
    path('search-nurse/', views.SearchNurse.as_view()),
    path('search-nurse-by-location/', views.SearchNurseByLocation.as_view()),
    path('get-nurse-profile/', views.GetNurseProfile.as_view()),
    path('get-nurse-reviews/', views.GetNurseReviews.as_view()),
    path('push-notification-token/', views.PushNotificationToken.as_view()),
]