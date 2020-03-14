from django.urls import path

from mysite.polls import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('questions/', views.QuestionView.as_view(), name='questions'),
    path('choices/', views.ChoiceView.as_view(), name='choices'),
    path('related/', views.RelatedView.as_view(), name='related'),
    path('no-trans/', views.NoTransaction.as_view(), name='no-trans'),
    path('with-trans/', views.WithTransaction.as_view(), name='with-trans'),
    path('nested-trans/', views.NestedTransaction.as_view(), name='nested-trans'),
    path('nested-save/', views.NestedSavePoint.as_view(), name='nested-save'),
]