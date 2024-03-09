import sys
import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 创建一个字典，将货币代码映射到中文货币名称
currency_mapping = {
    "英镑": "GBP",
    "港币": "HKD",
    "美元": "USD",
    "瑞士法郎": "CHF",
    "德国马克": "DEM",
    "法国法郎": "FRF",
    "新加坡元": "SGD",
    "瑞典克朗": "SEK",
    "丹麦克朗": "DKK",
    "挪威克朗": "NOK",
    "日元": "JPY",
    "加拿大元": "CAD",
    "澳大利亚元": "AUD",
    "欧元": "EUR",
    "澳门元": "MOP",
    "菲律宾比索": "PHP",
    "泰国铢": "THB",
    "新西兰元": "NZD",
    "韩国元": "KRW",
    "卢布": "RUB",
    "林吉特": "MYR",
    "新台币": "TWD",
    "西班牙比塞塔": "ESP",
    "意大利里拉": "ITL",
    "荷兰盾": "NLG",
    "比利时法郎": "BEF",
    "芬兰马克": "FIM",
    "印度卢比": "INR",
    "印尼卢比": "IDR",
    "巴西里亚尔": "BRL",
    "阿联酋迪拉姆": "AED",
    "南非兰特": "ZAR",
    "沙特里亚尔": "SAR",
    "土耳其里拉": "TRY",
}

# 根据货币代码获取中文货币名称
def get_currency_name(code):
    for currency_name, currency_code in currency_mapping.items():
        if currency_code == code:
            return currency_name
    return "未知"




def fetch_currency_rate(date, currency_code):
    service = Service('D:/unload/chromedriver-win64/chromedriver.exe')
    service.start()

    try:
        driver = Chrome(service=service)

        driver.get("https://www.boc.cn/sourcedb/whpj/")

        # 输入查询日期
        date_input = driver.find_element(By.NAME, 'erectDate')
        date_input.clear()
        date_input.send_keys(date)
        date_input.send_keys(Keys.ENTER)

        # 根据货币代码选择对应的中文货币
        currency_select = driver.find_element(By.ID,'pjname')
        options = currency_select.find_elements(By.TAG_NAME,'option')
        currency_name = get_currency_name(currency_code)
        #print(get_currency_name(currency_code))
        for option in options:
            if option.get_attribute("value") == get_currency_name(currency_code):
                option.click()
                break

        # 点击查询按钮
        search_button = driver.find_element(By.CSS_SELECTOR,'input.search_btn[style*=\'float:right\']')
        search_button.click()

        # 等待结果加载完成
        time.sleep(2)

        # 获取汇率信息
        rate_element = driver.find_element(By.XPATH,
                                           f"//tr[@class='odd']/td[contains(text(), '{currency_name}')]/following-sibling::td[3]")
        rate = rate_element.text
        #print(rate)
        # 将结果写入文件
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(f"{date} {currency_code}: {rate}\n")

        return rate

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        try:
            driver.quit()
            service.stop()
        except NameError:
            pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: CESHI1.py <date> <currency_code>")
        sys.exit(1)

    date = sys.argv[1]
    currency_code = sys.argv[2]

    rate = fetch_currency_rate(date, currency_code)
    if rate:
        print("现汇卖出价:", rate)