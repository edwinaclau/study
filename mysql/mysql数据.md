TINYINT


SMALLINT



MEDIUMINT


INT INTEGER


BIGINT





create table t1(id1 int, id2 int(5));

insert  into t1 values(1,1);

altert table t1 modify id1 int zero fill;


zerofil就是用0填充


如果输入大于int(5)在id2


整数类型都有一个可选属性(UNSIGNED)


AUTO_INCREMENT



CREATE TABLE 't1' {

   'id1' float(5,2) default NULL,
   'id2' double(5,2) default NULL,
   'id3' decimal(5,2) default NULL
}


insert into t1 (1.23,1.23,1.23);

select * from t1;

1.23 1.23 1.23


insert toto t1 values(1.234,1.234,1.23);
