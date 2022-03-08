from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import pyautogui


def download(site, remainingDownloads):
    browser.get(site)
    browser.implicitly_wait(0.5)
    first = True
    if remainingDownloads != "all":
        if int(remainingDownloads) < 1:
            return

    # get link from LMAnime.com

    else:
        if browser.find_elements("class name", "nolink"):
            if not first:
                print("Reached end of show!")
                return
            first = False

    nextSite = browser.find_elements("class name", "nvs")[2].find_elements("tag name", "a")[0].get_attribute("href")
    savename = browser.find_elements("class name", "entry-title")[0].get_attribute("innerHTML")
    downloadPage = browser.find_elements("class name", "mctnx")

    langSelection = downloadPage[0].find_elements("class name", "soraddlx")

    LangEng = langSelection[0].find_elements("class name", "soraurlx")
    linkElements = LangEng[0].find_elements("tag name", "a")
    href = 0
    try:
        for element in linkElements:
            if element.get_attribute("innerHTML") == "FEMBED":
                href = element.get_attribute("href")
        asdf
    except:
        try:
            href = linkElements[1].get_attribute("href")
        except:
            href = linkElements[0].get_attribute("href")

    browser.implicitly_wait(0.5)

    # leaving LMAnime.com

    browser.get(href)
    browser.implicitly_wait(0.5)

    # handle url shortener if needed
    skip = False
    if browser.current_url[0:21] != "https://suzihaza.com/":
        skip = not handleUrlShortener(browser.current_url)

    time.sleep(2)
    if browser.current_url[0:21] != "https://suzihaza.com/":
        skip = True

    if not skip:
        downloadButton = browser.find_elements("id", "download")
        downloadButton[0].click()
        browser.implicitly_wait(11)
        time.sleep(12)
        try:
            link = browser.find_elements("class name", "clickdownload")[2].get_attribute('href')

        except:
            try:
                link = browser.find_elements("class name", "clickdownload")[1].get_attribute('href')

            except:
                link = browser.find_elements("class name", "clickdownload")[0].get_attribute('href')

        # download video from link

        downloadVideo(link, savename)

    else:
        print(f"Couldn't download {savename} please download manually on {site}.")

    if not nextSite:
        return
    time.sleep(10)

    if remainingDownloads == "all":
        download(nextSite, remainingDownloads)
    else:
        download(nextSite, int(remainingDownloads)-1)


def handleUrlShortener(address):
    if address[0:12] == "https://ouo.":
        print('Registered ouo.io url shortener!\nTrying to skip url shortener')
        browser.implicitly_wait(0.5)
        time.sleep(2)
        try:
            browser.find_elements("id", "btn-main")[0].click()
        except:
            browser.find_elements("id", "captcha")[0].click()

        browser.implicitly_wait(3.2)
        time.sleep(3.2)

        skipAd("https://ouo.io/")

        try:
            browser.find_elements("id", "form-go")[0].click()
            browser.implicitly_wait(1)
            time.sleep(1)
        except:
            time.sleep(2)
            try:
                browser.find_elements("id", "btn-main")[0].click()
            except:
                browser.find_elements("id", "captcha")[0].click()

            browser.find_elements("id", "form-go")[0].click()
            browser.implicitly_wait(1)
            time.sleep(1)

        skipAd("https://ouo.io/")
        return True
    else:
        return False


def downloadVideo(link, savename):
    browser.get(link)
    browser.implicitly_wait(4)
    time.sleep(5)
    webdriver.ActionChains(browser).key_down(Keys.SPACE).perform()
    webdriver.ActionChains(browser).context_click(browser.find_elements("tag name", "video")[0]).perform()
    pyautogui.press("down", 9)
    pyautogui.press("enter")
    time.sleep(5)
    pyautogui.press("backspace")
    pyautogui.typewrite(savename)
    pyautogui.press("enter")


def skipAd(site):
    if browser.current_url[0:len(site)] != site or browser.current_url != "https://suzihaza.com/":
        time.sleep(1.5)
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(1)


if __name__ == "__main__":
    print("-------------------------- LMAnime.com Downloader --------------------------")
    url = input("Enter the url to the first episode of the Show\n>")
    end = input("How many Episodes do you want to download?\n>")

    print("Starting will open a firefox window. Please always keep this window in the foreground.")
    if input("Do you want to start? (y/n)") == "y":
        options = Options()
        options.unhandled_prompt_behavior = "dismiss"
        options.set_preference("dom.webnotifications.enabled", False)
        browser = webdriver.Firefox(options=options)

    else:
        exit()

    download(url, end)

    if input("Was everything successful?\n>") == 'y':
        browser.quit()
    else:
        print("Please download everything missing manually.")
