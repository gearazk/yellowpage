echo "Please have Python3 and Scrapy installed "
echo "The result will be in the data_result.csv file"
python3 $(python3 -m site --user-site)/scrapy runspider ./crawler.py -o data_result.csv -t csv