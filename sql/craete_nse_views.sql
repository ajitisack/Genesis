drop view if exists nseeq_symbols;
create view nseeq_symbols as
    select 
      a.isin
    , a.symbol
    , case when b.symbol is null then 0 else 1 end infno
    , case when c.symbol is null then 0 else 1 end innifty50
    , a.name
    , a.facevalue
    , a.series
    , a.dateoflisting
    , a.paidupvalue
    , a.marketlot
    , a.runts
    from NSE_EquitySymbols a
        left outer join NSE_EquityFNOCurrentPrice b on a.symbol = b.symbol
        left outer join NSE_Indices c on a.symbol = c.symbol and c.indexname = 'Nifty 50'
    where 1 = 1
;

drop view if exists nseeq_indices;
create view nseeq_indices as
    select *
    from NSE_Indices
;

drop view if exists nseeq_histprice;
create view nseeq_histprice as
    select *
    from NSE_EquityHistoricalPrices
    where 1 = 1
;

drop view if exists nseeq_profile_mc;
create view nseeq_profile_mc as
    select *
    from NSE_EquityProfileMoneyControl
    where 1 = 1
;

drop view if exists nseeq_profile_yf;
create view nseeq_profile_yf as
    select *
    from NSE_EquityProfileYahooFinance
    where 1 = 1
;


drop view if exists nseeq_summary;
create view nseeq_summary as
    select
      date
    , case when b.symbol is null then 0 else 1 end innifty50
    , case when c.symbol is null then 0 else 1 end innifty100
    , e.innsefo
    , e.name
    , a.symbol
    , openingtype, openinggap
    , closingtype, closinggap
    , close ltp, prevclose, open, pricechange, pricechangepct
    , low, high
    , pricevolumeratio
    , volume, prevvolume, volumechange, volumechangepct
    , a.runts
    from NSE_EquitySummary a
        join nseeq_symbols e on a.symbol = e.symbol
        left outer join nseeq_indices b on a.symbol = b.symbol and b.indexname = 'Nifty 50'
        left outer join nseeq_indices c on a.symbol = c.symbol and c.indexname = 'Nifty 100'
    where 1 = 1
;

drop view if exists nseeq_pivotpoints;
create view nseeq_pivotpoints as
    select
      date
    , case when b.symbol is null then 0 else 1 end innifty50
    , case when c.symbol is null then 0 else 1 end innifty100
    , e.innsefo
    , e.name
    , a.symbol
    , close ltp
    , r3
    , r2
    , r1
    , pp
    , s1
    , s2
    , s3
    , a.runts
    from NSE_EquitySummary a
        join nseeq_symbols e on a.symbol = e.symbol
        left outer join nseeq_indices b on a.symbol = b.symbol and b.indexname = 'Nifty 50'
        left outer join nseeq_indices c on a.symbol = c.symbol and c.indexname = 'Nifty 100'
    where 1 = 1
;


drop view if exists nseeq_narrowrange;
create view nseeq_narrowrange as
    select
      date
    , case when b.symbol is null then 0 else 1 end innifty50
    , case when c.symbol is null then 0 else 1 end innifty100
    , e.innsefo
    , e.name
    , a.symbol
    , close ltp
    , NR4
    , NR7
    , NR9
    , lowerhigh lowerhighthanprevious
    , higherlow higherlowthanprevious
    , tr
    , tr1d
    , tr2d
    , tr3d
    , tr4d
    , tr5d
    , tr6d
    , tr7d
    , tr8d
    , a.runts
    from NSE_EquitySummary a
        join nseeq_symbols e on a.symbol = e.symbol
        left outer join nseeq_indices b on a.symbol = b.symbol and b.indexname = 'Nifty 50'
        left outer join nseeq_indices c on a.symbol = c.symbol and c.indexname = 'Nifty 100'
    where 1 = 1
;

drop view if exists nseeq_preopen;
create view nseeq_preopen as
    select time, b.name, a.symbol, b.innsefo
         , case when d.symbol is null then 0 else 1 end innifty50
         , openingtype, prevclose, open, pricechange, pricechangepct, volume, yearlow, yearhigh, sellqty, buyqty, a.runts
    from NSE_EquityMarketPreOpen a
        join nseeq_symbols b on a.symbol = b.symbol
        left outer join nseeq_indices d on a.symbol = d.symbol and d.indexname = 'Nifty 50'
    where 1 = 1
;

drop view if exists nseeq_intraday_hist;
create view nseeq_intraday_hist as
    select * from NSE_EquityIntradayPrices_202005 union all
    select * from NSE_EquityIntradayPrices_202006 union all
    select * from NSE_EquityIntradayPrices_202007
;


