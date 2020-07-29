drop view if exists nsecurrent;
create view nsecurrent as
    select timestamp, 'equity' type, b.name || '(' || a.symbol || ')' as name, open, low, high, close, volume, change, changepct, runts
    from nsecurrentpriceequity a
        join symbols b on a.symbol = b.symbol
    union all
    select timestamp, indextype type, a.indexname as name, open, low, high, close, volume, change, changepct, runts
    from nsecurrentpriceindices a
        join (select distinct lower(indextype) || '_index' as indextype, indexname from nseindices) b on a.indexname = b.indexname
;

drop view if exists nseintradayhist;
create view nseintradayhist as
    select * from nseintraday_202005 union all
    select * from nseintraday_202006 union all
    select * from nseintraday_202007
;
