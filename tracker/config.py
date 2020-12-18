from dotenv import load_dotenv
import os
from pathlib import Path

colab=False
if colab:
    ENV_PATH = Path("/content/drive/secrets", ".env")
    ROOT = Path("/content/drive/Shared drives/WDCEP/COVID-tracker")
else:
    ROOT = Path(os.environ['NLT'],"WDCEP-COVID-tracker")
    ENV_PATH = Path(ROOT, "tracker", ".env")

load_dotenv(ENV_PATH)

# yelp
# documentation: https://www.yelp.com/developers/documentation/v3/business

YELP_API = os.getenv("YELP_API")
YELP_HOST = "https://api.yelp.com"
YELP_BIZSEARCH = "/v3/businesses/search"
YELP_BIZDETAILS = "/v3/businesses/{}"  # business ID
TOP_DC_CATS = (
    "homeservices",
    "health",
    "restaurants",
    "shopping",
    "localservices",
    "food",
    "beautysvc",
    "realestate",
    "physicians",
    "auto",
    "eventservices",
    "professional",
    "active",
    "hotelstravel",
    "hair",
    "dentists",
    "fashion",
    "education",
    "financialservices",
    "fitness",
    "bars",
    "arts",
    "autorepair",
    "homeandgarden",
)
YELP_OPATH = Path(ROOT, "data", "yelp_dcbiz_sample.dill"
)
REST_OPATH = Path(ROOT, "data", "yelp_dcrest_sample.dill"
)

OPENTABLE_SEATEDYOY_PATH = Path(ROOT, "data", "opentable","YoY_Seated_Diner_Data.csv"
)

PLOT_DIR = Path(ROOT, "tracker","plots"
)
PLOT_DIR.mkdir(exist_ok=True)

# geo
DC_ZIPS = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Location_WebMercator/MapServer/4/query?where=1%3D1&outFields=*&outSR=4326&f=json"
CRS = "epsg:4326"

CITIES = Path(ROOT, 'data','cities.csv')