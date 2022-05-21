# twitscrape
tweet extractor using python selenium
will only scrape the latest tweets together with user account
made it because plenty of unemployment time lol
suggestion for improvement will be appreciated

IMPORTANT
you need selenium library and googlechrome + related driver before using it
dont forget to check to make sure the driver is of suitable version to the browser

direct use by function twitscrape(query='',includes=[],excludes=[],n_tweets=500,check_end=False,init_time=6,scroll_pause_time=1)

  query
  string of word you want to search on twitter

  includes
  list of strings to include with main query, default:None

  excludes
  list of strings to exclude with main query, default:None

  n_tweets
  number of tweets to be retrieved 

  check_end
  set True if the page scrolling can reach the end (for example on Top tab)

  init_time
  time given to browser to load twitter page. bad internet? bad laptop? increase it. default=6 (seconds)

  scroll_pause_time
  time given to browser to load scrolled twitter page. bad internet? bad laptop? increase it, default=1 (second)

the function will return Dict type {'user':[*args],'tweet':[*args]}
