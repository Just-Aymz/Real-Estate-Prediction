from pydantic import BaseModel
from enum import Enum


# Use Enum library to limit the options for the suburb inputs
class Suburbs(Enum):
    ROSEBANK_AND_PARKTOWN = 'Rosebank and Parktown'
    FOURWAYS_SUNNINGHILL_AND_LONEHILL = 'Fourways, Sunninghill and Lonehill'
    MODDERFONTEIN = 'Modderfontein'


# Use Enum library to limit the options for the Property Type inputs
class PropertyTypes(Enum):
    APARTMENT = 'Apartment'
    FLAT = 'Flat'
    HOUSE = 'House'
    PENTHOUSE = 'Penthouse'
    SIMPLEX = 'Simplex'
    CLUSTER = 'Cluster'
    TOWNHOUSE = 'Townhouse'
    LOFT = 'Loft'
    STUDIO = 'Studio'
    DUPLEX = 'Duplex'
    BACHELOR = 'Bachelor'
    SMALL_HOLDING = 'Small Holding'


# Create a class for the input data from the user and the data type.
class PropertyInput(BaseModel):
    Floor_Size: float
    Bedrooms: float
    Bathrooms: float
    Lounges: float
    Property_Type: PropertyTypes
    Suburb: Suburbs
