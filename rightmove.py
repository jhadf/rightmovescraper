import requests
import json
import random
import time
import re

url = "https://api.rightmove.co.uk/api/property-listing"

querystring = {
    "apiApplication":"IPHONE",
    "radius":"0.25",
    "includeUnavailableProperties":"false",
    "maxBedrooms":"2",
    "dontShow":"retirement,houseShare",
    "minBedrooms":"2",
    "propertyTypes":"flat,terraced,detached,semi-detached",
    "maxPrice":"3000",
    "page":"1",
    "channel":"RENT",
    "sortBy":"newestListed",
    "numberOfPropertiesPerPage":"500",
    "locationIdentifier":"OUTCODE^2332"
}

payload = ""
headers = {
    "Accept": "*/*",
    "Accept-Language": "en-GB;q=1",
    "Connection": "keep-alive",
    "User-Agent": "Rightmove/8.8 (iPhone; iOS 16.0; Scale/3.00)"
}

discord_webhook_url = '#'  # replace this with your actual Discord Webhook URL

seen_properties = set()  # to keep track of properties already posted

while True:
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    properties = response.json()["properties"]

    for property in properties:
        # Only post the property if we haven't seen it before
        if property['identifier'] not in seen_properties:
            seen_properties.add(property['identifier'])

            property_id = re.search(r'(\d+)/\d+_', property['photoThumbnailUrl']).group(1)
            property_url = f"https://www.rightmove.co.uk/properties/{property_id}/"

            data = {
                "embeds": [
                    {
                        "title": f"New property listed at {property['address']}",
                        "description": f"Price: {property['displayPrices'][0]['displayPrice']}\nSummary: {property['summary']}",
                        "url": property_url,
                        "image": {"url": property['photoThumbnailUrl']},
                        "color": 242424
                    }
                ]
            }

            result = requests.post(discord_webhook_url, json=data)

            if result.status_code == 204:
                print(f"Successfully sent message for property: {property['address']}")
            else:
                print(f"Failed to send message for property: {property['address']}")

    # Sleep for a random interval between 30 and 90 seconds before checking for new properties
    time.sleep(random.randint(30, 90))
