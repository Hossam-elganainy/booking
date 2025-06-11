HOTEL_SCHEMA = {
    "hotel_name": {"type": "text", "required": True, "label": "Hotel Name"},
    "room_type": {
        "type": "choice",
        "required": True,
        "label": "Room Type",
        "choices": ["standard", "deluxe", "suite"]
    },
    "guests": {"type": "number", "required": True, "min": 1, "max": 4}
}

CAR_SCHEMA = {
    "pickup_location": {"type": "text", "required": True, "label": "Pickup Location"},
    "car_type": {
        "type": "choice",
        "required": True,
        "label": "Car Type",
        "choices": ["economy", "midsize", "luxury"]
    }
}