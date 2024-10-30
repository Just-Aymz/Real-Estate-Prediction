# **Property Price Prediction**

This repository contains an end-to-end data science project aimed at predicting property prices using real-time scraped data. The project involves data scraping, cleaning, model building, API creation, and web deployment, demonstrating a comprehensive workflow for a data science solution.

# **Table Of Content**

1. [Project Overview](#project-overview)
2. [Data Collection](#data-collection)
3. [Data Cleaning and Preprocessing](#data-cleaning-and-preprocessing)
4. [Exploratory Data Analysis (EDA)](#exploratory-data-analysis)
5. [Feature Engineering](#feature-engineering)
6. [Modeling](#modeling)
7. [API Development](#api-development)
8. [Deployment](#deployment)
9. [Results](#results)
10. [Usage](#usage)
11. [Technologies Used](#technologies-used)
12. [Future Work](#future-work)
13. [Contact](#contact)

# **Project Overview**

The goal of this project is to build a predictive model that estimates property prices based on various features gathered from online sources. The project walks through the process of web scraping, data processing, and model deployment, ultimately creating an accessible API and a user-friendly interface for real estate price predictions.

# **Data Collection**

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

# **Data Cleaning and Preprocessing**

Data cleaning ensures high-quality inputs for the model. This step includes:
* **Data Cleaning**:
  * *Miscellaneous Data Errors* - Converted property details and features from strings into list objects, iterating through them to extract key-value pairs. These pairs were then used to create dataframes, which were appended to the original dataframe.
* **Duplicate Values**:
  * There were a total of 4 duplicated values were identified and removed from the dataframe.
* **Null Values**:
  *   There were a total of 34189 null values in the dataframe.
  *   Features with majority null values were dropped, these included: address, Erf_size_(m²).
  *   Floor size and Lounges null values were imputed using KNNimputer from the sklearn library.
* **Outlier Values**:
  *  Removed outlier values from the dataset.

# **Exploratory Data Analysis**

EDA is conducted to understand relationships between features and uncover patterns in the data. Visualisations and statistical tests are included, focusing on:

**Feature Distribution Before Scaling**:
* The distribution of the features is positively skewed, with Bathroom being slightly skewed, and Price, Floor Size, Bedrooms, and Lounges being heavily skewed.
* Price and Floor Size are found to contain continuous numeric data, whereas the other features are found to contain discrete numeric data.

![output](https://github.com/user-attachments/assets/358909f8-104f-4281-8e3b-438b294262c2)

**Correlation To Price Feature**
* The features most correlated to the Price of a property.
* The most correlated feature to Price, is Bedrooms, with a correlation coefficient of 0.78

![output](https://github.com/user-attachments/assets/072a8dc4-6f46-4fe8-8e04-21948a68dcb4)

**Total Properties per Suburb**
* There are a total of 2711 properties in the dataset from Fourways, Sunninghill, and Lonehill.
* There are a total of 308 properties in the dataset from Modderfontein.
* There are a total of 2411 properties in the dataset from Rosebank and Parktown.

![output](https://github.com/user-attachments/assets/699b6b1a-5bac-4c0f-96e4-a30024eff128)

**Average Price per Suburb**
* Rosebank and Parktown are the most expensive suburbs based on the properties in the dataset.
* Modderfontein is the least expensive suburb based on the properties in the dataset.
* However, this needs to be caveated by the fact that Modderfontein has significantly fewer properties that make this average.

![output](https://github.com/user-attachments/assets/e713b3e9-18f4-4459-89ed-654f3defac6e)

**Average Price per m²**
* Modderfontein has the highest average price per m² out of the three areas with a total price of R23961 per m² on average

![output](https://github.com/user-attachments/assets/f3b3f1dd-207a-4638-8f9b-bb65cbe8c5ed)

**Average Price per Property Type**
* Based on the average price per property plot, it can be seen that the small holding property type is on average the most valuable, however, on further analysis, we can see that  we do not really large sample space into this matter, with only one property being a small holding in the entire dataset
* We can see that the next 3 most expensive property types are Houses, Penthouses, and Clusters. Based on the dataset, we can see that Rosebank and Parktown have the most of this property type.

![output](https://github.com/user-attachments/assets/4f38c7ee-fed0-445d-9b1f-837427525979)

![output](https://github.com/user-attachments/assets/c7a17bb8-14a1-43f8-be4e-711090417d28)

# **Feature Engineering**
Feature engineering is applied to create meaningful features that improve model accuracy. Examples include:

* **One-Hot Encoding**:
  *  Applied one-hot encoding on the suburb and property type features to convert the string features into numeric feature that can be used in training the model, removed one feature from each of the generated features from the two variables to avoid multicollinearity.
* **Scaling and Transformation** :
  * Used the skew function to find the skew direction of each feature. It was found that all the features have a positive skew, with price, floor size, bathrooms, and lounges having a heavy positive skew, whilst bedrooms only had a slight positive skew
  * The p-value of each feature was found using the Normal Statistical test to confirm the distribution of the features. All the features rejected the null hypothesis (the assumption made was that all the features are normally distributed).
  * Based on the kurtosis value of each feature, it was found that all the features had a Leptokurtic distribution, which indicated the presence of heavier tails in the distribution curve of the feature, which means that the features contained outlier values. This was taken into consideration when identifying the scaling method.
  * Due to the heavy skew of the features—price, floor size, bathrooms, and lounges—a log transformation was applied to bring about a more normal distribution before applying scaling.
  * RobustScaler was applied to the features because of the aforementioned reasons.

# **Modeling**
Multiple regression models were tested to determine the best fit for property price prediction, including:

* **Algorithms**:
  * Linear Regression, Random Forest, Gradient Boosting, XGBoost.
* **Evaluation Metrics**:
  * Mean Absolute Error (MAE), Root Mean Squared Error (RMSE).
* **Model Selection**:
  * Hyperparameter tuning via GridSearchCV to identify the optimal model.
 
# **API Development**
An API was developed to make predictions available for live queries. Key points include:

* **Framework**
  * FastAPI.
* **Endpoints**:
  * ```/predict``` - Takes property details as input and returns predicted price.
* **Testing**:
  * API tested with real-world inputs to ensure accurate predictions.

# **Deployment**
The model and API are deployed to make the service accessible:

* **Cloud Platform**:
  * Deployed on [mention platform, e.g., AWS, Heroku].
* **Web Interface**:
  * A simple frontend allows users to input property details and view the predicted price.

# **Results**
The final model achieves an MAE of X and an RMSE of Y, indicating robust predictive accuracy. The model’s performance was evaluated against benchmark datasets, with satisfactory results on new unseen data.

# **Usage**
To use the API or access the web app:

1. Visit the [deployment link here]()
2. Use the form to input property details (location, size, etc.).
3. Submit to view the predicted property price.
4. Alternatively, clone the repository to run the project locally:
```
git clone https://github.com/Just-Aymz/Real-Estate-Prediction.git
cd Real-Estate-Prediction
pip install -r requirements.txt
python main.py
```

# **Technologies Used**
1. **Web Scraping**: Selenium
2. **Data Processing**: Pandas, NumPy
3. **Data Visualisation**: Matplotlib, Seaborn
4. **Modeling**: Scikit-Learn, XGBoost
5. **API Development**: FastAPI
6. **Deployment**: AWS, Docker, [your chosen platform]

# **Future Work**
* **Continuous Learning**: Implementing a pipeline for automated retraining with new data.
* **Enhanced Features**: Including additional predictors like economic indicators.
* **Feature Engineering**: Scrape more information to include more features to add useful features the model can use to predict more accurate scores.
* **User Interface Improvements**: Adding more detailed information and interactivity in the web app.

# **Contact**
For questions or collaborations, please reach out via:

**Email**: [your-email@example.com]()
**LinkedIn**: [Your LinkedIn Profile]()
