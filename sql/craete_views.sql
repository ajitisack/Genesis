drop view if exists symbols;
create view symbols as
    select 
      a.isin
    , a.symbol
    , case when d.symbol is null then 0 else 1 end inhotlist
    , case when b.symbol is null then 0 else 1 end infno
    , case when c.symbol is null then 0 else 1 end innifty50
    , a.name
    , d.sector
    , a.facevalue
    , a.series
    , a.dateoflisting
    , a.paidupvalue
    , a.marketlot
    , a.runts
    from NSE_EquitySymbols a
        left outer join NSE_EquityFNOCurrentPrice b on a.symbol = b.symbol
        left outer join NSE_Indices c on a.symbol = c.symbol and c.indexname = 'Nifty 50'
        left outer join NSE_Watchlist d on a.symbol = d.symbol 
    where 1 = 1
;

drop view if exists indices;
create view indices as
    select *
    from NSE_Indices
;

drop view if exists histprice;
create view histprice as
    select *
    from NSE_EquityHistoricalPrices
    where 1 = 1
;


/*drop view if exists intradayhist;
create view intradayhist as
    select * from NSE_EquityIntradayPrices_202005 union all
    select * from NSE_EquityIntradayPrices_202006 union all
    select * from NSE_EquityIntradayPrices_202007 union all
    select * from NSE_EquityIntradayPrices_202008
;*/

drop view if exists profilemc;
create view profilemc as
    select *
    from NSE_EquityProfileMoneyControl
    where 1 = 1
;

drop view if exists profileyf;
create view profileyf as
    select *
    from NSE_EquityProfileYahooFinance
    where 1 = 1
;


drop view if exists technicals;
create view technicals as
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
    , a.runts
    from NSE_EquityTechnicals a
        join symbols b on a.symbol = b.symbol
    where 1 = 1
;


drop view if exists narrowrange;
create view narrowrange as
    select
      date
    , b.innifty50
    , b.infno
    , b.inhotlist
    , b.name
    , b.sector
    , b.symbol
    , close ltp
    , case when NR4 = 0 then '' else 'X' end NR4
    , case when NR7 = 0 then '' else 'X' end NR7
    , case when NR9 = 0 then '' else 'X' end NR9
    , case when lowerhigh = 0 then '' else 'X' end lowerhigh
    , case when higherlow = 0 then '' else 'X' end higherlow
    , tr, tr1d, tr2d, tr3d, tr4d, tr5d, tr6d, tr7d, tr8d
    , a.runts
    from NSE_EquityTechnicals a
        join symbols b on a.symbol = b.symbol
    where 1 = 1
;

drop view if exists preopen;
create view preopen as
    select 
--     , b.name
       b.sector
     , a.symbol
     , a.openingtype
--     , a.prevclose
     , a.open
--     , a.pricechange
     , (a.pricechangepct/100) changepct
    , r3, r2, r1, bc, pp, tc, cpr
    , (cpr/a.lastprice)/100 cpr_pct
    , s1, s2, s3
     , yearlow
     , yearhigh
     , b.inhotlist
     , b.innifty50
     , b.infno
     , time
     , a.runts
    from NSE_EquityMarketPreOpen a
        join symbols b on a.symbol = b.symbol
        left outer join NSE_EquityTechnicals c on a.symbol = c.symbol
    where 1 = 1
    order by sector, changepct desc
;

drop view if exists currentprice;
create view currentprice as
    select
      a.time
--    , b.name
    , b.sector
    , a.symbol
    , case when a.prevclose > a.open then 'Gap-Up' when a.prevclose < a.open then 'Gap-Down' else 'No-Gap' end openingtype
    , case when a.lastprice >= a.open then 'Up'else 'Down' end trend
--    , a.pricechange
    , a.open, a.low, a.high, a.volume
    , a.lastprice ltp
    , (a.pricechangepct/100) changepct
    , r3, r2, r1, bc, pp, tc, cpr
    , (cpr/a.lastprice)/100 cpr_pct
    , s1, s2, s3
    , case when a.open = a.low then 'X' else '' end 'openislow'
    , case when a.open = a.high then 'X' else '' end 'openishigh'
    , b.inhotlist
    , b.innifty50
    , b.infno
    , a.runts
    from NSE_EquityFNOCurrentPrice a
        join symbols b on a.symbol = b.symbol
        left outer join NSE_EquityTechnicals c on a.symbol = c.symbol
    order by changepct desc
;



