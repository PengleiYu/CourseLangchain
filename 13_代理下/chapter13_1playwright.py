# 展示playwright工具的使用
from playwright.sync_api import sync_playwright


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://langchain.com/')
        title = page.title()
        print('title=', title)
        browser.close()


if __name__ == '__main__':
    run()
