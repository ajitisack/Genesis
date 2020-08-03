drop view if exists nseeqsymbols;
create view nseeqsymbols as
    select isin, symbol, innsefo, name, industry, facevalue, [group] grp, series, dateoflisting, paidupvalue, marketlot, runts
    from EquitySymbols
    where innse=1
;

drop view if exists nseeqsummary;
create view nseeqsummary as
    select a.*
    , case when b.symbol is null then 0 else 1 end innifty50
    , case when c.symbol is null then 0 else 1 end innifty100
    , e.innsefo
    from NSE_EquitySummary a
        join nseeqsymbols e on a.symbol = e.symbol
        left outer join nseindices b on a.symbol = b.symbol and b.indexname = 'Nifty 50'
        left outer join nseindices c on a.symbol = c.symbol and c.indexname = 'Nifty 100'
        --left outer join nseindices d on a.symbol = d.symbol and d.indextype = 'Sector'
    where 1 = 1
;

drop view if exists nseeqpreopen;
create view nseeqpreopen as
    select time, b.name, a.symbol, c.indexname sectorindex, b.innsefo
         , case when d.symbol is null then 0 else 1 end innifty50
         , openingtype, prevclose, open, pricechange, pricechangepct, volume, yearlow, yearhigh, sellqty, buyqty, a.runts
    from NSE_EquityMarketPreOpen a
        join nseeqsymbols b on a.symbol = b.symbol
        left outer join nseindices c on a.symbol = c.symbol and c.indextype = 'Sector'
        left outer join nseindices d on a.symbol = d.symbol and d.indexname = 'Nifty 50'
    where 1 = 1
;

drop view if exists nselive_equity;
create view nselive_equity as
    select timestamp, a.symbol, c.indexname sectorindex
    , case when d.symbol is null then 0 else 1 end innifty50
--    , case when e.symbol is null then 0 else 1 end innifty100
    , b.name, open, low, high, close, volume, change, changepct, a.runts
    from NSE_EquityCurrentPrice a
        join EquitySymbols b on a.symbol = b.symbol and b.innse = 1
        left outer join nseindices c on a.symbol = c.symbol and c.indextype = 'Sector'
        left outer join nseindices d on a.symbol = d.symbol and d.indexname = 'Nifty 50'
--        left outer join nseindices e on a.symbol = e.symbol and e.indexname = 'Nifty 100'
;

drop view if exists nselive_nifty;
create view nselive_nifty as
    select timestamp, a.indexname as name, open, low, high, close, change, changepct, a.runts
    from NSE_IndicesCurrentPrice a
    where 1 = 1
        and indexname in ('Nifty 50', 'Nifty 100', 'Nifty 200', 'Nifty 500')
;

drop view if exists nselive_sectors;
create view nselive_sectors as
    select timestamp, a.indexname as name, open, low, high, close, change, changepct, a.runts
    from NSE_IndicesCurrentPrice a
        join (select distinct indexname from NSE_Indices where indextype = 'Sector') b on a.indexname = b.indexname
;

drop view if exists nselive_niftyindices;
create view nselive_niftyindices as
    select timestamp, a.indexname as name, open, low, high, close, change, changepct, a.runts
    from NSE_IndicesCurrentPrice a
        join (select distinct indexname from NSE_Indices where indextype = 'MarketCap') b on a.indexname = b.indexname
;

drop view if exists nselive_thematics;
create view nselive_thematics as
    select timestamp, a.indexname as name, open, low, high, close, change, changepct, a.runts
    from NSE_IndicesCurrentPrice a
        join (select distinct indexname from NSE_Indices where indextype = 'Thematic') b on a.indexname = b.indexname
;

drop view if exists nselive_eqintraday;
create view nselive_eqintraday as
    select *
    from NSE_EquityIntradayPrices
    where 1 = 1
;

drop view if exists nseintradayhist;
create view nseintradayhist as
    select * from nseintraday_202005 union all
    select * from nseintraday_202006 union all
    select * from nseintraday_202007
;

drop view if exists nseeqhistprice;
create view nseeqhistprice as
    select *
    from NSE_EquityHistoricalPrices
    where 1 = 1
;

drop view if exists nseindices;
create view nseindices as
    select *
    from NSE_Indices
;

drop view if exists nseeqprofilemc;
create view nseeqprofilemc as
    select *
    from NSE_EquityProfileMoneyControl
    where 1 = 1
;

drop view if exists nseeqprofileyf;
create view nseeqprofileyf as
    select *
    from NSE_EquityProfileYahooFinance
    where 1 = 1
;
