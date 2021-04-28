static page 서비스  
web server  
dynamic page 서비스  
WAS (application 실행 환경 conatiner 포함)   
session  
cookie(보안에 약하다)  
Framework  

Django FrameWork(개발 서버 제공 + 웹 어플리케이션을 개발, 운영 구조 제공)    
MVC(Model View Controller) - 데이터 관리, 사용자 요청 처리, 사용자 인터페이스를 분리해서 개발하는 패턴 =＞개발，운영 관리，확장　용이 MTV(Model Templete View)   


ORM (Object Relational Mapping) -SQL 없이 객체를 Database의 Table, Row 매핑해서 CRUD 작업 수행   


#### 가상환경 생성 , 장고 설치

가상환경 만들기     
C:\>python -m venv myweb     

가상 환경 진입, 활성화  
C:\>cd myweb\Scripts  
C:\>myweb\Scripts>activate   

가상환경에 장고 설치하기   
(myweb) C:\myweb\Scripts>pip install django   

pip 최신 버전 설치   
(myweb) C:\myweb\Scripts>python  -m pip install --upgrade pip   
(myweb) C:\>myweb\Scripts>deactivate  

##### 장고 프로젝트 생성  

프로젝트 루트 디렉토리 생성  
C:\workspace>mkdir project  
C:\workspace>cd project   

프로젝트 루트 디렉토리안에서 가상 환경 진입  
C:\workspace\project>c:\myweb\Scripts\activate  

장고 프로젝트 물리적 저장소 디렉토리 생성  
(myweb) C:\workspace\project>mkdir mysite  
(myweb) C:\workspace\project>cd mysite  
(myweb) C:\workspace\project\mysite>  

장고 프로젝트 생성  
(myweb) C:\workspace\project\mysite>django-admin startproject config .   

개발 서버 구동  
(myweb) C:\workspace\project\mysite>python manage.py runserver  

웹 브라우저로 웹 서버에 요청 (welcome페이지 응답 확인)     
http://127.0.0.1:8000/    


##### 메모장에 아래 내용을 편집 후  myweb.cmd 파일명으로저장   
@echo off  
cd c:\workspace\project\mysite   
c:\myweb\scripts\activate   

파이참 community 버전 다운로드   
설치   
실행 > Open > c:\workspace\project\mysite   
 
#### 앱 생성 (장고가 제공하는 기본 앱, 개발자가 직접 만든 앱)   
(myweb) C:\workspace\project\mysite>django-admin startapp first   
#C:\workspace\project\mysite아래에 first디렉토리와 여러 *.py 파일 생성됨    

#### 개발 서버 구동   
(myweb) C:\workspace\project\mysite>python manage.py runserver    
#웹 브라우저로 웹 서버에 요청 (welcome페이지 응답 확인)     
http://127.0.0.1:8000/first     
결과 page not found (404) 오류 발생 =>원인은 urls.py에 url패턴과 view함수 매핑이 없어서   

#### #url패턴 설정  
C:\workspace\project\mysite\config\urls.py파일에  아래 내용으로 수정  

```
from django.contrib import admin  
from django.urls import path
from first import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('first/', views.index)
]
```

#### first앱의 view함수 추가    
C:\workspace\project\mysite\first\views.py파일에 아래 내용 추가 

```
from django.shortcuts import render
from django.http import HttpResponse

Create your views here.

def  index(request) :
    return HttpResponse ("안녕하세요? 장고 first앱 입니다. ")
```

설치 끝
