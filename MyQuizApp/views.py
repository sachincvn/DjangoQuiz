import email
from re import U
from django.contrib import messages
from django.contrib.auth.models import User
from .models import quizquestion, quiztopics, useranswers,userProfile
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage

def signUp(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method == "POST":
            #GET DATA FROM SIGNUP FORM
            users_first_name =  request.POST['firstname']
            users_last_name =  request.POST['lastname']
            users_user_name =  request.POST['username']
            users_email_id =  request.POST['email']
            users_c_password =  request.POST['cpassword']
            users_mobile =  request.POST['mobileno']
            users_dob =  request.POST['dob']
            users_gender =  request.POST['gender']

            if(len(users_user_name)<6):
                # print("Username Must Be Atleast 6 charcher")
                messages.error(request, 'Username Must Be Atleast 6 charcher')
            elif (len(users_c_password)<6):
                # print("Password must be more then 6 character")
                messages.error(request, 'Password must be more then 6 character')
            elif(len(users_mobile)<10):
                # print("Enter Correct Mobile Number")
                messages.error(request, 'Enter Correct Mobile Number')
            else:
                myuser = User.objects.create_user(users_user_name,users_email_id,users_c_password)
                myuser.first_name = users_first_name
                myuser.last_name = users_last_name
                add_users = userProfile(mobie_number=users_mobile,dob=users_dob,gender=users_gender,is_admin=False,user=myuser)
                myuser.save()
                add_users.save()
                return redirect("Login")
        else:
            print("Wrong")

        
        return render(request,"MyQuiz/signup.html")


def logIn(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    else:
        if request.method == "POST":
            users_user_name =  request.POST['username']
            users_password =  request.POST['password']

            user = authenticate(username=users_user_name,password=users_password)

            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Sucessfully")
                return HttpResponseRedirect("/")
            else:
                messages.error(request, 'Invalid Credentials, Please Try Again..')
        return render(request,"MyQuiz/login.html")

def userLogout(request):
    logout(request)
    messages.info(request,"Logged out Sucessfully")
    return redirect("index")

def quizIndex(request):
    get_quizs = quiztopics.objects.all()
    return render(request,'MyQuiz/index.html',{'quizs_topic':get_quizs})

def myProfile(request):
    if request.user.is_authenticated:
        current_user = request.user
        first_name = current_user.first_name
        last_name = current_user.last_name
        email = current_user.email
        user_id = current_user.id
        password = current_user.password
        print(password)
        user_profile = userProfile.objects.filter(user_id=user_id)
        for user_detail in user_profile:
            gender = user_detail.gender
            mobile_number = user_detail.mobie_number
            dob = user_detail.dob

                
        return render(request,"MyQuiz/myprofile.html",
        {
            "username":current_user,
            "firstname":first_name,
            "lastname":last_name,
            "email":email,
            "userid":user_id,
            "gender":gender,
            "mobile":mobile_number,
            "dob":dob,
        })



def quizTest(request,slug):  
    if request.user.is_authenticated:
        current_user = request.user
        get_quizs = quiztopics.objects.all()

        for quiz in get_quizs:
            quizcat = quiz.quiz_cat
            quiztitile =  quiz.quiz_title
            get_quizsqn = quizquestion.objects.filter(qn_cat=quizcat)
            get_user_ans  =  useranswers.objects.filter(username=current_user.username,qn_cat=quizcat)
            if request.method == "POST":
                ans_dict = request.POST
                for quizqn in get_quizsqn:
                    quiz_qn_name = quizqn.qn_name 
                    quiz_crt_ans = quizqn.qn_ans            
                    for i in ans_dict:
                        if quiz_qn_name == i:
                            print(i,ans_dict[quiz_qn_name])
                            fname = current_user.first_name+" "+current_user.last_name
                            uname = current_user.username
                            emailid = current_user.email
                            qncat = quizcat
                            qnname = i
                            qnans = ans_dict[i]
                            crtans = quiz_crt_ans
                            addans = useranswers(full_name=fname,username=uname,
                            email_id=emailid,qn_cat=qncat,qn_name=qnname,qn_ans=qnans,crt_ans=crtans)
                            addans.save()

            if quiz.quiz_url==slug:
                return render(request,'MyQuiz/quiz.html',
                {'quiz_questions':get_quizsqn,
                'quizcat':quizcat,
                'quiztitile':quiztitile,
                'full_name':current_user.first_name+" "+current_user.last_name,
                'email':current_user.email,
                'quiz_id':quiz.quiz_id,
                'quiz_answers':get_user_ans,
                })
    else:
        messages.error(request, 'Please Login To Continue..')
        return redirect("Login")

    return HttpResponse('Not Avalible')



def quizResult(request,slug):
    if request.user.is_authenticated:
        current_user = request.user
        get_quizs = quiztopics.objects.all()
        user_answers = useranswers.objects.filter(username=current_user.username)
                    
        for quiz in get_quizs:
            quizcat = quiz.quiz_cat
            quiztitile =  quiz.quiz_title
            get_quizsqn = quizquestion.objects.filter(qn_cat=quizcat)
            get_user_ans  =  useranswers.objects.filter(username=current_user.username,qn_cat=quizcat)

            if quiz.quiz_url==slug:     
                total_qn = len(get_quizsqn)
                user_answerd = len(get_user_ans)
                correct_answer = 0
                wrong_answer = 0
                for ans in get_user_ans:
                    if ans.qn_ans == ans.crt_ans:
                        correct_answer += 1   
                    else:
                        wrong_answer += 1
                return render(request,'MyQuiz/result.html',{
                    'user_result':get_user_ans,
                    'full_name':current_user.first_name+" "+current_user.last_name,
                    'email_id':current_user.email,
                    'quiz_cat':quizcat,
                    'quiz_questions':total_qn,
                    'user_attempetd':user_answerd,
                    'correct_answer':correct_answer,
                    'wrong_answer':wrong_answer,
                    'total_points': correct_answer*10,
                    'quiz_qns' : get_quizsqn,
                })

        return HttpResponse('Not Avalible')
    else:
        return redirect("Login")


def addQuiz(request):
    if request.user.is_authenticated:
        current_user = request.user
        if current_user.is_staff== True:
            if request.method == "POST" and request.FILES['quiz_thumb']:
                cat = request.POST['quiz_cat']
                title = request.POST['quiz_title']
                desc = request.POST['quiz_desc']
                quizurl = request.POST['quiz_url']
                thumb = request.FILES['quiz_thumb']
                fs = FileSystemStorage()
                fileName = fs.save("MyQuiz/images/"+thumb.name,thumb)
                url = fs.url(fileName)
                add_quiz = quiztopics(quiz_cat=cat, quiz_title=title, quiz_desc=desc,quiz_url=quizurl,quiz_thumb=url)
                add_quiz.save()
                return HttpResponseRedirect('addquiz')

            get_quizs = quiztopics.objects.all()

            return render(request,'MyQuiz/addquiz.html',{
                "quiz_topics":get_quizs,
            })
        else:
            return HttpResponse("Hello Jii, You are not a admin")



def addQuestion(request,slug):
    if request.user.is_authenticated:
        current_user = request.user
        if current_user.is_staff== True:
            get_quizs = quiztopics.objects.all()
            for quiz in get_quizs:
                if quiz.quiz_cat==slug:
                    quizcat = quiz.quiz_cat
                    quiztitile =  quiz.quiz_title
                    get_quizsqn = quizquestion.objects.filter(qn_cat=quizcat)
            
            if request.method == "POST":
                qncat = request.POST['qn_cat']
                qntitle = request.POST['qn_title']
                qnname = request.POST['qn_name']
                qnopt1 = request.POST['qn_opt1']
                qnopt2 = request.POST['qn_opt2']
                qnopt3 = request.POST['qn_opt3']
                qnopt4 = request.POST['qn_opt4']
                qnans = request.POST['qn_ans']
                add_question=quizquestion(qn_cat=qncat,qn_title=qntitle,qn_name=qnname,qn_opt1=qnopt1,qn_opt2=qnopt2,qn_opt3=qnopt3,qn_opt4=qnopt4,qn_ans=qnans)
                add_question.save()
            
            return render(request,'MyQuiz/addquestion.html',{
                "quiztitile":quiztitile,
                "quizcat":quizcat,
                "quiz_questions":get_quizsqn
            })
        else:
            return HttpResponse("You Are Not A Admin To Access This Page")

    else:
        return HttpResponse("Hello Jii")



def userResponse(request,slug):
    if request.user.is_authenticated:
        current_user = request.user
        if current_user.is_staff== True:
            print("Admin Here")
            quizcat = slug
            print(quizcat)

            qn_attempted = 0
            correct_answer = 0
            wrong_answer = 0
            total_response = []
            total_users = User.objects.all()
            for quiz_user in total_users:
                user_name = quiz_user
                get_user_ans  =  useranswers.objects.filter(username=user_name.username,qn_cat=quizcat)
                for user_answer in get_user_ans:
                    for user_answer in get_user_ans:
                        qn_attempted+=1
                        if user_answer.qn_ans == user_answer.crt_ans:
                            correct_answer += 1   
                        else:
                            wrong_answer += 1
                    total_response.append({'username':user_answer.username,
                    'fullname': user_answer.full_name,
                    'emailid':user_answer.email_id,
                    'correct_answer':correct_answer,
                    'question_attempted':qn_attempted,
                    'wrong_answer': wrong_answer,
                    'total_score':correct_answer*10})
                    correct_answer=0
                    qn_attempted=0
                    wrong_answer=0
                    break

            
            print(total_response)
    return render(request,"MyQuiz/user-response.html",{
        'quizcat':slug,
        'total_response':total_response,
    })


def deleteQuiz(request,slug):
    if request.user.is_authenticated:
        current_user = request.user
        if current_user.is_staff== True:
            if request.method == "POST":
                delQuiz = quiztopics.objects.get(quiz_cat=slug)
                delQuiz.delete()
                return HttpResponseRedirect('/addquiz') 
    else:
        return HttpResponse("LoooooooooL")
    return HttpResponseRedirect('/') 


def editQuestion(request,id):
    if request.user.is_authenticated:
        current_user = request.user
        if current_user.is_staff== True:
            editQn = quizquestion.objects.filter(qn_id=id)

            if request.method == "POST":
                qncat = request.POST['qn_cat']
                qntitle = request.POST['qn_title']
                qnname = request.POST['qn_name']
                qnopt1 = request.POST['qn_opt1']
                qnopt2 = request.POST['qn_opt2']
                qnopt3 = request.POST['qn_opt3']
                qnopt4 = request.POST['qn_opt4']
                qnans = request.POST['qn_ans']
                quizquestion.objects.filter(qn_id=id).update(qn_cat=qncat,qn_title=qntitle,qn_name=qnname,qn_opt1=qnopt1,qn_opt2=qnopt2,qn_opt3=qnopt3,qn_opt4=qnopt4,qn_ans=qnans)
                messages.success(request,"Question Updated Successfully..")
                return HttpResponseRedirect(request.session['addquestion'])
    else:
        return HttpResponse("LLOOOOOOOOOOLLLL")
    request.session['addquestion'] = request.META.get('HTTP_REFERER','/')
    
    return render(request,"MyQuiz/editquestion.html",{
            "edit_question":editQn
        })


def deleteQuestion(request,id):
    if request.user.is_authenticated:
        current_user = request.user
        if current_user.is_staff== True:

            if request.method == "POST":
                delQuiz = quizquestion.objects.get(qn_id=id)
                delQuiz.delete()
                messages.error(request,"Question Deleted Successfully..")
                return HttpResponseRedirect(request.session['addquestion']) 
    else:
        return HttpResponse("LoooooooooL")
    return HttpResponseRedirect('/') 


def about(request):
    return render(request,"MyQuiz/about.html") 