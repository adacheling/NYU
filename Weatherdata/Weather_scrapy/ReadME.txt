//first run
conda create -n web_scrapy
conda activate web_scrapy
conda install -c conda-forge --name web_scrapy selenium 
conda install -c conda-forge --name web_scrapy phantomjs 

//run code
python3 weather_spider.py -sNY -wknyc -y2016 -m1-12 weather_2016
python3 weather_spider.py -sNY -wknyc -y2017 -m1-12 weather_2017

//Reference: We want to give special thank you to our friend: Yang Gao for helping us with the scrapy tool. 