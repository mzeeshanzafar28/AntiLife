import requests

def lookup_mac(mac_address):
    """
    Lookup MAC address vendor using macvendors.co API.
    """
    try:
        url = f"https://macvendors.co/api/{mac_address}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and 'company' in data['result']:
                return f"Vendor: {data['result']['company']}\nAddress: {data['result'].get('address', 'N/A')}"
            else:
                return "Vendor not found."
        else:
            return "API Error"
    except Exception as e:
        return f"Error: {e}"
