from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm


def scrapping(fetch_url, speeches_url_log_file):
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    opts.add_argument("headless")
    n = 63  # No. of scrolls

    # x paths for Selenium
    x_path_link = '//*[@id="td-outer-wrap"]//div[2]/h3/a'
    x_path_btn = '//*[@id="td-outer-wrap"]/div[3]/div/div/div[1]/div/div[{}]/a'

    driver = webdriver.Chrome(options=opts)
    driver.get(fetch_url)

    # scroll down page n times
    for i in range(0, 5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    for no in tqdm(range(0, n)):
        button = driver.find_element_by_xpath(x_path_btn.format(32 + no * 10))
        try:
            button.click()
            time.sleep(1.5)
        except NoSuchElementException:
            time.sleep(10)
            button.click()
            time.sleep(5)

    sel_links = driver.find_elements_by_xpath(x_path_link)

    links = []
    for link in sel_links:
        links.append(link.get_attribute('href'))
    driver.quit()

    # Create logging file with links
    with open(speeches_url_log_file, 'w') as fp:
        for item in links:
            fp.write("%s\n" % item)

    return links
