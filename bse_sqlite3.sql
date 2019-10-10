create table equity(
  dt varchar(10)
, seccd int
, secgrp varchar(10)
, sectp varchar(10)
, open decimal(19,2)
, high decimal(19,2)
, low decimal(19,2)
, close decimal(19,2)
, last decimal(19,2)
, prevclose decimal(19,2)
, trds bigint
, shrs bigint
, trnovr decimal(19,2)
);

.mode csv equity
.import a.csv equity




drop table if exists security;
create table security (
  seccd varchar(100)
, secid varchar(100)
, secnm varchar(100)
, secstatus varchar(2)
, secgrp varchar(2)
, faceval decimal(10,2)
, isin varchar(100)
, industry varchar(100)
);

cat ListOfScrips.csv | sed 's/,.[^,]*$//g; s/&amp;/\&/g; 1d; s/ *,/,/g' > bse_securities.csv

.mode csv security
.import bse_securities.csv security

create index if not exists index_seccd on security(seccd);

create view equity_h as
select A.*, B.secid, B.secnm, B.secstatus, B.industry
from (
select * from eq_2010
union
select * from eq_2011
union
select * from eq_2012
union
select * from eq_2013
union
select * from eq_2014
union
select * from eq_2015
union
select * from eq_2016
) A left outer join security B on A.seccd = B.seccd

create view equity_3y as
select A.*, B.secid, B.secnm, B.secstatus, B.industry
from (
select * from eq_2017
union
select * from eq_2018
union
select * from eq_2019
) A left outer join security B on A.seccd = B.seccd
