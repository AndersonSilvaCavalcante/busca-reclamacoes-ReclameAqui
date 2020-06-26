import pandas as pd
import time
from datetime import datetime
import os
from selenium import webdriver
from structure_table import report_colums
from enitdades.csv_generator import CSVGenerator

#Exemplo da URL que deve ser usada
RECLAME_AQUI_COMPANY_URL = "https://www.reclameaqui.com.br/empresa/clinica-sim/lista-reclamacoes/" 
#Mude o driver de acordo com o seu S.O
PATH_CHROME_DRIVER = f"{os.getcwd()}/chromedriver/chromedriver" 

def execute_script():
    start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"###Start {start_datetime}###")

    try:
        main_url = RECLAME_AQUI_COMPANY_URL

        browser = webdriver.Chrome(
            executable_path=PATH_CHROME_DRIVER)

        browser2 = webdriver.Chrome(
            executable_path=PATH_CHROME_DRIVER)

        browser.get(main_url)

        company = browser.find_element_by_css_selector(
            '#brand-page-header > section.company-data-wrapper.ng-scope > div > div:nth-child(1) > div.col-xs-12.col-sm-12.col-md-9.brand-page-info > h1 > span')

        report_list = browser.find_elements_by_xpath(
            '//*[@id="complains-anchor-top"]/ul[1]/li')

        df_reports = pd.DataFrame(columns=report_colums)

        print("Get reports...")
        for report in report_list:
            url = report.find_element_by_tag_name('a')
            url = url.get_attribute('href')

            browser2.get(url)
            title = browser2.find_element_by_css_selector(
                '#complain-detail > div > div.row.ng-scope > div.col-md-9.col-sm-8 > div > div.complain-head > div.row > div.col-md-10.col-sm-12 > h1')

            location = browser2.find_element_by_xpath(
                '/html/body/ui-view/div[3]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/ul[1]/li[1]')

            report_date = browser2.find_element_by_xpath(
                '/html/body/ui-view/div[3]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/ul[1]/li[3]')

            report = browser2.find_element_by_xpath(
                '/html/body/ui-view/div[3]/div/div[1]/div[2]/div/div[2]/p')

            document_report = {"title": title.text, "location": location.text,
                               "report_date": report_date.text, "report": report.text, "company": company.text}

            df_reports = df_reports.append(document_report, ignore_index=True)

            time.sleep(2)
        
        print("Generating CSV...")
        if df_reports.shape[0]:
            CSVGenerator(df_reports, os.getcwd(),
                         f"reports_{company.text}", False).generate_csv()

        browser.quit()
        browser2.quit()
    except Exception as e:
        print(f"Error:{e}")
    finally:
        end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"###Finish {end_datetime}###")


if __name__ == "__main__":
    execute_script()
