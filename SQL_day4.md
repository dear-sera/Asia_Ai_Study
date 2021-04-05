### 데이터베이스 객체 - table, view, index, sequence  

####table생성 시 table이름, 컬럼이름, 컬럼size, default 깂, 제약조건 등을 함께 선언 할 수 있다   

제약조건: foreign key, not null, primary key, unique, check  

create table ~ as (subquery) ; => 구조만 복제, 전체와 모든 레코드 복제, 일부 구조와 레코드 복제(not null 제약조건만 복제됨)   

foreign key : 부모테이블의 primary key, unique 제약조건이 선언된 컬럼을 참조   
참조하는 부모테이블의 컬럼값으로만 (child테이블의 fk 선언 컬럼값으로) insert, update 가능   
부모테이블의 (child의 레코드에 의해) 참조되고 있는 row는 (참조하는  자식 row가 존재하므로) 삭제불가   
참조무결성 제약조건

```
create table category(
code number(4),
name varchar2(20)
);

insert into category values(1000, 'Music');
insert into category values(2000, 'Book');
insert into category values(3000, 'Game');
insert into category values(4000, 'Movie');
```

```
create table book(
isbn number(10) primary key,
title varchar2(100),
author varchar2(50),
price number(6),
code number(4) constraint book_fk references category(code) );
```
오류발생 -> 부모테이블(category)

```
alter table category
add constraint category_pk primary key (code);
```
이 코드로 제약조건을 다시 만들어서 create table book을 재실행하면 오류가 안난다
```
select constraint_name, constraint_type, r_owner, r_constraint_name, delete_rule
from user_constraints
where table_name = 'BOOK';
```

```
insert into book values (1, 'oracle', 'hufs', 10000, 2000);
insert into book values (2, 'packman', 'hufs', 3000, 5000);  ---x
insert into book values (3, 'with God', 'hufs', 11000, null); ---null허용

update book
set code = 2001
where isbn = 3; ---x

delete from category where code = 3000;  ---참조하는 child의 레코드가 존재하지 않음
delete from category where code = 2000;  ---참조하는 child의 레코드가 존재하므로 x(에러발생)
```

```
alter table book
modify (code number(4) constraint book_fk foreign key references category(code) on delete cascade)
---부모 테이블의 row가 삭제될 때 자식 row도 함께 삭제
```


```
alter table book
modify (code number(4) constraint book_fk foreign key references category(code) on delete set null)
---부모 테이블의 row가 삭제될 때 자식 row의 컬럼값이 null로 변경됨
```


#### alter table~
컬럼이름 변경, 타입 변경, size 변경, 컬럼 추가, 컬럼 삭제  
제약조건 삭제, 제약조건 추가, 제약조건 확성화/비활성화

alter table ~ add (컬럼정보)  
alter table ~ add column ~  
alter table ~ drop (컬럼이름, ...)  
alter table ~ drop column 컬럼이름  
alter table ~ modify (컬럼이름, ...)  --not null 제약조건 추가, 타입변경, size 변경  
alter table ~ rename column old_name to new_name;  
alter table ~ add constraint ~  
alter table ~ drop constraint ~
alter table ~ enable constraint ~
alter table ~ disable constraint ~


#### drop table ~
레코드 삭제
테이블 메타 정보를 data dictionary(system catalog)로부터 삭제  
제약조건, index는 함께 삭제


#### drop table ~ purge (oracle db에서 recyclebin 기능)
테이블이 rename되어 recyclebin에 저장되고, 물리적으로 disk영역이 남아 있으면 삭제되지 않고 남아있음  

```
conn hr/orale
select tname from tab;  -- select table_name from user_tables;

drop table emp;
desc emp  --조회 결과 없음
select * from emp;  --조회 결과 없음
select tname from tab;  --emp테이블 결과 없음, bin$~ 테이블이 존재(recycle된 테이블의 이름)
```

```
desc recyclebin
select object_name, original_name, operation, type
from recyclebin;
```
emp테이블을 drop시켜서 테이블이 rename되어 bin$~~ 로 recyclebin 됨  
rename된 recyclebin의 object이름으로 조회하면 레코드 결과  확인  


```
flashback table emp to before drop;  --삭제된 테이블 복원 (oracle)
desc emp  
select * from emp;  
select tname from tab;
select object_name, original_name, operation, type
from recyclebin;
```
 flashback을 하면 테이블이 복원됨, 다시 코드를 입력해서 돌아왔는 지 확인

#### view - 논리적 테이블, table에 대한 window역할
select문(subquery)이 definition 보안(데이터 제한), 간결한 sql문 사용이 목적   
간접적으로 테이블에 access 함   



create (or replace) view 이름  
as select ~
from ~  
(where ~~~  );  

```
create or replace view emp20vu
as select empno, ename, sal, job, deptno
from emp
where deptno = 20;

desc emp20vu;  --뷰의 구조 조회
select * from emp20vu; --뷰의 데이터 조회

select object_name, object_type from user_objects;
select view_name, text
from user_views           ---뷰의 메타 정보 조회
where view_name = 'EMP20VU';

create  or replace  view emp20vu 
as select empno, ename, sal*12, job, deptno
   from emp
   where deptno = 20;  --? error

create or replace view emp20vu (empno, ename, sal, job, deptno)
as select empno, ename, sal*12, job, deptno
from emp
where deptno = 20;

create or replace view emp20vu
as select empno, ename, sal, job, deptno
from emp
where deptno = 20 with check option;
```
view를 통해서 간접적이지만 base가 되는 테이블에 insert, update, delete가능 => simple view

```
select * from emp20vu;

insert into emp20vu
values (9007, 'jeju', 5000, 'IT', 20);
select * from emp;  --base가 되는 데이블에서도 조회됨
select * from emp20vu;  --조회결과 확인


insert into emp20vu
values (9001, 'jeju', 5000, 'IT', 30);   --error(체크 제약조건 위배 -부서가 30번은 못들어옴)
select * from emp;

select constraint_name, constraint_type
from user_constraints
where table_name = 'EMP20VU';  --view에 대한 제약조건 정보 확인

create or replace view emp20vu
as select empno, ename, sal, job, deptno
from emp
where deptno = 20 with read only;  --읽기전용 뷰 제약조건

insert into emp20vu
values (9100, 'seoul', 3500, 'IT', 20);  --error 읽기전용 뷰여서


select object_name, object_type from user_objects
where object_type='VIEW';


drop view emp20vu;  -view삭제

select object_name, object_type from user_objects
where object_type='VIEW';   

```
quiz> view 삭제는 table에 영향?  
emp20vu를 삭제하면 emp테이블은 삭제되지 않습니다.  
view의 meta data만 data dictionary에서 삭제됩니다.   

```
create  or replace view emp20vu 
as select empno, ename, sal, job, deptno
   from emp
   where deptno = 20;

select * from emp20vu;
drop table emp;
select * from emp20vu;

select object_name, object_type, status from user_objects
where object_type='VIEW';
```

emp테이블을 삭제하면 emp20vu는 삭제되지 않고 invalid




