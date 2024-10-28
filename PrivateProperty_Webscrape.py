# import the necessary libraries
import selenium
from selenium import webdriver
import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import selenium.webdriver.remote
import selenium.webdriver.remote.webelement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tqdm import tqdm
import time
import random
import pandas as pd

# Return all the columns of the dataframe
pd.set_option('display.max_columns', None)

#  Create undetectable driver instance
Service = Service(r'C:\Program Files\WebDrivers\chromedriver.exe')
Options = webdriver.ChromeOptions()
Options.add_argument("start-maximized")
Options.add_experimental_option("excludeSwitches", ["enable-automation"])
Options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(service=Service, options=Options)
url = 'https://www.privateproperty.co.za/'
wait = WebDriverWait(driver, 30)
actions = ActionChains(driver)
WebElement = selenium.webdriver.remote.webelement.WebElement


def random_wait(a: int, b: int) -> None:
    """
    A function that is responsible for mimicks human wait waiting time
    during scrolling on a webpage

    Args:
        a: int.
            Integer value indicating the starting value of the waiting
            range of time.
        b: int.
            Integer value indicating the end value of the waiting range
            of time
    Returns:
        None
    """
    time.sleep(random.randint(a, b))


def openBrowser(url: str) -> None:
    """
    A function that is responsible for opening the browser

    Args:
        url: str.
            String value of an web address
    Returns:
        None.
    """
    i = 0
    while i < 3:
        try:
            driver.get(url)
            random_wait(3, 5)
            acceptCookies()
            break
        except TimeoutException:
            driver.refresh
            i += 1
            print(f'Refreshed at link ... {i}')


def acceptCookies():
    try:
        time.sleep(2)
        button = driver.find_element(
            By.XPATH, '//button[contains(text(), "Accept all cookies")]')
        random_wait(2, 3)
        scroll_and_click(button)
    except NoSuchElementException:
        pass


def scroll_and_click(element: WebElement) -> None:
    """
    A function that scrolls to a web element, and clicks on that web
    element.

    Args:
        WebElement: WebElement.
            object representing an HTML element on a web page which can
            be interacted with using the Selenium WebDriver in
            automation scripts
    Returns:
        None.
    """
    actions.move_to_element(element).perform()
    random_wait(1, 4)
    actions.move_to_element(element).click().perform()
    random_wait(1, 3)


def sendKeys(input_bar: WebElement, text_input: str) -> None:
    """
    A function that inputs texts characters into a search input.

    Args:
        input_bar: WebElement.
            An input bar where input text will be sent.
        text_input: str.
            A string that will be sent into the search bar.

    Returns:
        None

    """
    random_wait(2, 4)
    # Send keys to a search input, input_bar
    input_bar.send_keys(text_input)
    random_wait(2, 3)
    # Simulate the pressing of enter to exit the search input and
    # search value sent into the input text
    input_bar.send_keys(Keys.RETURN)


def areaSearch(area: str):
    """
    A function that is inputs an area to search into the search input.

    Args:
        area: str.
            Name of the area we are searching.
    """
    random_wait(3, 5)
    wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="search"]'))
    )
    # Store the search bar.
    search_bar = driver.find_element(By.XPATH, '//input[@type="search"]')
    # Move to the search bar.
    scroll_and_click(search_bar)
    # Send keys to the search bar
    sendKeys(search_bar, area)


def propertyLinks(areas: list) -> dict[str: list]:
    """
    A function that is responsible for returning a dictionary and where
    the key is the area, and the values are a list of links to
    properties

    Returns:
        area_prop_dct: dict.
            A dictionary with a key value pair of a string and a list.
    """
    # Open the browser
    openBrowser(url)
    # Areas to Search
    area_prop_dct = {}
    for area in areas:
        areaSearch(area)
        random_wait(7, 10)
        i = 0
        property_links = []
        while True:
            # Store all the properties on the current web page
            property_containers = (
                driver.find_elements(By.XPATH, '//a[@class="listing-result"]')
            )
            properties = [
                property.get_attribute('href')
                for property in property_containers
            ]
            property_links.append(properties)
            # Scroll to each web element
            for container in tqdm(property_containers):
                i += 1
                actions.move_to_element(container).perform()
                random_wait(1, 5)
            try:
                next = (
                    driver.find_element(
                        By.XPATH, '//span[contains(text(), "Next")]/parent::a'
                    )
                )
                scroll_and_click(next)
            except NoSuchElementException:
                print(f"Area: {area}\nTotal properties: {i}")
                break

        # Flatten the nested list using list comprehension
        property_links = [
            link for sublist in property_links for link in sublist
        ]
        dct = {area: property_links}
        area_prop_dct.update(dct)
        print(
            f"\n {area} has been added with a total of {len(property_links)}"
        )

    return area_prop_dct


def propertyScrape() -> dict[str: str]:
    """
    A function that is responsible for scraping the information about a
    property from the webpage.
    """
    random_wait(2, 4)
    r = 0
    while r < 3:
        try:
            # Store standard information
            property_price = driver.find_element(
                By.XPATH,
                '//div[@class="listing-price-display__price txt-heading-1"]'
            ).text
            property_desc = driver.find_element(
                By.XPATH, '//h1[@class="listing-details__title"]'
            ).text

            # If the address variable is available, store the address
            try:
                address = driver.find_element(
                    By.XPATH, '//a[@id="address-show-map"]'
                ).text
                standard_dct = {
                    "propert_desc": property_desc,
                    "address": address,
                    "price": property_price
                }
            except NoSuchElementException:
                standard_dct = {
                    "propert_desc": property_desc,
                    "price": property_price
                }

            # Scroll to the property_detail container
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="property-features"][1]')
                )
            )
            scroll_element = driver.find_element(
                By.XPATH, '//div[@class="property-features"][1]'
            )

            actions.move_to_element(scroll_element).perform()
            random_wait(2, 4)

            # Store the WebElements for property details
            property_detail_name = driver.find_elements(
                By.XPATH, '//div[@class="property-features"][1]/ul/li/span'
            )
            # Store the text values of the property details
            property_detail_name = [
                detail_name.text for detail_name in property_detail_name
            ]
            # Store the property details as a dictionary
            property_details_dct = {
                'property_details': property_detail_name
            }

            # Store the WebElements for property features
            property_features_values = driver.find_elements(
                By.XPATH,
                f'//div[@id="property-features-list"]/ul/li/span/span'
                f'/parent::span'
            )
            # Store the text values for property feature
            property_features_values = [
                feature_value.text for feature_value
                in property_features_values
            ]
            # Store the property features as a dictionary
            property_features_dct = {
                'property_features': property_features_values
            }

            # Store image as a dictionary
            property_img = driver.find_element(
                By.XPATH,
                '//div[@class="media-container__image--main"]/img'
            ).get_attribute('src')

            random_wait(1, 4)

            standard_dct.update(property_details_dct)
            standard_dct.update(property_features_dct)
            standard_dct.update({'image': property_img})

            return standard_dct
        except NoSuchElementException:
            r += 1
            driver.refresh()
            print(f'Page refreshed . . . {r}')


def main():
    # Get the property links and area names.
    area_prop_dct = propertyLinks(['Rosebank and Parktown'])

    # iterate through the key and value pairs of the area_prop_dct
    # dictionary
    table_information = []
    for key, value in area_prop_dct.items():
        for link in tqdm(value):
            suburb_dct = {"suburb": key}
            openBrowser(link)
            property_data_dct = propertyScrape()
            try:
                suburb_dct.update(property_data_dct)
                table_information.append(suburb_dct)
            except TypeError:
                continue

    # Close the browser
    driver.close()

    # Store as a pandas dataframe
    df = pd.DataFrame(table_information, index=range(len(table_information)))
    print(df)

    # Save the dataframe as a csv file.
    df.to_csv(f'{list(area_prop_dct.keys())[0]}_real_estate.csv')


if __name__ == "__main__":
    main()
