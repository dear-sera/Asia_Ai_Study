### Database
- 데이터베이스는 특정 기업이나 조직 또는 개인이 필요에 의해 논리적으로 연관된 데이터를 일정한 형태로 저장해 놓은 것을 의미한다.(논리적 데이터 저장소)

#### DBMS(Database Management System) 데이터베이스 관리 프로그램
- DBMS를 이용해서 입력, 수정, 삭제 등의 기능을 제공한다 (memory+process로 구성되어 있음)

왜 필요한가? 이전까진 각각 나누어졌던 데이터들을 하나에서 관리를 하는 것이 데이터베이스인데, 이 데이터 베이스의 데이터를 보호하고 읽고, 쓰는 것이 정확성, 일관성, 장애를 보호하기 위해 만들어진 프로그램이 DBMS이다.

#### 데이터베이스의 특징
- 실시간 접근성(real time accessibility)  

데이터베이스는 실시간으로 서비스된다. 사용자가 데이터를 요청하면 몇 시간이나 몇 일 뒤에 결과를 전송하는 것이 아니라 수 초 내에 결과를 서비스한다.
- 계속적인 변화(continuous change)

데이터베이스에 저장된 내용은 어느 한 순간의 상태를 나타내지만, 데이터 값은 시간에 따라 항상 바뀐다. 데이터베이스는 삽입(insert), 삭제(delete), 수정(update) 등의 작업을 통하여 바뀐 데이터 값을 저장한다
– 동시 공유(concurrent sharing)

데이터베이스는 서로 다른 업무 또는 여러 사용자에게 동시에 공유된다. 동시(concurrent)는 병행이라고도 하며, 데이터베이스에 접근하는 프로그램이 여러 개 있다는 의미다.
– 내용에 따른 참조(reference by content)

데이터베이스에 저장된 데이터는 데이터의 물리적인 위치가 아니라 데이터 값에 따라 참조된다

#### SQL은? 구조적인 질의 언어
관계형 데이터베이스에서 데이터 조작과 데이터 정의를 하기 위해 사용하는 언어  
DML(DQL) => 조회, 추가 수정, 삭제  
DDL => 데이터 구조(객체)를 생성, 수정, 삭제  
DCL => 해당 구조에 대해 권한을 부여, 회수  
TCL => Tx 제어 (Tx란 트랜직션으로 오류가 나면 아예 취소하거나 결과를 내는 것(오류가 나서 가만히 있으면 안됨))


- sql 실행(임의의 스크립트를 추가함)

-DB에 접속한 계정 확인
```
select user from dual;
```

유저가 생성한(소유의) 테이블 이름 조회
```
select table_name from user_tables;
```

테이블의 구조 확인 명령어는 툴 명령어
```
describe employees
```
- select * from 테이블명 ; => 모든 데이터 조회

 테이블에 선언된 컬럼 순서와 상관없이 조회 가능

- select 컬럼 연산자 값 => 표현식   
- 함수(컬럼)   => 표현식

select expression [as alias](생략가능) from 테이블명;   
```
select sal*12 from emp;     
select sal*12 totalsalary from emp;   
select sal*12 as totalsalary from emp;
```
- alias에서 공백포함 또는 대소문자 구분하고 싶으면 "alias"를 처리합니다
```
select sal*12 as "Total Salary" from emp;
```
#### select-조회(검색)의 종류
1.projection검색 - 1개의 table로부터 column을 기준으로 조회
2. selection - 1개의 table로부터 (조건기반) row기준으로 검색
3. join - 2개 이상의 table로부터 PK, FK컬럼 기준으로 컬럼 값이 일치할 때 두 레코드를 결합, 검색

oracle은 select절과 from절이 필수절  
mysql, mssql등의 dbms는 select만 필수절  

oracle은 from절에 선언될 대상의 table이 없는 경우 dual을 사용해야 한다  

#### desc emp 테이블 구조
number타입 - 정수, 실수 저장 컬럼타입  
number(3)  
number(8, 2)  
char - 고정길이 문자열 ~2000byte  
varchar2 - 가변길이 문자열 ~4000byte    
data - 내부적으로 7byte의 수치값(oo세기 oo년 oo월 일 시 분 초)  
DB에 접속되어 있는 세션 환경 파라미터에 기본값 RR/MM/DD  
영미권 DD-MON-RR  

```
select hiredate from emp;
alter session set nls_data_format = 'YYYY/MM/DD HH24:MI:SS';
select hiredate from emp;
select sysdate from dual; ---sysdate는 시스템 현재시간 반환하는 함수
```
- number타입 컬럼은 산술연산자와 함께 사용 가능
- date타입 컬럼은 +n, -n, -date, +n/24, -n/24, +n/1440 등으로 가능하다
```
select sysdate, sysdate+1, sysdate-1 from dual;
select sysdate, sysdate+5/1440 from dual;
select sysdate-hiredate from emp;
```
- 문자열 컬럼은 결합연산 || 연산자(버티컬바2개)
```
select ename || job from emp;
```
- DB에서는 문자열과 날짜 데이터는 반드시 ''로 감싸서 허용(""이건 안됨)
```
select ename || 'works as a' || job from emp;
select *from emp:
```
- 값이 없는 field은 null  
이때 주의 사항은 null의 산술연산 결과는 null
```
select sal, comm, (sal+comm)*12 from emp;
select sal, comm, (sal+nvl(comm, 0))*12 from emp;
```
연산전에 null처리 함수 적용

! null의 비교연산, 논리연산 결과는 null
! null은 연산 불가
! null은 값이 아직 할당되지 않음을 의미하므로 ''또는 0과 같지 않다
```
select deptno from emp;
select distinct deptno from emp;
```
distinct는 중복제거를 뜻함
```
select deptno, distinct job from emp;  --error! distinct는 모든 컬럼 중 가장 앞에 선언
select distinct | deptno, job from emp;
```
rowid칼럼은 내장컬럼 - 논리적 행 주소(objextid + filed + blockid + 행순서번호)
```
select rowid, deptno, dname from dept;
```
rownum컬럼 내장컬럼 - 결과레코드에 순차 번호 발생
```
select rownum, deptno, dname from dept;
```
select ~
from ~
[where 조건] =>조건은 기준컬럼 비교연산자 비교값 형태

-비교연산자 : >, >=, =, <>, !=, <=, ^=
```
--문제> 사원 중 10번 부서 소속 사원만 검색
select * from emp where deptno=10;

--문제> EMP테이블에서 담당업무가 MANEGER인 사원의 정보를 사원정보, 성명, 담당업무, 급여를 조회
select * from emp where job = 'MANAGER';

--문제>커미션을 받지 않는 사원들을 검색
select * from emp where comm IS NULL; -비교 연산자는 is null
(comm = null;, comm=''; 같은 비교연산은 불가)

--문제>커미션을 받는 사원들을 검색
select * from emp where comm is not NULL;
select * from emp where comm >= 0; (으로도 가능)
```
-범위연산자 기준컬럼 between 하한값 and 상한값
1. 조건1 and 조건2
2. 논리연산자 and, or, not을 이용
```
--문제> EMP 테이블에서 급여서 1300에서 2500사이에 해당되는 사원의 성명, 담당업무, 급여, 부서 번호를 조회
select ename, job, sal, deptno from emp where sal >= 1300 and sal <= 2500;
```
empno in은 값을 추출해줌 >멤버쉽 연산자, 값 목록 중 하나만 일치하더라도 반환 =any, =some와 같은 연산
```
--문제> EMP 테이블에서 사원번호가 7902, 7788, 7566인 사원의 사원번호, 성명, 담당업무, 급여, 입사일자를 조회한다
select ename, job, sal, hiredate from emp where empno in (7902,7788,7566);
select ename, job, sal, hiredate from emp where empno = 7902 or empno = 7788 or empno = 7566; 
--두 코드가 동일함
```
like는 문자열의 패턴을 비교하는 연산자로 만능문자 _(1개문자), %(0개이상 여러개)
```
--문제> EMP테이블에서 이름의 두 번째 글자가 'A'인 사원이름, 급여, 업무를 조회
select ename, sal, job from emp where ename like '_A%';

--문제> EMP테이블에서 이름의 'N'문자로 끝나는 사원이름, 급여, 업무를 조회
select ename, sal, job from emp where ename like '%N';

--문제> EMP테이블에서 급여가 2800 이상이고 JOB이 MANAGER인 사원의 사원번호, 성명, 담당업무, 급여, 입사일자, 부서번호를 조회
select ename, job, sal, hiredate, deptno from emp where sal >= 2800 and job='MANAGER';

--문제> EMP테이블에서 JOB이 'MANAGER', 'CLERK', 'ANALYST'가 아닌 사원의 사원번호, 성명, 담당업무, 급여, 입사일자, 부서번호를 조회
select ename, job, sal, hiredate, deptno from emp where job!='MANAGER' and job!='CLERK' and job!= 'ANALYST';
select empno, ename, job, sal , hiredate, deptno from emp where job not in ('MANAGER', 'CLERK', 'ANALYST');

--문제> EMP테이블에서 급여가 1000에서 3000상에 해당 되지 않는 사원들만 이름, 급여, 업무 조회한다
select ename, sal, job from emp where sal not between 1000 and 3000;
```
연산자들의 우선순위를 염두에 두지 않고 WHERE절을 작성한다면  
테이블에서 자기가 원하는 자료를 찾지 못하거나, 혹은 틀린 자료인지도 모른 채 사용할 수도 있으므로...
연산자 순서
1. 산술연산자
2. ||
3. 비교연산자
4. is null, is not null, like, not like, in, not in
5. between ~ and, not between ~ and
6. not
7. and
8. or
not > and > or 순서는 중요
```
--문제> 직무가 president 이거나 salesman인 사원들 중에서 급여가 1500보다 큰 사원 검색
select * from emp where sal > 1500 AND job in ('PRESIDENT','SALESMAN');
```
검색 결과를 특정 컬럼값 기준으로 정렬된 결과를 만들려면  
order by 컬럼 asc|desc (asc가 기본), 컬럼 asc|desc  
```
select empno, ename, sal from emp;
select empno, ename, sal from emp order by sal;
select empno, ename, sal from emp order by sal desc;

--문제> EMP테이블에서 부서번호로 오름차순 정렬한 후 부서번호가 같을 경우 급여가 많은 순으로 정렬하여 사원번호, 성명, 업무, 부서번호, 급여를 출력하여라.
select empno,ename,job,deptno,sal from emp order by deptno asc, sal desc;
select ename, sal, sal*12 ANN_SAL from emp order by ANN_SAL; > 새로 정렬해도 별칭이 사용 가능할까? >답은 가능

select empno, ename, job, deptno, sal from emp order by 4, 5 desc; > select절의 선언된 column position 값을 사용 가능할까? (위치를 숫자로 나타내도 되는지) > 답은 가능(4은 오름차순, 5는 내림차순)
```
null값은 정렬 결과가 앞에 올까 뒤에 올까?  
답은 오름차순은 뒤, 내림차순은 앞
```
select * from emp order by comm;
select * from emp order by comm desc; 
```
####DB에서 제공하는 함수
SQL은 선언적, 결과지향적 언어이므로 조건처리(X), 변수 사용(X), 예외 처리(X)  
SQL을 좀 더 powerful하게 사용할 수 있도록 함수처리


DB에서 제공하는 함수는 반드시 하나의 값을 리턴함  
조건처리 함수  
null함수  
format 처리 함수  
복잡한 연산 처리 함수....  

Built-in (predefined) 함수 - DBMS에서 제공  
custom function (사용자 정의 함수) => sql + 절차적 언어 (PL/SQL)  

단일행 함수 - 함수의 인수로 1record의 컬럼값이 전달되면, 함수의 정의된 기능 수행 후 1개의 결과 반환  
복수행 함수(그룹 함수) - 함수의 인수로 전체 테이블의 records 또는 그룹핑 된 records가 전달되고, 정의된 기능 수행 후 1개의 결과 반환


단일행 함수의 분류 character function -캐릭터 함수 값이 인수로 전달  
number function - 숫자 함수 값이 인수로 전달  
date function - 날짜 함수 값이 인수로 전달  
conversion function 변환 함수 값이 인수로 전달  
기타 함수  


단일행 함수는 select절, where절, order by절에서 사용 할 수 있음  
함수를 중첩 사용도 가능
```
select lower('Hello World'), upper('Hello World'), initcap('HELLO WORLD') from dual;

select length('korea'), lengthb('korea'), length('대한민국'), lengthb('대한민국') from dual;
--lengthb 에서 b는 byte 즉 바이트 길이를 물어보는 것

select ename|| 'work as a' || job, concat(ename, concat('work as a', job)) from emp;

select substr('Hello World', 7), substr('Hello World', 2, 4), substr('Hello World', -5) from dual;

select instr('Hello World', 'o'), instr('Hello World', 'o', 7), instr('Hello World', 'o', 3, 2) from dual;
--첫 o의 위치, 7번부터 o의 위치, 3번부터 o을 찾는데 2번째 나오는 o를 찾아라

--문제> EMP테이블에서 이름이 첫글자가 'K'보다 크고 'Y'보다 작은 사원의 사원번호, 이름, 업무, 급여, 부서번호를 조회, 결과는 이름순으로 정렬

select empno, ename, job, deptno, sal from emp where substr(ename,1,1) >'K' and substr(ename,1,1)< 'Y' order by ename;

select sal, rpad(sal, 10, '*') from emp; --rpad에 sal을 숫자를 적고 뒤에 10자리를 *로 채워준다
 select ' hello world ', length(' hello world '), length(trim(' hello world ')), from emp; --중간 공백은 제거되지 않는다
```
LTRIM함수 - 문자열의 첫 문자부터 확인해서 지정 문자가 나타나는 동안 해당 문자를 제거  
RTRIM함수 - 문자열의 끝 문자부터 확인해서 지정 문자가 나타나는 동안 해당 문자를 제거  
```
select ename, job, ltrim(job, 'A'), sal, ltrim(sal, 1) from emp where deptno=20;
select ename, job, ltrim(job, 'T'), sal, ltrim(sal, 0) from emp where deptno=10;
select ename, replace(ename, 'SC', '*?') from emp where deptno=20;
select ename, translate(ename, 'SC', '*?') from emp where deptno=20;
