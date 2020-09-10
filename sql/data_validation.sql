drop table if exists temp.allsymbols;
drop table if exists temp.fnosymbols;
drop table if exists temp.prices;
create table temp.allsymbols as select distinct symbol from symbols;
create table temp.fnosymbols as select distinct symbol from symbols where infno = 1;
create table temp.prices as select distinct symbol from histprice;


select * 
from temp.fnosymbols a
    left outer join temp.prices b on a.symbol = b.symbol
where b.symbol is null;


select * 
from temp.allsymbols a
    left outer join temp.prices b on a.symbol = b.symbol
where b.symbol is null;



select *
from histprice where symbol = 'KALYANI'
order by date desc;

select *
from symbols
where symbol = 'KALYANI';


select date, symbol, open, low, high, close, round(high-low, 2) tr from histprice where date in (
select distinct date from histprice where date <= (select date()) order by 1 desc limit 9)
and symbol = 'HDFCBANK';

