
drop view if exists nselive_equity;
create view nselive_equity as
    select
      b.name
    , a.symbol
    , case when change > 0 then 'Up' else 'Down' end trend
    , changepct, change
    , close ltp, open, low, high, volume, timestamp, a.runts
    from NSE_EquityCurrentPrice a
        join EquitySymbols b on a.symbol = b.symbol and b.innse = 1
;

drop view if exists nselive_niftybank;
create view nselive_niftybank as
    select
      a.runts
    , case when c.symbol is null then 0 else 1 end innifty50
    , b.name
    , a.symbol
    , case when change > 0 then 'Up' else 'Down' end trend
    , changepct, change
    , close ltp, open, low, high, volume, timestamp
    from NSE_EquityCurrentPrice a
        join EquitySymbols b on a.symbol = b.symbol and b.innse = 1
        left outer join nseindices c on a.symbol = c.symbol and c.indexname = 'Nifty 50'
        left outer join nseindices d on a.symbol = d.symbol
    where 1 = 1
        and d.indexname = 'Nifty Bank'
;

drop view if exists nselive_niftyauto;
create view nselive_niftyauto as
    select
      a.runts
    , case when c.symbol is null then 0 else 1 end innifty50
    , b.name
    , a.symbol
    , case when change > 0 then 'Up' else 'Down' end trend
    , changepct, change
    , close ltp, open, low, high, volume, timestamp
    from NSE_EquityCurrentPrice a
        join EquitySymbols b on a.symbol = b.symbol and b.innse = 1
        left outer join nseindices c on a.symbol = c.symbol and c.indexname = 'Nifty 50'
        left outer join nseindices d on a.symbol = d.symbol
    where 1 = 1
        and d.indexname = 'Nifty Auto'
;


drop view if exists nselive_niftyfinserv;
create view nselive_niftyfinserv as
    select
      a.runts
    , case when c.symbol is null then 0 else 1 end innifty50
    , b.name
    , a.symbol
    , case when change > 0 then 'Up' else 'Down' end trend
    , changepct, change
    , close ltp, open, low, high, volume, timestamp
    from NSE_EquityCurrentPrice a
        join EquitySymbols b on a.symbol = b.symbol and b.innse = 1
        left outer join nseindices c on a.symbol = c.symbol and c.indexname = 'Nifty 50'
        left outer join nseindices d on a.symbol = d.symbol
    where 1 = 1
        and d.indexname = 'Nifty Financial Services'
;


drop view if exists nselive_niftyfmcg;
create view nselive_niftyfmcg as
    select
      a.runts
    , case when c.symbol is null then 0 else 1 end innifty50
    , b.name
    , a.symbol
    , case when change > 0 then 'Up' else 'Down' end trend
    , changepct, change
    , close ltp, open, low, high, volume, timestamp
    from NSE_EquityCurrentPrice a
        join EquitySymbols b on a.symbol = b.symbol and b.innse = 1
        left outer join nseindices c on a.symbol = c.symbol and c.indexname = 'Nifty 50'
        left outer join nseindices d on a.symbol = d.symbol
    where 1 = 1
        and d.indexname = 'Nifty FMCG'
;


drop view if exists nselive_niftyit;
create view nselive_niftyit as
    select
      a.runts
    , case when c.symbol is null then 0 else 1 end innifty50
    , b.name
    , a.symbol
    , case when change > 0 then 'Up' else 'Down' end trend
    , changepct, change
    , close ltp, open, low, high, volume, timestamp
    from NSE_EquityCurrentPrice a
        join EquitySymbols b on a.symbol = b.symbol and b.innse = 1
        left outer join nseindices c on a.symbol = c.symbol and c.indexname = 'Nifty 50'
        left outer join nseindices d on a.symbol = d.symbol
    where 1 = 1
        and d.indexname = 'Nifty IT'
;


drop view if exists nselive_niftypharma;
create view nselive_niftypharma as
    select
      a.runts
    , case when c.symbol is null then 0 else 1 end innifty50
    , b.name
    , a.symbol
    , case when change > 0 then 'Up' else 'Down' end trend
    , changepct, change
    , close ltp, open, low, high, volume, timestamp
    from NSE_EquityCurrentPrice a
        join EquitySymbols b on a.symbol = b.symbol and b.innse = 1
        left outer join nseindices c on a.symbol = c.symbol and c.indexname = 'Nifty 50'
        left outer join nseindices d on a.symbol = d.symbol
    where 1 = 1
        and d.indexname = 'Nifty Pharma'
;


drop view if exists nselive_indices_nifty;
create view nselive_indices_nifty as
    select
      a.runts
    , a.indexname as name
    , case when change > 0 then 'Up' else 'Down' end trend
    , changepct, change
    , close ltp, open, low, high, timestamp
    from NSE_IndicesCurrentPrice a
        join (select distinct indexname from NSE_Indices where indextype = 'MarketCap') b on a.indexname = b.indexname
;


drop view if exists nselive_indices_sector;
create view nselive_indices_sector as
    select
      a.runts
    , a.indexname as name
    , case when change > 0 then 'Up' else 'Down' end trend
    , changepct, change
    , close ltp, open, low, high, timestamp
    from NSE_IndicesCurrentPrice a
        join (select distinct indexname from NSE_Indices where indextype = 'Sector') b on a.indexname = b.indexname
;

drop view if exists nselive_indices_thematics;
create view nselive_indices_thematics as
    select
      a.runts
    , a.indexname as name
    , case when change > 0 then 'Up' else 'Down' end trend
    , changepct, change
    , close ltp, open, low, high, timestamp
    from NSE_IndicesCurrentPrice a
        join (select distinct indexname from NSE_Indices where indextype = 'Thematic') b on a.indexname = b.indexname
;

drop view if exists nselive_eqintraday;
create view nselive_eqintraday as
    select *
    from NSE_EquityIntradayPrices
    where 1 = 1
;