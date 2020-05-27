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
where 1 = 1