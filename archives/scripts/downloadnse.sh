getMonth(){
cat << !month | grep "^$1" | cut -d"-" -f2
01-JAN
02-FEB
03-MAR
04-APR
05-MAY
06-JUN
07-JUL
08-AUG
09-SEP
10-OCT
11-NOV
12-DEC
1-JAN
2-FEB
3-MAR
4-APR
5-MAY
6-JUN
7-JUL
8-AUG
9-SEP
!month
}

createEQFile(){
	awk -F "," '
	BEGIN {
		OFS = ","
		a["JAN"]="01"
		a["FEB"]="02"
		a["MAR"]="03"
		a["APR"]="04"
		a["MAY"]="05"
		a["JUN"]="06"
		a["JUL"]="07"
		a["AUG"]="08"
		a["SEP"]="09"
		a["OCT"]="10"
		a["NOV"]="11"
		a["DEC"]="12"
	}
	{
		if ( NR == 1 ) next;
		split($11, date, "-")
		dd = date[1] 
		mm = a[date[2]]
		yy = date[3] 
		if (length(dd) == 1) dd = "0"dd
		batch_date = yy"-"mm"-"dd
		print batch_date, $1, $13, $3, $4, $5, $6, $7, $8, $12, $9, $10, $2","
	}' $1
}

file=$(ls -1 ../data/nse* | tail -1)
date=`tail -1 $file | cut -d"," -f1 | sed 's/-//g'`
date=`./dateAdd days $date 1`
enddate=`date '+%Y%m%d'`
outfile="../data/.nsetemp"
user_agent='Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'

while [ $date -le $enddate ]
do
	yy=`echo $date | cut -c1-4`
	mm=`echo $date | cut -c5-6`
	dd=`echo $date | cut -c7-8`
	mon=`getMonth $mm`

	dfile=cm${dd}${mon}${yy}bhav.csv.zip
	file=cm${dd}${mon}${yy}bhav.csv
	url="http://www.nseindia.com/content/historical/EQUITIES/${yy}/${mon}/${dfile}"

	curl -A "$user_agent" -O $url 2> /dev/null 
	unzip -o $dfile > /dev/null 2> /dev/null
	[ $? -eq 0 ] && {
		createEQFile $file >> $outfile
		rm -f $file
		echo "Downloaded and processed NSE equity file for $date"
	}
	rm -f $dfile

	date=`./dateAdd days $date 1`

done

cat $outfile 2> /dev/null | awk '{
	yr=substr($0,1,4)
	fname="../data/nse"yr
	print $0 >> fname
}'

rm -f $outfile

