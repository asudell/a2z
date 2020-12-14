FILES="DataLoading.html XPN2020.html data/xpn2020.csv"
FILES="$FILES data/XPN2020_and_88Worst.csv data/XPN2020_and_885Best.csv"
DEST=regulus:/var/www/www.drewsudell.org/html/projects/a2z
for x in ${FILES}
	do scp $x ${DEST}/${x}
done


