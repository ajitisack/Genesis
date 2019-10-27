drop view if exists equity;
create view equity as
select
  A.seccd
, B.secid
, B.secnm
, B.secgrp
, B.faceval
, B.isin
, B.industry
, A.dt
, A.open
, A.high
, A.low
, A.close
, A.adjclose
, A.vol
, A.year
, A.month
, A.day
, A.wkday
, A.wknr
, A.qrtr
, A.freq
from (
	select *, 'd' freq from equitydly union
	select *, 'w' freq from equitywly union
	select *, 'm' freq from equitymly
) A inner join security B on A.seccd  = B.seccd
