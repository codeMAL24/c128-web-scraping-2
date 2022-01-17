from selenium import webdriver
from bs4 import BeautifulSoup
import time 
import csv
import requests

START_URL = "https://exoplanets.nasa.gov//exoplanet-catalog/"
browser = webdriver.Chrome("C:\chromedriver")
browser.get(START_URL)
time.sleep(10)

headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]

planet_data = []
new_planet_data = []


def scrape():
      for i in range(1, 430):
            while True:
                  time.sleep(2)
                  soup = BeautifulSoup(browser.page_source, "html.parser")

                  #the input box where the page number is written
                  current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
                  if current_page_num < i:
                        browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
                  elif current_page_num > i:
                        browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[1]/a').click()
                  else:
                        break
            for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
                  li_tags = ul_tag.find_all("li")
                  temp_list = []

                  for index, li_tag in enumerate(li_tags):
                        if index == 0:
                              temp_list.append(li_tag.find_all("a")[0].contents[0])
                        else:
                              try:
                                    temp_list.append(li_tag.contents[0])
                              except:
                                    temp_list.append("")
                  hyperlink_li_tag = li_tags[0]
                  temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
                  planet_data.append(temp_list)
            browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a')      
            print(f"{i} page done")
            

def scrape_more_data(hyperlink):
      try:
            page = requests.get(hyperlink)
            soup = BeautifulSoup(page.content, "html.parser")
            templist = []

            for tr_tag in  soup.find_all('tr', attrs = {"class", "fact_row"}):
                  td_tags = tr_tag.find_all('td')
                  for td_tag in td_tags:
                        try:
                              templist.append(td_tag.find_all('div', attrs = {"class","value"})[0].contents[0] )
                        
                        except:
                              templist.append("")    

            new_planet_data.append(templist)
      except:
        time.sleep(1)
        scrape_more_data(hyperlink)         

scrape()
for  index, data in enumerate(planet_data):
      scrape_more_data(data[5])

final_planet_data = []
for index , data in enumerate(planet_data):
      e = new_planet_data[index]
      e = [elem.replace("\n","") for elem in e ]
      e = e[:7]
      final_planet_data.append(data + e)

with open("final.csv" , "w") as f:
      c = csv.writer(f)
      c.writerow(headers)
      c.writerows(final_planet_data)



