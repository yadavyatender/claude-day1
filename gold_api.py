import requests
import urllib3
import logging
from datetime import datetime

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_gold_rate():
    """
    Fetch live 22K gold price from APIs.
    Returns price per gram in USD only.
    """
    # Try GoldAPI first
    result = fetch_from_goldapi()
    if result:
        return result
    
    # Fallback to alternative sources
    result = fetch_from_metals_live()
    if result:
        return result
    
    # If all fail, use cached fallback
    return fetch_gold_rate_fallback()

def fetch_from_goldapi():
    """
    Fetch from GoldAPI (free tier available).
    This API provides accurate 22K gold prices.
    """
    try:
        url = "https://www.goldapi.io/api/XAU/USD"
        headers = {"x-access-token": "googlecolab"}
        
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        data = response.json()
        
        if 'price_gram_22k' in data:
            price_usd_22k = data['price_gram_22k']
            
            logger.info(f"✓ Gold 22K rate from GoldAPI: ${price_usd_22k:.2f} USD/gram")
            
            return {
                'price_usd': round(price_usd_22k, 2),
                'raw_response': data,
                'timestamp': datetime.now().isoformat(),
                'source': 'GoldAPI'
            }
    except Exception as e:
        logger.debug(f"GoldAPI failed: {e}")
        return None

def fetch_from_metals_live():
    """
    Fallback to metals.live API with 22K conversion to USD.
    """
    try:
        url = "https://api.metals.live/v1/spot/gold"
        
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        data = response.json()
        
        # Get 24K price in USD
        price_usd_per_oz_24k = data.get('gold', None)
        
        if price_usd_per_oz_24k is None:
            return None
        
        # Convert troy oz to grams (1 oz = 31.1035 grams)
        price_usd_per_gram_24k = price_usd_per_oz_24k / 31.1035
        
        # Convert 24K to 22K (multiply by purity factor 22/24)
        price_usd_per_gram_22k = price_usd_per_gram_24k * (22 / 24)
        
        logger.info(f"✓ Gold 22K rate from Metals.live: ${price_usd_per_gram_22k:.2f} USD/gram")
        
        return {
            'price_usd': round(price_usd_per_gram_22k, 2),
            'raw_response': data,
            'timestamp': datetime.now().isoformat(),
            'source': 'Metals.live'
        }
    except Exception as e:
        logger.debug(f"Metals.live failed: {e}")
        return None

def fetch_gold_rate_fallback():
    """
    Fallback to cached 22K gold value when API is unavailable.
    """
    logger.warning("⚠️ Using fallback gold rate (APIs unavailable)")
    # Approximate fallback price in USD
    price_usd = 65.50  # $65.50 per gram for 22K gold
    
    return {
        'price_usd': price_usd,
        'raw_response': {'fallback': True},
        'timestamp': datetime.now().isoformat(),
        'source': 'Fallback'
    }
