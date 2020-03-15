from django.urls import path

from mysite.polls import views

app_name = 'polls'
urlpatterns = [
    # Tutorial examples.
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

    # Serialization.
    path('choices/', views.ChoiceSerialization.as_view(), name='choices'),
    path('questions/', views.QuestionSerialization.as_view(), name='questions'),

    # Relations.
    path('related/', views.RelatedName.as_view(), name='related'),

    # Transactions.
    path('no-trans/', views.NoTransaction.as_view(), name='no-trans'),
    path('with-trans/', views.WithTransaction.as_view(), name='with-trans'),
    path('nested-trans/', views.NestedTransaction.as_view(), name='nested-trans'),
    path('nested-save/', views.NestedSavePoint.as_view(), name='nested-save'),
]