
file=$(ls -1 ../data/bse* | tail -1)

date=`tail -1 $file | cut -d"," -f1 | sed 's/-//g'`
date=`./dateAdd days $date 1`
enddate=`date '+%Y%m%d'`
outfile="../data/.bsetemp"
 
#date  - yyyymmdd
#date1 - mmddyy
#date2 - yyyy-mm-dd
 
while [ $date -le $enddate ]
do
	date1=`echo $date | sed 's/^..\(..\)\(..\)\(..\)$/\3\2\1/'`
	date2=`echo $date | sed 's/^\(....\)\(..\)\(..\)$/\1-\2-\3/'`
	url="http://www.bseindia.com/download/BhavCopy/Equity"
	url=$url"/eq${date1}_csv.zip"
	dfile=eq${date}.zip
	curl $url -o $dfile 2> /dev/null 
	unzip -o $dfile > /dev/null 2> /dev/null
	[ $? -eq 0 ] && {
		infile=`unzip -l $dfile | head -4 | tail -1 | awk '{ print $NF }'`
		awk -v batchdate=$date2 -F "," '
			BEGIN { OFS = "," }
			{
				if ( NR == 1 ) next;
				print batchdate, $2, $1, $5, $6, $7, $8, $9, $10, $11, $12, $13, $4, $3
		}' $infile >> $outfile
		rm -f $infile 
		echo "Downloaded and processed BSE equity file for $date"
	}
	rm -f $dfile
	date=`./dateAdd days $date 1`
done

#split downloaded data into respective year file

cat $outfile | awk '{
	yr=substr($0,1,4)
	fname="../data/bse"yr
	print $0 >> fname
}'

rm -f $outfile

