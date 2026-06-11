import os
import json
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

# --- eBay Authentication ---

def get_ebay_token():
    credentials = f"{os.getenv('EBAY_CLIENT_ID')}:{os.getenv('EBAY_CLIENT_SECRET')}"
    encoded = base64.b64encode(credentials.encode()).decode()

    response = requests.post(
        "https://api.ebay.com/identity/v1/oauth2/token",
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data="grant_type=client_credentials&scope=https://api.ebay.com/oauth/api_scope"
    )

    return response.json().get("access_token")


# --- eBay Browse API ---

def search_listings(query: str, max_results: int = 5):
    """
    Uses eBay Browse API to get active listings sorted by lowest price.
    """
    token = get_ebay_token()

    response = requests.get(
        "https://api.ebay.com/buy/browse/v1/item_summary/search",
        headers={
            "Authorization": f"Bearer {token}",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_GB",
            "Content-Type": "application/json"
        },
        params={
            "q": query,
            "category_ids": "261328",
            "sort": "price",
            "limit": max_results
        }
    )

    data = response.json()

    try:
        items = data.get("itemSummaries", [])
        results = []
        for item in items:
            price = float(item["price"]["value"])
            shipping = 0.0
            if item.get("shippingOptions"):
                shipping = float(
                    item["shippingOptions"][0]
                    .get("shippingCost", {})
                    .get("value", 0)
                )
            results.append({
                "title": item["title"],
                "price_gbp": round(price, 2),
                "shipping_gbp": round(shipping, 2),
                "total_gbp": round(price + shipping, 2),
                "condition": item.get("condition", "Unknown"),
                "url": item.get("itemWebUrl", "")
            })
        return results
    except (KeyError, IndexError):
        return []


# --- Tool definitions ---

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "research_card_value",
            "description": "Research the estimated resale value of a sports card based on active eBay listings sorted by lowest price",
            "parameters": {
                "type": "object",
                "properties": {
                    "player": {"type": "string", "description": "Player name e.g. Jude Bellingham"},
                    "year": {"type": "string", "description": "Card year e.g. 2023"},
                    "set": {"type": "string", "description": "Card set e.g. Topps Chrome UEFA"},
                    "parallel": {"type": "string", "description": "Parallel type e.g. Gold Refractor /50"},
                    "condition": {"type": "string", "description": "Card condition e.g. Near Mint"}
                },
                "required": ["player", "set"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_break_roi",
            "description": "Calculate the ROI of a box break given card values and box cost",
            "parameters": {
                "type": "object",
                "properties": {
                    "box_cost": {"type": "number", "description": "What you paid for the box in GBP"},
                    "card_values": {
                        "type": "array",
                        "description": "List of cards with estimated values",
                        "items": {
                            "type": "object",
                            "properties": {
                                "card": {"type": "string"},
                                "estimated_value": {"type": "number"}
                            }
                        }
                    },
                    "ebay_fee_percent": {"type": "number", "description": "eBay fee percentage, default 12.8"}
                },
                "required": ["box_cost", "card_values"]
            }
        }
    }
]


# --- Tool implementations ---

def research_card_value(player, set, year=None, parallel=None, condition=None):
    """
    Searches eBay active listings to estimate card value.
    """
    query_parts = [player, set]
    if year:
        query_parts.append(year)
    if parallel:
        query_parts.append(parallel)

    query = " ".join(query_parts)
    print(f"🔍 Searching eBay for: {query}")

    listings = search_listings(query)

    if not listings:
        return {
            "player": player,
            "query": query,
            "estimated_value_gbp": None,
            "message": "No listings found — try a broader search"
        }

    prices = [item["total_gbp"] for item in listings]
    avg_price = round(sum(prices) / len(prices), 2)
    min_price = round(min(prices), 2)
    max_price = round(max(prices), 2)

    return {
        "player": player,
        "parallel": parallel or "Base",
        "query_used": query,
        "listings_found": len(listings),
        "average_listing_price_gbp": avg_price,
        "min_listing_price_gbp": min_price,
        "max_listing_price_gbp": max_price,
        "note": "Prices based on active listings sorted by lowest price — use as a conservative estimate",
        "sample_listings": listings[:3]
    }


def calculate_break_roi(box_cost, card_values, ebay_fee_percent=12.8):
    total_value = sum(c["estimated_value"] for c in card_values)
    fees = total_value * (ebay_fee_percent / 100)
    net_profit = total_value - fees - box_cost

    return {
        "box_cost_gbp": box_cost,
        "total_estimated_value_gbp": round(total_value, 2),
        "ebay_fees_gbp": round(fees, 2),
        "net_profit_gbp": round(net_profit, 2),
        "roi_percent": round((net_profit / box_cost) * 100, 1),
        "verdict": "Profitable" if net_profit > 0 else "Loss"
    }


def handle_tool_call(tool_name, tool_args):
    if tool_name == "research_card_value":
        return research_card_value(**tool_args)
    elif tool_name == "calculate_break_roi":
        return calculate_break_roi(**tool_args)
    else:
        return {"error": f"Unknown tool: {tool_name}"}