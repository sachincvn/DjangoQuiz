from django.urls import path
from . import views

urlpatterns = [
    path('',views.quizIndex,name='index'),
    path('quiz/<str:slug>',views.quizTest,name='MyQuiz'),
    path('quiz/<str:slug>/result',views.quizResult,name='QuizResult'),
    path('addquiz',views.addQuiz,name='AddQuiz'),
    path('<str:slug>/addquestion',views.addQuestion,name='AddQuestion'),
    path('login',views.logIn,name='Login'),
    path('signup',views.signUp,name='SignUp'),
    path('logout',views.userLogout,name='Logout'),
    path('myprofile',views.myProfile,name='MyProfile'),
    path('<str:slug>/user-response',views.userResponse,name='UserResponse'),
    path('deletequiz/<str:slug>',views.deleteQuiz,name="deletequiz"),
    path('editquestion/<int:id>',views.editQuestion,name="editquestion"),
    path('deletequestion/<int:id>',views.deleteQuestion,name="deletequestion"),
    path('about',views.about,name='about')
]