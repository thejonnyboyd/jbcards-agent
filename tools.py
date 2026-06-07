import json

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "research_and_card_value",
            "description": "Research the estimated resale value of a sports card based on recent eBay sold listings",
            "parameters": {
                "type": "object",
                "properties": {
                    "player": {"type": "string", "description": "Player name e.g. Jude Bellingham"},
                    "year": {"type": "string", "description": "Card year e.g. 2025/2026"},
                    "set": {"type": "string", "description": "Card set e.g. Topps Chrome UEFA Club Competitions"},
                    "parallel": {"type": "string", "description": "Parallel type e.g. Gold Refactor /50"},
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
                        "description": "List of estimated card values in GBP",
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

def research_card_value(player, set, year=None, parallel=None, condition=None):
    """
    Stub for now - replace with real eBay Browse API call later.
    """
    return {
        "player": player,
        "set": set,
        "parallel": parallel or "Base",
        "estimated_value_gbp": "Research not yet connected - please estimate manually",
        "note": "Plug in eBay Browse API here for live data"
    }

def calculate_break_roi(box_cost, card_values, ebay_fee_percent=12.8):
    total_value = sum(c["estimated_value"] for c in card_values)
    fees = total_value * (ebay_fee_percent / 100)
    net_profit = total_value - fees - box_cost

    return{
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