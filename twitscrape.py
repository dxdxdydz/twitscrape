from selenium import webdriver
import time
from bs4 import BeautifulSoup
def twitscrape(query='', includes=[], excludes=[], n_scrolls=100, n_tweets=500, check_end=False, init_time=6,
               scroll_pause_time=1):
    driver = webdriver.Chrome()  # need to download the browser driver first
    if includes != []:
        include_query = '%20OR%20'.join(includes)
        include_string = '%20({})'.format(include_query)
    else:
        include_string = ''
    exclude_string = ''
    for exclude in excludes:
        exclude_string += '%20-{}'.format(exclude)

    url = 'https://www.twitter.com/search?q={}{}{}&src=typed_query&f=live'.format(query, include_string, exclude_string)

    driver.get(url)
    screen_height = driver.execute_script("return window.screen.height;")
    i = 5
    time.sleep(init_time)  # Allow x seconds for the web page to open (set higher for bad internet)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    htmls = soup.find_all(attrs = {"data-testid": 'tweet'})
    text_final = []  # initialize main list
    users = []


    for html in htmls:
        user = html.find_all('a', href = True)
        tweet = html.find_all("div", attrs = {"data-testid": 'tweetText'})
        text_final.append(tweet[0].text)
        users.append(user[0]['href'])

    # scroll one screen height each time (the effective multiplier to avoid duplicate is 6)
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height = screen_height, i = i))
    i += 5
    time.sleep(scroll_pause_time)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    htmls = soup.find_all("div", attrs = {"data-testid": 'tweet'})

    text = []  # initialiZe intermediate list
    user_i = []
    n = 0
    while len(text_final) < n_tweets:
        #         for html in htmls:
        #             text.append(html.text)

        for html in htmls:
            user = html.find_all('a', href = True)
            tweet = html.find_all("div", attrs = {"data-testid": 'tweetText'})
            try:
                text.append(tweet[0].text)
                user_i.append(user[0]['href'])
            except:
                pass
        print(text)
        print('------------------------------------------')

        n_duplicates = len(set(text_final).intersection(set(text)))
        text_final[len(text_final):0] = text[n_duplicates:]
        users[len(users):0] = user_i[n_duplicates:]
        print(len(text_final))
        print('**********************************')
        text = []
        user_i = []

        # scroll one screen height each time (the effective multiplier to avoid duplicate is 6)
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height = screen_height, i = i))
        i += 6

        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")

        htmls = soup.find_all(attrs = {"data-testid": 'tweet'})

        if check_end:
            if htmls == soup.find_all("div", attrs = {"data-testid": 'tweetText'}):
                break
            else:
                htmls = soup.find_all("div", attrs = {"data-testid": 'tweetText'})

        else:
            soup = BeautifulSoup(driver.page_source, "html.parser")
        n += 1
    return {'user': users, 'tweet': text_final}