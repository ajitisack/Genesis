/*****************************/
/***   VIEW FOR SYMBOLS    ***/
/*****************************/

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

/*
drop view if exists profilemc;
create view profilemc as
    select *
    from NSE_EquityProfileMoneyControl
    where 1 = 1
;
*/

/*
drop view if exists profileyf;
create view profileyf as
    select *
    from NSE_EquityProfileYahooFinance
    where 1 = 1
;
*/


/*drop view if exists intradayhist;
create view intradayhist as
    select * from NSE_EquityIntradayPrices_202005 union all
    select * from NSE_EquityIntradayPrices_202006 union all
    select * from NSE_EquityIntradayPrices_202007 union all
    select * from NSE_EquityIntradayPrices_202008
;*/

/********************************/
/***   VIEW FOR TECHNICALS    ***/
/********************************/

drop view if exists technicals;
create view technicals as
    select
      date
    , b.innifty50
    , b.inhotlist
    , b.infno
    , b.sector
    , b.name
    , a.symbol
    , openingtype, openinggap, openinggappct
    , closingtype, closinggap, closinggappct 
    , close, prevclose, open, pricechange change, pricechangepct changepct
    , low, high, prevlow, prevhigh
    , round(cast(totalvalue/1000000 as REAL),2) totaltradevalue
    , round(cast(volume as REAL)/1000000, 2) volume
    , round(cast(prevvolume as REAL)/1000000, 2) prevvolume
    , volumechange, volumechangepct
    , tr/close trratio
    , cpr0 cprtoday
    , (cpr0/prevclose) cprwidthtoday
    , r30, r20, r10, tc0, pp0, bc0, s10, s20, s30
    , cpr cprtomorrow
    , (cpr/close) cprwidthtomorrow
    , r3, r2, r1, tc, pp, bc, s1, s2, s3
    , case when NR4 = 0 then '' else 'X' end NR4
    , case when NR7 = 0 then '' else 'X' end NR7
    , case when NR9 = 0 then '' else 'X' end NR9
    , case when lowerhigh = 0 then '' else 'X' end lowerhigh
    , case when higherlow = 0 then '' else 'X' end higherlow
    , tr, tr1d, tr2d, tr3d, tr4d, tr5d, tr6d, tr7d, tr8d
    , case when a.open = a.low then 'X' else '' end 'openislow'
    , case when a.open = a.high then 'X' else '' end 'openishigh'
    , a.runts
    from NSE_EquityTechnicals a
        join symbols b on a.symbol = b.symbol
    where 1 = 1
;


/********************************/
/***    VIEW FOR PRE-OPEN     ***/
/********************************/

drop view if exists preopen;
create view preopen as
    select 
       b.sector
     , a.symbol
     , a.openingtype
     , a.prevclose
     , a.open
--     , a.pricechange
     , (a.pricechangepct/100) changepct
     , a.volume
     , a.volume * a.open value
     , c.cpr
     , (c.cpr/a.open) cpr_pct
     , case  when a.open > R3  then 'Above R3'
             when a.open < r3  and  a.open > r2 then 'Above R2'
             when a.open = r2  then 'On R2'
             when a.open < r2  and  a.open >= r1 then 'Above R1'
             when a.open = r1  then 'On R1'
             when a.open > tc  then 'Below R1; Above CPR'
             when a.open <= tc and  a.open >= bc then 'Within CPR'           
             when a.open > s1  then 'Above S1; Below CPR'
             when a.open = s1  then 'On S1'             
             when a.open > s2  and  a.open < s1 then 'Above S2'
             when a.open = s2  then 'On S2'
             when a.open > s3  and  a.open < s2 then 'Above S3'
             when a.open = s2  then 'On S3'
             else 'Below S3' end openstatus
     , case when NR4 = 0 then '' else 'X' end NR4
     , case when NR7 = 0 then '' else 'X' end NR7
     , case when NR9 = 0 then '' else 'X' end NR9
     , yearlow
     , yearhigh
     , c.low as prevlow
     , c.high as prevhigh
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


/***********************************/
/***    VIEW FOR CURRENT PRICE   ***/
/***********************************/

drop view if exists currentprice;
create view currentprice as
    select
--      a.time
--    , b.name
      strftime('%H:%S', a.time) time
    , b.sector
    , a.symbol
--    , case when a.open > a.prevclose then 'Gap-Up' when a.prevclose < a.open then 'Gap-Down' else 'No-Gap' end openingtype
    , a.prevclose
    , (d.pricechangepct/100) openchangepct
    , case when a.lastprice >= a.open then 'Up'else 'Down' end trend
--    , a.pricechange
    , a.open, a.low, a.high
    , round(cast(a.volume as REAL)/10000000, 2) volume
    , round((cast(a.volume as REAL) * (a.open + a.low + a.high + a.lastprice)/4)/1000000, 2) value
    , a.lastprice ltp
    , (a.lastprice-a.open)/a.open ltptoopenchangepct
    , (a.pricechangepct/100) changepct
    , cpr, (cpr/a.lastprice) cpr_pct
    , case   when a.lastprice > R3  then 'Above R3'
             when a.lastprice < r3  and  a.lastprice > r2 then 'Above R2'
             when a.lastprice = r2  then 'On R2'
             when a.lastprice < r2  and  a.lastprice >= r1 then 'Above R1'
             when a.lastprice = r1  then 'On R1'
             when a.lastprice > tc  then 'Below R1; Above CPR'
             when a.lastprice <= tc and  a.lastprice >= bc then 'Within CPR'           
             when a.lastprice > s1  then 'Above S1; Below CPR'
             when a.lastprice = s1  then 'On S1'             
             when a.lastprice > s2  and  a.lastprice < s1 then 'Above S2'
             when a.lastprice = s2  then 'On S2'
             when a.lastprice > s3  and  a.lastprice < s2 then 'Above S3'
             when a.lastprice = s2  then 'On S3'
             else 'Below S3' end pricestatus
    , c.low as prevlow
    , c.high as prevhigh
    , case when a.open = a.low then 'X' else '' end 'openislow'
    , case when a.open = a.high then 'X' else '' end 'openishigh'
    , case when NR4 = 0 then '' else 'X' end NR4
    , case when NR7 = 0 then '' else 'X' end NR7
    , case when NR9 = 0 then '' else 'X' end NR9
    , b.inhotlist
    , b.innifty50
    , b.infno
    , a.runts
    from NSE_EquityFNOCurrentPrice a
        join symbols b on a.symbol = b.symbol
        left outer join NSE_EquityTechnicals c on a.symbol = c.symbol
        left outer join NSE_EquityMarketPreOpen d on a.symbol = d.symbol
    order by changepct desc
;



