create view nselive_eqintraday as
    select *
    from NSE_EquityIntradayPrices
    where 1 = 1
;


/*
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

/*
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

/*
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
