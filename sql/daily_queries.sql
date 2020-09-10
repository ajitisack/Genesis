/*----------------*/
/*  MARKET HOURS  */
/*----------------*/
-- Equity Current Price
select time, sector, symbol, prevclose, open, openchangepct, low , high , volume , value, pricestatus, ltp, ltptoopenchangepct, changepct, cpr, cpr_pct, prevlow, prevhigh, openislow, openishigh, NR4, NR7, NR9
from currentprice 
where 1 = 1
    and inhotlist = 1
--    and infno = 1
order by sector, symbol
;

select sector, symbol, ltp from currentprice where inhotlist = 1 order by sector, symbol;


/*-------------------*/
/*  MARKET PRE OPEN  */
/*-------------------*/

-- Pre Open Market Data
select sector, symbol, prevclose, open, changepct, volume, value, openstatus, cpr, cpr_pct, prevlow, prevhigh, yearlow, yearhigh, NR4, NR7, NR9
from preopen
where 1 = 1
    and inhotlist = 1
--    and infno = 1    
order by sector, symbol
;


/*----------------------*/
/*  AFTER MARKET HOURS  */
/*----------------------*/

-- End of Day Analysis
select sector, symbol, openinggap, openinggappct, prevclose, open, low, high, tr, trratio, cprtoday, cprwidthtoday, close, closinggap, closinggappct, change, changepct, totaltradevalue, volume, prevvolume, volumechangepct, openislow, openishigh
from technicals
where 1 = 1
--    and infno = 1
    and inhotlist = 1 
order by sector, symbol
;


-- Pivot Points & Narrow Range for Next Day
select sector, symbol, close ltp, cprtomorrow cpr, cprwidthtomorrow cpr_pct, NR4, NR7, NR9, lowerhigh, higherlow
from technicals
where 1 = 1
    and inhotlist = 1
--    and infno = 1
order by sector, symbol
;

