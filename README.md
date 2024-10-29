# Property Price Prediction

This repository contains an end-to-end data science project aimed at predicting property prices using real-time scraped data. The project involves data scraping, cleaning, model building, API creation, and web deployment, demonstrating a comprehensive workflow for a data science solution.

# Table Of Content

1. [Project Overview](#project-overview)
2. [Data Collection](#data-collection)
3. [Data Cleaning and Preprocessing](#data-cleaning-and-preprocessing)
4. [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-(eda))
5. [Feature Engineering]()
6. [Modeling]()
7. [API Development]()
8. [Deployment]()
9. [Results]()
10. [Usage]()
11. [Technologies Used]()
12. [Future Work]()
13. [Contact]()

### Project Overview

The goal of this project is to build a predictive model that estimates property prices based on various features gathered from online sources. The project walks through the process of web scraping, data processing, and model deployment, ultimately creating an accessible API and a user-friendly interface for real estate price predictions.

### Data Collection

Property price data is collected through web scraping. Key aspects include:
* **Source**: Scraped from [PrivateProperty.co.za](https://www.privateproperty.co.za/).
* **Libraries**: Selenium, Pandas
* **Data Points**:
  | Feature | Data Type | Measuring Unit |
  | ------- | --------- | -------------- |
  | Suburb | String | None |
  | Property Description | String | None |
  | Address | String | None |
  | Price | String | Rands (R) |
  | Property Details | List | None |
  | Property Features | List | None |
  | Image | String | None |

### Data Cleaning and Preprocessing

Data cleaning ensures high-quality inputs for the model. This step includes:
* **Data Cleaning**:
  * *Miscellaneous Data Errors* - Converted property details and features from strings into list objects, iterating through them to extract key-value pairs. These pairs were then used to create dataframes, which were appended to the original dataframe.
* **Duplicate Values**:
  * There were a total of 4 duplicated values that were identified and removed from the dataframe.
* **Null Values**:
  *   There were a toal of 34189 null values in the dataframe.
  *   Features with majority null values were dropped, these included: address, Erf_size_(m²).
  *   Floor size and Lounges null values were imputed using KNNimputer from the sklearn library.
* **Outlier Values**:
  *  Removed outlier values from the dataset.

### Exploratory Data Analysis (EDA)

EDA is conducted to understand relationships between features and uncover patterns in the data. Visualisations and statistical tests are included, focusing on:

**Feature Distribution Before Scaling**:
* The distribution of the features is positively skewed, with Bathroom being slightly skewed, and Price, Floor Size, Bedrooms, and Lounges being heavily skewed.
* Price and Floor Size are found to contain continuous numeric data, whereas the other features are found to contain discrete numeric data.

![output](https://github.com/user-attachments/assets/358909f8-104f-4281-8e3b-438b294262c2)

**Correlation To Attrition Feature**
* The features most correlated to the Price of a property
* The most correlated feature to Price, is Bedrooms, with a correlation coefficient of 0.78.

