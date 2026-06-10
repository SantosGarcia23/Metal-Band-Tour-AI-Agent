
#!/usr/bin/env python3
"""
Metal Band Touring Logistics Agent - Python Tools
Tools for Google Cloud Agent Builder to call:
1. Route & Mileage Calculator
2. Guarantee vs Door Split Payout Calculator
"""

from typing import List, Dict

# ============================================================================
# TOOL 1: Route & Mileage Calculator
# ============================================================================

def calculate_route_gas(
    origin: str,
    destination: str,
    gas_price_per_gallon: float = 3.50,
    van_fpg: float = 12.0
) -> Dict:
    """
    Calculate distance, drive time, and gas cost between two cities.
    
    For production: Replace demo distances with Google Maps Distance Matrix API:
    https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}
    """
    
    # Demo distances (real-world averages)
    demo_distances = {
        ("Chicago, IL", "Detroit, MI"): (450, 7.0),
        ("Detroit, MI", "Cleveland, OH"): (170, 2.8),
        ("Cleveland, OH", "Pittsburgh, PA"): (280, 4.5),
        ("Pittsburgh, PA", "Philadelphia, PA"): (350, 5.5),
        ("Philadelphia, PA", "New York, NY"): (110, 2.0),
        ("New York, NY", "Boston, MA"): (220, 4.0),
        ("Chicago, IL", "Milwaukee, WI"): (90, 1.5),
        ("Chicago, IL", "St. Louis, MO"): (300, 4.5),
    }
    
    route_key = (origin, destination)
    if route_key in demo_distances:
        distance_miles, duration_hours = demo_distances[route_key]
    else:
        distance_miles = 300
        duration_hours = distance_miles / 65
    
    gallons_needed = distance_miles / van_fpg
    gas_cost = gallons_needed * gas_price_per_gallon
    
    return {
        "origin": origin,
        "destination": destination,
        "distance_miles": round(distance_miles, 1),
        "duration_hours": round(duration_hours, 1),
        "gas_cost": round(gas_cost, 2),
        "route_summary": f"{origin} → {destination}: {distance_miles} miles, {duration_hours}h, ${gas_cost:.2f} gas"
    }


def calculate_multi_city_tour(
    cities: List[str],
    gas_price_per_gallon: float = 3.50,
    van_fpg: float = 12.0
) -> Dict:
    """Calculate total distance and gas cost for multi-city tour"""
    
    route_breakdown = []
    total_distance = 0
    total_gas_cost = 0
    
    for i in range(len(cities) - 1):
        segment = calculate_route_gas(cities[i], cities[i + 1], gas_price_per_gallon, van_fpg)
        route_breakdown.append(segment)
        total_distance += segment["distance_miles"]
        total_gas_cost += segment["gas_cost"]
    
    return {
        "cities": cities,
        "total_distance_miles": round(total_distance, 1),
        "total_gas_cost": round(total_gas_cost, 2),
        "route_breakdown": route_breakdown,
        "tour_summary": f"Total: {total_distance} miles, {len(route_breakdown)} segments, ${total_gas_cost:.2f} gas"
    }


# ============================================================================
# TOOL 2: Guarantee vs Door Split Payout Calculator
# ============================================================================

def calculate_band_payout(
    venue_capacity: int,
    ticket_price: float,
    expected_attendance_percent: float,
    guarantee: float,
    door_split_percent: float = 85.0
) -> Dict:
    """
    Calculate band's payout based on guarantee vs door split deal.
    
    Band gets the HIGHER of guarantee or door split.
    """
    
    attendance = int(venue_capacity * (expected_attendance_percent / 100))
    door_revenue = attendance * ticket_price
    band_door_payout = door_revenue * (door_split_percent / 100)
    
    if band_door_payout > guarantee:
        payout_type = "door"
        band_payout = band_door_payout
    else:
        payout_type = "guarantee"
        band_payout = guarantee
    
    return {
        "venue_capacity": venue_capacity,
        "ticket_price": ticket_price,
        "attendance": attendance,
        "guarantee": guarantee,
        "door_split_percent": door_split_percent,
        "door_revenue": round(door_revenue, 2),
        "band_door_payout": round(band_door_payout, 2),
        "band_payout": round(band_payout, 2),
        "payout_type": payout_type,
        "payout_summary": f"Band gets {payout_type}: ${band_payout:.2f}"
    }


def calculate_multi_venue_tour_payout(
    venues: List[Dict],
    door_split_percent: float = 85.0
) -> Dict:
    """Calculate total payout for multi-venue tour"""
    
    venue_breakdown = []
    total_payout = 0
    
    for venue in venues:
        payout = calculate_band_payout(
            venue_capacity=venue["capacity"],
            ticket_price=venue["ticket_price"],
            expected_attendance_percent=venue["attendance_percent"],
            guarantee=venue["guarantee"],
            door_split_percent=door_split_percent
        )
        payout["venue_name"] = venue["name"]
        venue_breakdown.append(payout)
        total_payout += payout["band_payout"]
    
    return {
        "num_venues": len(venues),
        "total_payout": round(total_payout, 2),
        "venue_breakdown": venue_breakdown,
        "tour_summary": f"{len(venues)} cities, ${total_payout:.2f} total payout"
    }
