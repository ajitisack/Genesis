select 
a.symbol, a.name, a.industry BSE_industry, b.industry YF_industry, b.sector, b.shortname, b.longname
from security a
	left outer join securitydetails b on a.symbol = b.symbol
where 1 = 1
and a.industry <> 'Index Fund';