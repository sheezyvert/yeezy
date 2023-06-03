import time
import requests
import json
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from flask import Flask

app = Flask(__name__)

# List of product URLs to monitor
product_urls = [
    "https://www.adidas.co.za/IG9608.html",
    "https://www.adidas.co.za/BB5350.html",
    "https://www.adidas.co.za/F36640.html",
    "https://www.adidas.co.za/GZ0454.html",
    "https://www.adidas.co.za/ID4133.html",
    "https://www.adidas.co.za/GX9662.html",
    "https://www.adidas.co.za/FU7914.html",
    "https://www.adidas.co.za/ID4126.html",
    "https://www.adidas.co.za/EG7487.html",
    "https://www.adidas.co.za/CP9654.html",
    "https://www.adidas.co.za/HQ6448.html",
    "https://www.adidas.co.za/HQ7045.html",
    "https://www.adidas.co.za/ID1632.html",
    "https://www.adidas.co.za/HP5335.html",
    "https://www.adidas.co.za/GV6842.html",
    "https://www.adidas.co.za/HQ4540.html"
]

# Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1114205306935853188/lkhXcrVCBGHOlQhYJL-EbYzZMqMIPggK8DG_rYubyKPEWNwM8HWazkNlFnUraIIencMk"

@app.route('/')
def check_availability():
    while True:
        for url in product_urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Check for the 'data-tracking-view' attribute in the span element
            tracking_data = soup.find('span', {'class': 'd-none'}).get('data-tracking-view')
            tracking_data_json = json.loads(tracking_data)

            # Check the 'product_status' field
            if 'product_status' in tracking_data_json and tracking_data_json['product_status'] == 'IN STOCK':
                # The product is available, send a message to the Discord channel
                webhook = DiscordWebhook(url=webhook_url, content=f'Product is now available: {url}')
                webhook.execute()

        # Wait for a while before checking the product pages again to avoid hitting rate limits
        time.sleep(15)

    return "Running..."

if __name__ == '__main__':
    app.run()
