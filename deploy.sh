FILES="Dataloading2.html"
FILES="$FILES SongsByWomen.html"
# XPN2020_One_Vote_Wonders.html"
FILES="$FILES data/90sA2Z.csv"
#FILES="$FILES data/xpn2020_onsies.csv"
#FILES="$FILES data/XPN2020_and_88Worst.csv data/XPN2020_and_885Best.csv"
#FILES="$FILES data/885best_xpn2020_reranked.csv"
DEST=regulus:/var/www/www.drewsudell.org/html/projects/a2z
for x in ${FILES}
	do scp $x ${DEST}/${x}
done


