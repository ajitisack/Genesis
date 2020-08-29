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

drop view if exists nseeq_intraday_hist;
create view nseeq_intraday_hist as
    select * from NSE_EquityIntradayPrices_202005 union all
    select * from NSE_EquityIntradayPrices_202006 union all
    select * from NSE_EquityIntradayPrices_202007 union all
    select * from NSE_EquityIntradayPrices_202008
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
    , b.innifty50
    , b.infno
    , b.name
    , a.symbol
    , openingtype, openinggap
    , closingtype, closinggap
    , close ltp, prevclose, open, pricechange, pricechangepct
    , low, high
    , pricevolumeratio
    , volume, prevvolume, volumechange, volumechangepct
    , cpr
    , NR4
    , NR7
    , NR9
    , lowerhigh lowerhighthanprevious
    , higherlow higherlowthanprevious
    , r3
    , r2
    , r1
    , bc
    , pp
    , tc
    , s1
    , s2
    , s3
    , a.runts
    from NSE_EquitySummary a
        join nseeq_symbols b on a.symbol = b.symbol
    where 1 = 1
;

drop view if exists nseeq_pivotpoints;
create view nseeq_pivotpoints as
    select
      date
    , b.innifty50
    , b.infno
    , b.name
    , a.symbol
    , close ltp
    , r3
    , r2
    , r1
    , bc
    , pp
    , tc
    , cpr
    , s1
    , s2
    , s3
    , a.runts
    from NSE_EquitySummary a
        join nseeq_symbols b on a.symbol = b.symbol
    where 1 = 1
;


drop view if exists nseeq_narrowrange;
create view nseeq_narrowrange as
    select
      date
    , b.innifty50
    , b.infno
    , b.name
    , b.symbol
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
        join nseeq_symbols b on a.symbol = b.symbol
    where 1 = 1
;

drop view if exists nseeq_preopen;
create view nseeq_preopen as
    select 
       time
     , b.name
     , a.symbol
     , b.innifty50
     , b.infno
     , a.openingtype
     , a.prevclose
     , a.open
     , a.pricechange
     , a.pricechangepct
     , a.volume
     , r3
     , r2
     , r1
     , bc
     , pp
     , tc
     , cpr
     , s1
     , s2
     , s3
     , NR4
     , NR7
     , NR9
     , lowerhigh lowerhighthanprevious
     , higherlow higherlowthanprevious
     , yearlow
     , yearhigh
     , sellqty
     , buyqty
     , a.runts
    from NSE_EquityMarketPreOpen a
        join nseeq_symbols b on a.symbol = b.symbol
        join NSE_EquitySummary c on a.symbol = c.symbol
    where 1 = 1
    order by 10 desc
;


drop view if exists nseeq_fnopreopen;
create view nseeq_fnopreopen as
    select 
       time
     , b.name
     , a.symbol
     , b.innifty50
     , a.openingtype
     , a.prevclose
     , a.open
     , a.pricechange
     , a.pricechangepct
     , a.volume
     , r3
     , r2
     , r1
     , bc
     , pp
     , tc
     , cpr
     , s1
     , s2
     , s3
     , NR4
     , NR7
     , NR9
     , lowerhigh lowerhighthanprevious
     , higherlow higherlowthanprevious
     , yearlow
     , yearhigh
     , sellqty
     , buyqty
     , a.runts
    from NSE_EquityMarketPreOpen a
        join nseeq_symbols b on a.symbol = b.symbol
        join NSE_EquitySummary c on a.symbol = c.symbol
    where 1 = 1
    and infno = 1
    order by a.pricechangepct desc
;


drop view if exists nseeq_fnocurrent;
create view nseeq_fnocurrent as
    select
      a.time
    , b.name
    , a.symbol
    , case when a.pricechange > 0 then 'Up' else 'Down' end trend
    , a.pricechange
    , a.pricechangepct
    , a.lastprice ltp
    , a.open
    , a.low
    , a.high
    , a.volume
    , r3
    , r2
    , r1
    , bc
    , pp
    , tc
    , cpr
    , s1
    , s2
    , s3
    , NR4
    , NR7
    , NR9
    , lowerhigh lowerhighthanprevious
    , higherlow higherlowthanprevious
    , a.runts
    from NSE_EquityFNOCurrentPrice a
        join NSE_EquitySymbols b on a.symbol = b.symbol
        join NSE_EquitySummary c on a.symbol = c.symbol
    order by a.pricechangepct desc
;




