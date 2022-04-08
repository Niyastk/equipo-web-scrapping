
import time
from selenium import webdriver
import pandas

# setup
chrome_driver_path = 'C:\development\chromedriver.exe'
driver = webdriver.Chrome(chrome_driver_path)

# target link
driver.get('https://www.hcpcsdata.com/Codes')

# accessing all the a tags using css selector
groups = driver.find_elements_by_css_selector('.clickable-row a')


# extracting code names from the a tags
group_names = [group.text for group in groups]

# Descriptions(categories) are the third child of table row. so in here we are using a loop to get all the descriptions
category = [driver.find_element_by_css_selector(
    f'body > div > div > table > tbody > tr:nth-child({n}) > td:nth-child(3)').text for n in range(1, len(group_names)+1)]

''
data = {}
for group_name in group_names:
    link = driver.find_element_by_link_text(group_name)
    link.click()
    # getting codes and saving into data dictionary
    data[group_name] = {
        'code': [code.text for code in driver.find_elements_by_css_selector('.clickable-row a')]}

    # getting long description
    data[group_name]['long description'] = [lg.text for lg in driver.find_elements_by_css_selector(
        '.clickable-row td:nth-child(2)')]

    # getting short description
    short_description = []
    for code in data[group_name]['code']:
        item = driver.find_element_by_link_text(code)
        item.click()
        short_description.append(driver.find_element_by_xpath(
            '//*[@id="codeDetail"]/tbody/tr[1]/td[2]').text)
        driver.back()
        time.sleep(2)
    data[group_name]['short description'] = short_description
    driver.back()

# cleaning and creating new list for the dataframe
all_long_description = []
for values in data.values():
    for ld in values['long description']:
        all_long_description.append(ld)
all_short_description = []
for values in data.values():
    for sd in values['short description']:
        all_short_description.append(sd)
all_codes = []
group_names = []
all_categories = []
count = 0
for key, values in data.items():
    for item in values['code']:
        group_names.append(key)
        all_codes.append(item)
        all_categories.append(category[count])
    count += 1
final_data = {
    "Group": group_names,
    "Category": all_categories,
    "Code": all_codes,
    "Long Descriptions": all_long_description,
    "Short Description": all_short_description
}
# making dataframe and converting into csv
data_frame = pandas.DataFrame(final_data)
data_frame.to_csv('test.csv', index=False)
print("completed")
''
