for i in $(seq 2012 2019); 
do echo $i;	
	scrapy crawl interspeech -a target_year=$i -o $i.xml;
done
