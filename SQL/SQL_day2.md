### SQL_day1 정리

database : 논리적 data들의 저장소 단위  
DBMS : database 관리 시스템  
트랜잭션 처리 뛰어난 장점을 가진 DBMS : RDBMS(관계형)  
RDBMS에서 데이터 저장 객체 - table  

- table : column(attribute)과 row(record, tuple, entityinstance)구성
- Primary Key: 유일하게 하나의 row를 식별하기 위해 사용하는 속성(키) PK, not null+unique
- Unique Key : 유일하게 하나의 row를 식별(null을 허용)
- Foreign Key : data의 참조 관계를 설정할 때 사용되는 키

부모테이블의 PK 또는 UK를 자식테이블의 FK가 참조함으로써 데이터의 무결성 보장

벤더 별 DBMS는 구조(메모리, 프로세스)가 다르고 내부에 data를 저장하는 형식이 다르지만, 데이터를 독립적으로 사용할 수 있도록 표준 언어 사용 => SQL

SQL 문 분류:  

- DML : select, insert, update, delete, merge
- DDL : (table, index, ciew,...) create, alter, drop, truncate,...
- DCL : grant, revoke
- TCL : rollback, commit

Transaction : 여러 명령을 하나의 작업단위로 실행 또는 취소, unit of work  
(ACID 원자성, 일관성, 고립성, 영속성 특성)  

DB의 물리적 구조 - DISK, FILE, BLOCK(PAGE)  
DB의 논리적 구조 - Database, Tablespace, Segment, Extent, Block  

모든 DB의 기본 보안을 위한 기능 - 1. 인증, 2. 권한  
  
connect - conn 명령어  
create user ~ ; 사용자, 인증방법 DB에 등록  

DB에 저장되는 data 종류  
1. User Data(Application Data, Business Date)  
2. Meta Data(DBMS가 DB를 관리하기 위한 데이터 - data dictionary, system datalog)  

- [데이터 검색] []는 생략가능  

select * | distinct column, column,.... | expression [[as] alias]  
from table명  
[where조건]  
[order by 컬럼(표현식 | alias | column position) 정렬방식 (asc|desc) ]  

- 컬럼 데이터 타입:  
char, varcha2(varchar와 호환), CLOB(문자열을 4GB까지 저장)  
number(p, s)  
date  

- 검색종류 :

projection - 1table, 컬럼기준 (select ~ from ~)  
selection - 1able, row기준 (select ~ from ~ where 조건)   
join - 2개이상 table, 동일 속성 컬러값이 일치할 때 row결합 => 검색 결과  

- select의 표현식 : 컬럼 연산자 값 , 함수(컬럼) 

number타입 컬럼의 연산자 : 산술연산자   
date타입 컬럼의 연산자: +n, -n, -date, +n/24  
문자열 타입 컬럼의 연산자 : ||  

- where절의 조건에 사용되는 연산자:  

비교연산자 : >, >=, =, !=, <>,...  
범위연산자 : 컬럼 between 하한값 and 상한값  
문자 패턴 비교 연산자 : like '', 만능문자 _, %  
멤버쉽연산자 : in    
논리 연산자 : not, and, or  

null 비교 연산자 : is null, is not null    
null => 아직 할당되지 않은 값, 산술연산, 비교연산, 논리연산 모두 연산불가, null반환  
''과 같지 않음, 0과 같지 않음  

- 함수 : 반드시 하나의 값을 반환

single row function  
multiple row function(group function)  

복잡한 계산 처리  
형변환  
null처리  
조건 처리  
출력 format 변경  
nested해서 사용 가능  

- character function   

대소문자 변환-lower,upper  
문자열 길이- length  
문자열 부분 추출-substr  
문자열의 위치 반환 - rpad, lpad, replace, translate, ltrim, rtrim, trim  

### day2

#### 오라클 기본 함수
round(n, [m]) : 반올림을 수행 n=값, m=옵션 어디위치에서 올릴 것인지  
trunc(n, [m]) : 소수점 절사를 수행 n=값, m=옵션 어디위치에서 자를 것인지   
power(n, m) : n의 m제곱  
mod(m, n): m/n의 나머지 반환 함수
ceil(n) : 현재 값(n)의 큰 정수의 값을 출력  
floor(n) : 현재 값(n)의 작은 정수의 값을 출력  
SIGN(n) : n보다 크면 1, n보다 작으면 -1, n이랑 같을 경우 0

```
--문제EMP 테이블에서 급여를 30으로 나눈 나머지를 구하여 출력하여라
select sal, mod(sal, 30) from emp;

--문제> 사원번호가 홀수인 사원들만 사원번호와 이름 출력
select empno from emp where mod(empno, 2) = 1;

--SIGN(n) -2975가 기준으로 2975보다 작으면 -1 크면 1 같으면 0
select ename, sal, sign (sal-2975) from emp;
```

#### date funcition
sysdate : 시스템 현재 날짜 시간 반환 함수  
select sysdate from dual;  
세션 날짜 시간 출력 파라미터 RR/MM/DD 기본값  
ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';  

timestamp 컬럼타입  
timestamp with timezone 컬럼타입  
interval year to month 컬럼타입  
interval day to second 컬럼타입  

```
select sysdate, systimestamp, current_date, current_timestamp
from dual;

select sessiontimezone
from dual;  --세션의 timezone값 확인

alter session set time_zone='+3:00';   --세션의 timezone 변경

select sysdate, systimestamp, current_date, current_timestamp
from dual;  
-- current_date, current_timestamp는 세션의 timezone 기준으로 현재시간 반환
--sysdate, systimestamp는 시스템(컴퓨터 OS)의 현재 시간 반환

alter session set time_zone='+9:00';
ALTER SESSION SET NLS_DATE_FORMAT = 'RR/MM/DD' ;

-- 문> EMP 테이블에서 현재까지의 근무일수가 몇 주 몇 일인가를 조회한다.
SELECT ename, hiredate, sysdate, sysdate-hiredate "Totoal Days", 
           trunc((sysdate-hiredate) / 7, 0) Weeks, 
           round(mod((sysdate-hiredate), 7), 0) DAYS
FROM emp 
ORDER BY sysdate-hiredate desc;
-- ORDER BY  "Totoal Days"  desc;
```
extract() -  datetime 또는 interval 값 표현식에 지정된 datetime 필드의 값을 추출하여 반환한다.
```
SELECT extract ( day from sysdate) 일자, extract ( month from sysdate) 월, 
 extract ( year from sysdate) 년도
 FROM dual ; 

SELECT SYSTIMESTAMP A, EXTRACT(HOUR FROM SYSTIMESTAMP) B, 
          TO_CHAR(SYSTIMESTAMP,'HH24') C
 FROM DUAL;
```
 MONTHS_BETWEEN(date1, date2) : 두 날짜 사이의 개월 수가 얼마인지를 구하는 함수
```
 --문제> EMP 테이블에서 현재까지의 근무 월수를 계산하여 조회한다.
SELECT ename, hiredate, sysdate, 
          months_between(sysdate, hiredate) m_between, 
           trunc(months_between(sysdate, hiredate), 0) t_between
 FROM emp;
```
 ADD_MONTHS(date, integer) : 날짜에 개월 수를 더한 뒤 그 결과를 반환하는 함수
```
 --문> EMP 테이블에서 입사 일자로부터 5개월이 지난 후 날짜를 계산하여 출력하여라.
SELECT ename, hiredate, add_months(hiredate, 5) a_month
FROM emp;
```
NEXT_DAY(date, char) : 지정한 date 이후의 날짜 중에서 char로 명시된 요일에 해당되는 첫 번째 일자를 반환
```
select next_day(sysdate, '화') from dual;

-- 문> EMP 테이블에서  입사 일자로부터 돌아오는 금요일, 토요일을 계산하여 조회
 SELECT ename, hiredate, next_day(hiredate, 6) n_6,
next_day(hiredate, 7) n_7 
FROM emp 

SELECT hiredate, ROUND(hiredate,'MONTH'), ROUND(hiredate,'YEAR')
 FROM emp;

SELECT hiredate, trunc(hiredate,'MONTH'), trunc(hiredate,'YEAR')
 FROM emp;
```
to_char는 숫자나 날짜 값을 특정 형식의 문자열로 변환합니다
```
 select to_char(123456.789, '$999,999,999.000')
from dual;

select to_char(sysdate, 'YYYY') from dual;

select to_char(sysdate, 'RR"년" MM"월" DD"일" HH24:MI:SS') from dual;
```
to_number는 숫자형식의 문자값을 숫자로 변환  
반드시 입력문자열 형식과 변환할  숫자 형식(fmt)을 동일하게  선언해야 합니다.
```
select to_number('$12,345.75', '99,999.99') from dual;  --> error
select to_number('$12,345.75', '$999,999.99') from dual; -->변환 결과는 DB에 저장가능한 수치 데이터
```
to_date는 날짜형식의 문자값을 날짜로 변환  
반드시 입력문자열 형식과 변환할  날짜 형식(fmt)을 동일하게  선언해야 합니다.
 ```
select to_date('2014-12-15 19:15:35', 'RR/MM/DD') from dual;  --> error
select to_date('2014-12-15 19:15:35', 'YYYY-MM-DD HH24:MI:SS') from dual; --세션의 날짜 출력 파라미터 기반으로 출력
```
 null처리 함수  
nvl(arg1, arg2): arg1, arg2 타입은 동일해야 합니다
```
if arg1 is not null return arg1 else return arg2 > arg1이 눌이 아니면 arg1을 리턴 맞으면 arg2리턴
select comm, nvl(comm, 0) from emp;

-nvl2(arg1, arg2, arg3): arg타입은 모두 동일해야 함
if arg1 is not null return arg2 else return arg3 > arg1이 null이 아니면 arg2반환 맞으면 arg3반환 select comm, nvl2(comm, sal+comm, 'no commission') from emp; >error 발생 arg2와 arg3의 타입이 달라서

select comm, nvl2(comm, to_char(sal+comm), 'no commission') from emp;
```
-coalesce(arg1,.....arg255) ; null인지 체크 후 null이 아닌 값을 리턴하고 함수 종료됨 >arg는 모두 동일타입
```
select coalesce(1, null, null, null, null) from dual; >1
select coalesce(1, 2, 3, 4, 5) from dual; >1
select coalesce(null, null, 3, null, null) from dual; >3
select coalesce(null, null, null, null, null, 'a') from dual; >a
```
nullif(arg1, arg2) arg1와 arg2 동일한 값이면 null을 리턴, arg1와 arg2 동일하지 않으면 arg1리턴
```
select nullif('A', 'A'), nullif('A','a') from dual;
```
greatest(exp1,...expN) - 하나 이상의 인수 중에서 가장 큰 값을 반환한다  
least(exp1,...expN) - 인수 expr의 리스트 중에서 가장 작은 값을 반환
```
 select ename, sal, comm, greatest(sal, comm) from emp where comm is not null;

select ename, sal, comm, least(sal, comm) from emp where comm is not null;
```
decode (value, c1, r1, c2, r2, c3, r3,....) : 조건처리 함수  
value 값이 c1과 같으면 r1출력, 그게 아닌 c2와 같으면 r2출력....이런 식
 ```
 문제> emp사원의 담당 업무가 analyst 인 경우 급여는 10% 증가, clerk인 경우 급여는 20% 증가, manager인 경우 30% 증가, president인 경우 40% 증가, saleman인 경우 50% 증가, 그 외엔 기존 급여값으로 나오도록 조회

select empno, ename, sal, job, 
decode(job, 'analyst', sal1.1, 'clerk', sal1.2, 'maneger', sal1.3, 'president', sal1.4, 'saleman', sal*1.5, sal) 변경결과 from emp;
```
SQL 1999표준에서 조건처리 구문이 추가됨  
CASE WHEN 비교조건1 THEN 처리1  
WHEN 비교조건2 THEN 처리2  
:  
WHEN 비교조건N THEN 처리N  
[ELSE 디폴트처리]  
END  
이때 when은 1번만 작성하면 그 뒷줄부터는 생략가능  
```
select empno, ename, sal, job, 
case job when 'analyst' then sal1.1 when 'clerk' then sal1.2 
when 'maneger' then sal1.3 when 'president' then sal1.4 when 'saleman' then sal*1.5 
else sal end salary from emp;

문제> 사원번호, 이름, 급여, 급여의 세금을 출력
급여가 1000이하면 0, 1000이상 2000미만이면 급여의 3%, 2000이상 3000미만이면 급여의 6%, 3000이상 4000미만이면 급여의 9% 급여의 4000이상이면 급여의 12%
select empno, ename, sal, job, 
decode(trunc(sal/1000),0, 0, 1, sal0.03, 2, sal0.06, 3, sal0.09, sal0.12) "Tax" from emp;

SELECT ename, job, sal, case when sal < 1000 THEN 0
when sal < 2000 THEN SAL0.03
when sal < 3000 THEN SAL0.06
when sal < 4000 THEN SAL0.09
ELSE SAL0.12 END tax FROM EMP;
```
복수행 함수 - count(), avg(), sum(), min(), max(), stddev(), variance()

count(*'expression) : 행(row)수 리턴 (null을 카운트 하지 않음)  
count는 모든 컬럼타입에 적용
 ```
 select comm from emp where comm is null;

select count(*), count(deptno), count(distinct deptno), count(comm) from emp where comm is null;
--  *=10 deptno=10 distnict deptno=3 comm=0
```
 avg (number타입컬럼과 표현식): 평균리턴  
sum (number타입컬럼과 표현식): 합 리턴  
min(expression): 최솟값 리턴, 모든 컬럼타입에 적용  
max(expression): 최댓값 리턴, 모든 컬럼타입에 적용  
stddev (number타입과 표현식) : 표준편차리턴  
variance (number타입컬럼과 표현식): 분산리턴  
group함수는 null을 무시한다(null값은 연산에서 제외)  
```
select sum(sal), avg(sal), min(sal), max(sal), variance(sal), stddev(sal) from emp;

-- min, max는 함수의 인수로 전달된 데이터를 정렬한 후 첫번째 값, 마지막 값을 반환
select min(hiredate), max(hiredate) from emp;

select min(ename), max(ename) from emp;

-- 문제> 전체 사원들의 커미션의 평균 조회
select avg(comm), sum(comm)/count(*) from emp;
```
평균을 내는 함수의 값과, 모든값을 센 뒤 합계함수를 이용해 나누는 값이 같지 않은 이유는 comm에 null이 포함되었기 때문.  
comm컬럼에 null이 포함되어 있는 경우, null을 null아닌 값으로 변환 후 함수 적용  
```
select avg(nvl(comm,0)), sum(comm)/count(*) from emp; > null에 0을 적용시킴
```
 테이블의 전체 레코드 집계 수행이 아닌 소그룹별 레코드 집계 수행  
 select~  
from~  
[where ~ ]  
group by 컬럼, 컬럼,....  
[order by~]  
```
select deptno from emp group by deptno;

select deptno, sum(sal), avg(sal) from emp group by deptno;
```
-select절에서 그룹함수를 적용한 컬럼과 그룹함수를 적용하지 않은 컬럼을 사용할 경우  
그룹함수를 적용하지 않은 컬럼 group by절에 반드시 선언해야 합니다(필수조건)  
group by절에 선언된 컬럼은 select절에 선언할 필요는 없다(충분조건)  
```
select deptno, sum(sal), avg(sal) from emp; >error
select sum(sal), avg(sal) from emp group by deptno; --맞는 실행

-- 문제> 부서와 직무로 그룹핑
select sum(sal), avg(sal) from emp group by deptno, job;

select deptno, job, sum(sal), avg(sal) from emp group by deptno, job;

-- 문제> 각 부서별로 인원수, 급여의 평균, 최저 급여, 최고 급여, 급여의 합을 구하여 급여의 합이 내림차순으로 출력
select deptno, sum(deptno), avg(sal), min(sal), max(sal), sum(sal) from emp 
group by deptno order by 2 desc;
```
- 그룹핑하기 전의 조건(필터링) 인지 그룹핑 수행 후의 조건인지 판단  

그룹핑하기 전의 조건(필터링)은 where절에 선언    
그룹핑 수행 후의 조건은 having절에 선언  

select절에서 수행 순서  
select~ ...그룹합수,... 5번  
from~ ---1번  
[where ~ ] ---2번  
[group by 컬럼, 컬럼,.... ] ---3번  
[having 그룹함수를 사용한 조건 선언] ---4번  
[order by~] ----6번  

```
--문제> emp테이블에서 부서 인원이 4명보다 많은 부서의 부서번호, 인원수, 급여의 합을 출력
select deptno, count(deptno), sum(sal) from emp group by deptno having count(deptno)>4;

-- 문제> employees테이블에서 관리자(manager_id)가 없는 사원은 제외하고, 사원들의 부서별(department_id) 평균급여(salary)가 6000미만인 부서번호와 평균급여를 출력
--단 평균급여는 내림차순으로 출력

select department_id, avg(salary) from employees where manager_id is not null group by department_id having avg(salary)<6000 order by avg(salary) desc;
```
그룹함수도 nested 사용 가능(중첩가능)
```
-- 문제> 부서별 급여 평균중에서 최고 평균 급여를 출력

select max(avg(sal)) from emp group by deptno;
```
#### 두 개 이상의 테이블로부터 데이터를 연결해서 결과집합을 선언  
oracle join syntax: where절, =연산자 조인 선언  
sql 1999 표준: from절 join키워드 사용해서 조인 선언  

inner join(equi join)  
non_equi join  
self join  
outer join  
```
--사원이름과 부서번호와 부서이름, 부서위치를 출력
select ename, deptno, dname, loc from emp, dept; --error 컬럼이 명확하지 않아서

select emp.ename, emp.deptno, dept.dname, dept.loc from emp, dept; --56행이나옴 (14rows * 4rows) --조인 조건 누락으로 cartesian product, cross join

select a.ename, a.deptno, b.dname, b.loc from emp a, dept b where a.deptno= b.deptno; --14rows

select a.employee_id, a.last_name, a.department_id, b.department_name from employees a, departments b 
where a.department_id = b.department_id; --106rows

departments.department_id (PK) -not null + unique
employees.department_id (FK) -null허용, 중복값 허용
--사원 테이블에 .department_id 조인 컬럼값이 null인 레코드가 1개 존재
```
조인할 테이블의 동일한 이름의 컬럼을 기준으로 오라클 서버가 자동 조인을 수행하기 때문에   
select문에서 동일이름의 컬럼명 앞에는 소유자를 선언하지 않습니다.  
```
select a.employee_id,, a.last_name, department_id, b.department_name 
from employees a natural join departments b; 
--32rows, manager_id과 department_id 가 일치할 때 조인 수행함

select a.employee_id, a.last_name, department_id, b.department_name 
from employees a inner join departments b using(department_id); --106rows
```
join ~ using(column) 구문을 사용하는 select문에서 동일한 이름의 컬럼명 앞에 소유자 선언하지 않습니다
```
create table emp2 (empno, deptid, ename, sal, job) 
as select empno, deptno, ename, sal, job from emp; --복제테이블 생성(CTAS)

--사원별로 급여와 급여의 등급을 조회결과 생성

select a.empno, a.ename, a.sal, b.grade from emp a, salgrade b 
where a.sal between b.losal and b.hisal; --non.equi join

select a.empno, a.ename, a.sal, b.grade 
from emp a join salgrade b on (a.sal between b.losal and b.hisal); --sql1999문법 non.equi join
```
사원번호, 사원이름, 관리자번호, 관리자 이름 조회결과 생성  
self join - 자기 참조가 가능한 테이블(PK <- FK이 존재)에서만 수행됨
```
select a.empno, a.ename, a.mgr, b.ename from emp a, emp b where a.mgr = b.empno;

select a.empno, a.ename, a.mgr, b.ename from emp a join emp b on a.mgr = b.empno; --sql 1999문법 self join

사원이름(last_name), 부서이름(department_name), 부서위치한 도시(city) 출력
desc employees
desc departments
desc locations
```
n개의 테이블을 조인할 때 최소 n-1개의 조인 조건을 선언합니다
```
select a.last_name, b.department_name, c.city 
from employees a, departments b, locations c 
where a.department_id = b.department_id and c.location_id = b.location_id; --sql1999문법

--부서를 아직 배정받지 못한 사원을 포함해서 사원들의 부서번호와 부서이름을 출력
--조인 컬럼값이 null인 경우 조인되지 못해서 조인 결과에 누락됨
=> 조인 결과를 가져오려면
insert into emp (empno, ename) values (7000, '홍길동'); --행 추가

--equi join은 7000번 사원 레코드 결과에서 누락
select a.ename, a.deptno, b.dname, b.loc from emp a, dept b where a.deptno= b.deptno;

--outer join은 조인 컬럼값이 null인 레코드도 조인 결과로 생성
select a.ename, a.deptno, b.dname, b.loc from emp a, dept b 
where a.deptno= b.deptno(+); > (+) = 아우터연산자

select a.ename, a.deptno, b.dname, b.loc 
from emp a left outer join dept b on a.deptno = b.deptno; --sql1999문법

select b.deptno, b.dname, a.empno, a.ename 
from emp a, dept b where a.deptno= b.deptno; --40번 부서 정보 조인 결과 누락

--40번 부서 정보 조인 결과로 생성하도록 SQL작성
select b.deptno, b.dname, a.empno, a.ename from emp a, dept b 
where a.deptno(+)= b.deptno order by 1 asc;

select b.deptno, b.dname, a.empno, a.ename 
from emp a right outer join dept b on a.deptno= b.deptno order by 1 asc;

--7000번 사원 레코드와 40번 부서 정보 레코드를 모두 조인 결과로 생성
select b.deptno, b.dname, a.empno, a.ename from emp a, dept b 
where a.deptno(+)= b.deptno(+) order by 1 asc; >error outer연산자는 한 쪽만 가능 양쪽 모두엔 사용 불가

select b.deptno, b.dname, a.empno, a.ename 
from emp a full outer join dept b on a.deptno= b.deptno order by 1 asc; >full을 붙이면 두개 모두 아우터 조인을 넣는다는 뜻
```
cross join은 cartesian join으로 수행됨
```
select b.deptno, b.dname, a.empno, a.ename from emp a cross join dept b ;
```
