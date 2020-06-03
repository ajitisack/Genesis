/*** Indices View ***/
drop view if exists indices;
create view indices as 
	select c.symbol, b.isin, a.*
	from nseindices a
		left outer join nseprofilemc b on a.code = b.symbolcd
		left outer join symbols c on b.isin = c.isin
	where 1 = 1
	union all
	select c.symbol, b.isin, a.*
	from bseindices a
		left outer join bseprofilemc b on a.code = b.symbolcd
		left outer join symbols c on b.isin = c.isin
	where 1 = 1;

	

/*** Actions View ***/
drop view if exists events;
create view events as 
	select * from nseevents where 1 = 1
	union all
	select * from bseevents where 1 = 1;



/*** EsgScores View ***/
drop view if exists esgscores;
create view esgscores as 
	select * from nseesgscores where 1 = 1
	union all
	select * from bseesgscores where 1 = 1;



/*** HistPrice View ***/
drop view if exists histprice;
create view histprice as 
	select * from nsehistprice where 1 = 1
	union all
	select * from bsehistprice where 1 = 1;

	
	
/*** Yahoo Finance Profile View ***/
drop view if exists profileyf;
create view profileyf as 
	select * from nseprofileyf where 1 = 1
	union all
	select * from bseprofileyf where 1 = 1;


/*** Money Control Profile View ***/
drop view if exists profilemc;
create view profilemc as 
	select * from nseprofilemc where 1 = 1
	union all
	select * from bseprofilemc where 1 = 1;