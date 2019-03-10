from scrapy import cmdline

run_spider = 'scrapy crawl douban_spider'.split()
save_csv = "scrapy crawl douban_spider -o ../../data/top250.csv -t csv".split()
cmdline.execute(run_spider)
# cmdline.execute(save_csv)
#Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/7