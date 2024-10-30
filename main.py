from fastapi import FastAPI
from API.schemas import PropertyInput, PropertyTypes, Suburbs
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler


# Initialize FastAPI instance.
app = FastAPI()


# Read in .pkl files for predictive model, encoders, and scalers.
with open('trained_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


# column order
final_columns = [
    'Floor_size_(m²)', 'Bedrooms', 'Bathrooms', 'Lounges',
    'Property_type_Bachelor', 'Property_type_Cluster',
    'Property_type_Duplex', 'Property_type_Flat', 'Property_type_House',
    'Property_type_Loft', 'Property_type_Penthouse',
    'Property_type_Simplex', 'Property_type_Small Holding',
    'Property_type_Studio', 'Property_type_Townhouse',
    'suburb_Modderfontein', 'suburb_Rosebank and Parktown'
]


# Categories for one-hot encoding of suburb feature
def suburb_encoding(suburb: Suburbs):
    suburb_map = {
        Suburbs.MODDERFONTEIN: [1, 0],
        Suburbs.ROSEBANK_AND_PARKTOWN: [0, 1],
        Suburbs.FOURWAYS_SUNNINGHILL_AND_LONEHILL: [0, 0],
    }

    return suburb_map.get(suburb, [0]*2)


# Categories for one-hot encoding of property type feature
def property_type_encoding(prop_type: PropertyTypes):
    prop_map = {
        PropertyTypes.BACHELOR: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        PropertyTypes.CLUSTER: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        PropertyTypes.DUPLEX: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        PropertyTypes.FLAT: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        PropertyTypes.HOUSE: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        PropertyTypes.LOFT: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        PropertyTypes.PENTHOUSE: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        PropertyTypes.SIMPLEX: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        PropertyTypes.SMALL_HOLDING: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        PropertyTypes.STUDIO: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        PropertyTypes.TOWNHOUSE: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        PropertyTypes.APARTMENT: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }

    return prop_map.get(prop_type, [0]*11)


@app.post('/predict/')
async def user_input(input: PropertyInput) -> dict:
    # Store PropertyInput class as a dictionary
    model_features = dict(input)

    # Convert the input dictionary into a dataframe
    input_df = pd.DataFrame(model_features, index=[0])

    # Iterate over the dictionary features to find the features that need
    # to be transformed and scaled
    for feature in input_df:
        if feature in ['Floor_Size', 'Bathrooms', 'Lounges']:
            # Transform the highly skewed feature using log transformation
            log_transform = np.log1p(input_df[[feature]])

            # Instantiate the RobustScaler
            scaler = RobustScaler()

            # Fit and transform the data of the feature
            new_feature = scaler.fit_transform(log_transform)

            # Add the scaled feature to the scaled_data dictionary.
            input_df[feature] = new_feature.flatten()

        elif feature == 'Bedrooms':
            # Instantiate the RobustScaler
            scaler = RobustScaler()

            # Fit and transform the data of the feature
            new_feature = scaler.fit_transform(input_df[[feature]])

            # Add the scaled feature to the scaled_data dictionary.
            input_df[feature] = new_feature.flatten()

    # Store the order of the features of the encodings as they appear in the
    # trained model for property types
    encoded_prop_features = [
        'Property_type_Bachelor', 'Property_type_Cluster',
        'Property_type_Duplex', 'Property_type_Flat', 'Property_type_House',
        'Property_type_Loft', 'Property_type_Penthouse',
        'Property_type_Simplex', 'Property_type_Small Holding',
        'Property_type_Studio', 'Property_type_Townhouse',
    ]
    # Store the order of the features of the encodings as they appear in the
    # trained model for suburbs
    encoded_suburb_features = [
        'suburb_Modderfontein', 'suburb_Rosebank and Parktown'
    ]

    # Return the encoding of the property type based on the user input
    prop_type_encoding = property_type_encoding(prop_type=input.Property_Type)
    # Return the encoding of the subrb based on the user input
    sub_encoding = suburb_encoding(suburb=input.Suburb)

    # If the lengths of the encoded_prop_features and prop_type_encoding match,
    # then create a df
    if len(encoded_prop_features) == len(prop_type_encoding):
        prop_type_data = dict(zip(encoded_prop_features, prop_type_encoding))
        prop_type_df = pd.DataFrame(prop_type_data, index=[0])

    if len(encoded_suburb_features) == len(sub_encoding):
        sub_data = dict(zip(encoded_suburb_features, sub_encoding))
        suburb_df = pd.DataFrame(sub_data, index=[0])

    # Encode the categorical feature 'property_type'
    encoded_input_df = pd.concat([input_df, prop_type_df, suburb_df], axis=1)
    # Drop the categorical features from the dataframe
    encoded_input_df.drop(columns=['Property_Type', 'Suburb'], inplace=True)
    # Rename columns to match model training
    column_rename_map = {'Floor_Size': 'Floor_size_(m²)'}
    encoded_input_df.rename(columns=column_rename_map, inplace=True)
    # Reindex to ensure the correct order
    encoded_input_df = (
        encoded_input_df.reindex(columns=final_columns, fill_value=0)
    )

    # Make prediction
    prediction = model.predict(encoded_input_df)
    # Reverse the Robust scaling of prediction
    with open('API/price_robust_scaler.pkl', 'rb') as file:
        loaded_scaler = pickle.load(file)
    reverse_scaling_pred = (
        loaded_scaler.inverse_transform(prediction.reshape(1, -1))
    )

    # Reverse the log transformation to get the original price scale
    final_prediction = np.expm1(reverse_scaling_pred)

    return {'predicted_price': float(final_prediction[0])}
