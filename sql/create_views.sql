/*****************************/
/***   VIEW FOR SYMBOLS    ***/
/*****************************/

drop view if exists symbols;
create view symbols as
    select 
      a.isin
    , a.symbol
    , case when e.symbol is null then 0 else 1 end inhotlist
    , case when b.symbol is null then 0 else 1 end infno
    , case when c.symbol is null then 0 else 1 end innifty50
	, case when d.symbol is null then 0 else 1 end innifty100
    , a.name
    , e.sector
    , a.facevalue
    , a.series
    , a.dateoflisting
    , a.paidupvalue
    , a.marketlot
    , a.runts
    from NSE_EquitySymbols a
        left outer join NSE_EquityFNOCurrentPrice b on a.symbol = b.symbol
        left outer join NSE_Indices c on a.symbol = c.symbol and c.indexname = 'Nifty 50'
		left outer join NSE_Indices d on a.symbol = d.symbol and d.indexname = 'Nifty 100'
        left outer join NSE_MyWatchlist e on a.symbol = e.symbol 
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


drop view if exists profilemc;
create view profilemc as
    select b.symbol, b.name,  b.sector NiftySector, b.innifty50, b.innifty100,  a.sector, marketcap, [52wh] yearhigh, [52wl] yearlow, open, volume, avgprice, prevdate, currentprice, prevclose, pricechange, pricepctchange, lclimit, uclimit, pe, industrype, totalshares, b.runts
    from NSE_EquityProfileMoneyControl a
		left outer join symbols b on a.isin = b.isin
    where 1 = 1
;


drop view if exists profileyf;
create view profileyf as
    select *
    from NSE_EquityProfileYahooFinance
    where 1 = 1
;



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
     , a.prevclose
     , a.open
     , a.pricechange
     , round(a.pricechangepct,2) changepct
     , a.volume
     , a.volume * a.open value
     , c.cpr
     , round(((c.cpr/a.open) * 100), 2) cpr_pct
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
      strftime('%H:%S', a.runts) time
    , b.sector
    , a.symbol
    , a.open, a.low, a.high
    , round(cast(a.volume as REAL)/10000000, 2) volume
    , round((cast(a.volume as REAL) * (a.open + a.low + a.high + a.ltp)/4)/1000000, 2) value
    , a.ltp
    , (a.ltp-a.open)/a.open ltptoopenchangepct
    , cpr, (cpr/a.ltp) cpr_pct
    , case   when a.ltp > R3  then 'Above R3'
             when a.ltp < r3  and  a.ltp > r2 then 'Above R2'
             when a.ltp = r2  then 'On R2'
             when a.ltp < r2  and  a.ltp >= r1 then 'Above R1'
             when a.ltp = r1  then 'On R1'
             when a.ltp > tc  then 'Below R1; Above CPR'
             when a.ltp <= tc and  a.ltp >= bc then 'Within CPR'           
             when a.ltp > s1  then 'Above S1; Below CPR'
             when a.ltp = s1  then 'On S1'             
             when a.ltp > s2  and  a.ltp < s1 then 'Above S2'
             when a.ltp = s2  then 'On S2'
             when a.ltp > s3  and  a.ltp < s2 then 'Above S3'
             when a.ltp = s2  then 'On S3'
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



