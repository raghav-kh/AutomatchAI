"""
Seeds a realistic demo catalog: manufacturers + cars + variants with full
specifications and AI attributes, so /recommendations, /compare,
/variants/{id}/ownership-cost, and /variants/{id}/alternatives all have
real, meaningful results to show -- not empty states.

Deliberately includes the SRS's own example scenarios so a demo/video can
recreate them directly:
- "SUV under 10 lakh -> Citroen Basalt shows up too" (Section 1: Problem Statement)
- "XUV 3XO -> you may also consider the Honda Elevate" (Section 4.7)

Idempotent: safe to re-run, skips manufacturers/cars/variants that already
exist by name.

Run with:
    python -m scripts.seed_demo_catalog
"""

from app.core.database import SessionLocal, Base, engine
from app import models  # noqa: F401
from app.models.manufacturer import Manufacturer, DataSourceType
from app.models.car import Car
from app.models.variant import Variant
from app.models.specification import Specification
from app.models.ai_attributes import AIAttributes

# Each manufacturer: name, country, data_source_type, confidence_score, cars[]
# Each car: model, body_type, launch_year, variants[]
# Each variant: name + core fields + specifications + ai_attributes
DEMO_CATALOG = [
    {
        "name": "Maruti Suzuki",
        "country": "India",
        "data_source_type": DataSourceType.SCRAPER,
        "confidence_score": 0.5,
        "cars": [
            {
                "model": "Swift",
                "body_type": "Hatchback",
                "launch_year": 2024,
                "variants": [
                    {
                        "variant_name": "VXI",
                        "price": 750000,
                        "fuel": "Petrol",
                        "transmission": "Manual",
                        "engine": "1197cc",
                        "power": "82 bhp",
                        "mileage": 22.0,
                        "specifications": dict(seating=5, airbags=2, safety_rating=4, ground_clearance=163, boot_space=268, length=3860, width=1735, height=1520),
                        "ai_attributes": dict(ride_quality=6, city_friendliness=9, highway_comfort=6, maintenance_level=2, resale_value=8, service_network=10, beginner_friendly=True, family_score=6, elderly_friendly=False, premium_feel=4, offroad_capability=2),
                    },
                    {
                        "variant_name": "CNG VXI",
                        "price": 830000,
                        "fuel": "CNG",
                        "transmission": "Manual",
                        "engine": "1197cc",
                        "power": "77 bhp",
                        "mileage": 30.6,
                        "specifications": dict(seating=5, airbags=2, safety_rating=4, ground_clearance=163, boot_space=208, length=3860, width=1735, height=1520),
                        "ai_attributes": dict(ride_quality=6, city_friendliness=9, highway_comfort=5, maintenance_level=2, resale_value=7, service_network=10, beginner_friendly=True, family_score=6, elderly_friendly=False, premium_feel=3, offroad_capability=2),
                    },
                ],
            },
        ],
    },
    {
        "name": "Tata Motors",
        "country": "India",
        "data_source_type": DataSourceType.SCRAPER,
        "confidence_score": 0.6,
        "scraper_module": "app.pipeline.scrapers.tata.TataScraper",
        "cars": [
            {
                "model": "Nexon",
                "body_type": "SUV",
                "launch_year": 2024,
                "variants": [
                    {
                        "variant_name": "XZ Plus",
                        "price": 950000,
                        "fuel": "Petrol",
                        "transmission": "Manual",
                        "engine": "1199cc",
                        "power": "118 bhp",
                        "mileage": 17.5,
                        "specifications": dict(seating=5, airbags=6, safety_rating=5, ground_clearance=209, boot_space=350, length=3993, width=1811, height=1616),
                        "ai_attributes": dict(ride_quality=7, city_friendliness=8, highway_comfort=6, maintenance_level=3, resale_value=7, service_network=8, beginner_friendly=True, family_score=7, elderly_friendly=True, premium_feel=5, offroad_capability=5),
                    },
                ],
            },
            {
                "model": "Nexon EV",
                "body_type": "SUV",
                "launch_year": 2024,
                "variants": [
                    {
                        "variant_name": "Long Range",
                        "price": 1600000,
                        "fuel": "Electric",
                        "transmission": "Automatic",
                        "power": "127 bhp",
                        "mileage": 8.0,  # km/kWh
                        "specifications": dict(seating=5, airbags=6, safety_rating=5, ground_clearance=190, boot_space=350, length=3993, width=1811, height=1616),
                        "ai_attributes": dict(ride_quality=7, city_friendliness=9, highway_comfort=5, maintenance_level=2, resale_value=6, service_network=6, beginner_friendly=True, family_score=6, elderly_friendly=True, premium_feel=6, offroad_capability=3),
                    },
                ],
            },
            {
                "model": "Tiago",
                "body_type": "Hatchback",
                "launch_year": 2023,
                "variants": [
                    {
                        "variant_name": "XZ",
                        "price": 680000,
                        "fuel": "Petrol",
                        "transmission": "Manual",
                        "engine": "1199cc",
                        "power": "85 bhp",
                        "mileage": 19.0,
                        "specifications": dict(seating=5, airbags=2, safety_rating=4, ground_clearance=172, boot_space=242, length=3765, width=1677, height=1536),
                        "ai_attributes": dict(ride_quality=6, city_friendliness=8, highway_comfort=6, maintenance_level=2, resale_value=6, service_network=8, beginner_friendly=True, family_score=6, elderly_friendly=False, premium_feel=4, offroad_capability=2),
                    },
                ],
            },
        ],
    },
    {
        "name": "Mahindra",
        "country": "India",
        "data_source_type": DataSourceType.API,
        "confidence_score": 0.9,
        "cars": [
            {
                "model": "XUV 3XO",
                "body_type": "SUV",
                "launch_year": 2024,
                "variants": [
                    {
                        "variant_name": "AX7L",
                        "price": 1400000,
                        "fuel": "Petrol",
                        "transmission": "Manual",
                        "engine": "1197cc",
                        "power": "129 bhp",
                        "mileage": 16.0,
                        "specifications": dict(seating=5, airbags=6, safety_rating=4, ground_clearance=201, boot_space=364, length=3990, width=1821, height=1647),
                        "ai_attributes": dict(ride_quality=6, city_friendliness=7, highway_comfort=6, maintenance_level=6, resale_value=5, service_network=7, beginner_friendly=False, family_score=6, elderly_friendly=False, premium_feel=5, offroad_capability=6),
                    },
                ],
            },
            {
                "model": "XUV700",
                "body_type": "SUV",
                "launch_year": 2024,
                "variants": [
                    {
                        "variant_name": "AX7L",
                        "price": 2400000,
                        "fuel": "Diesel",
                        "transmission": "Automatic",
                        "engine": "2198cc",
                        "power": "182 bhp",
                        "mileage": 14.0,
                        "specifications": dict(seating=7, airbags=7, safety_rating=5, ground_clearance=200, boot_space=240, length=4695, width=1890, height=1755),
                        "ai_attributes": dict(ride_quality=8, city_friendliness=5, highway_comfort=9, maintenance_level=5, resale_value=8, service_network=9, beginner_friendly=False, family_score=9, elderly_friendly=True, premium_feel=8, offroad_capability=7),
                    },
                ],
            },
        ],
    },
    {
        "name": "Honda",
        "country": "Japan",
        "data_source_type": DataSourceType.API,
        "confidence_score": 0.85,
        "cars": [
            {
                "model": "Elevate",
                "body_type": "SUV",
                "launch_year": 2024,
                "variants": [
                    {
                        "variant_name": "VX",
                        "price": 1450000,
                        "fuel": "Petrol",
                        "transmission": "Manual",
                        "engine": "1498cc",
                        "power": "121 bhp",
                        "mileage": 15.2,
                        "specifications": dict(seating=5, airbags=6, safety_rating=5, ground_clearance=220, boot_space=458, length=4312, width=1790, height=1650),
                        "ai_attributes": dict(ride_quality=8, city_friendliness=6, highway_comfort=7, maintenance_level=3, resale_value=8, service_network=9, beginner_friendly=True, family_score=7, elderly_friendly=True, premium_feel=8, offroad_capability=4),
                    },
                ],
            },
            {
                "model": "City",
                "body_type": "Sedan",
                "launch_year": 2023,
                "variants": [
                    {
                        "variant_name": "V CVT",
                        "price": 1350000,
                        "fuel": "Petrol",
                        "transmission": "Automatic",
                        "engine": "1498cc",
                        "power": "119 bhp",
                        "mileage": 18.4,
                        "specifications": dict(seating=5, airbags=6, safety_rating=5, ground_clearance=165, boot_space=506, length=4549, width=1748, height=1489),
                        "ai_attributes": dict(ride_quality=8, city_friendliness=6, highway_comfort=8, maintenance_level=3, resale_value=8, service_network=9, beginner_friendly=True, family_score=7, elderly_friendly=True, premium_feel=7, offroad_capability=1),
                    },
                ],
            },
        ],
    },
    {
        "name": "Citroen",
        "country": "France",
        "data_source_type": DataSourceType.SCRAPER,
        "confidence_score": 0.4,
        "cars": [
            {
                "model": "Basalt",
                "body_type": "SUV",
                "launch_year": 2024,
                "variants": [
                    {
                        "variant_name": "Max",
                        "price": 950000,
                        "fuel": "Petrol",
                        "transmission": "Manual",
                        "engine": "1199cc",
                        "power": "110 bhp",
                        "mileage": 19.3,
                        "specifications": dict(seating=5, airbags=4, safety_rating=4, ground_clearance=200, boot_space=470, length=4352, width=1765, height=1600),
                        "ai_attributes": dict(ride_quality=7, city_friendliness=7, highway_comfort=7, maintenance_level=5, resale_value=5, service_network=4, beginner_friendly=True, family_score=7, elderly_friendly=True, premium_feel=6, offroad_capability=4),
                    },
                ],
            },
        ],
    },
    {
        "name": "Hyundai",
        "country": "South Korea",
        "data_source_type": DataSourceType.API,
        "confidence_score": 0.8,
        "cars": [
            {
                "model": "i20",
                "body_type": "Hatchback",
                "launch_year": 2023,
                "variants": [
                    {
                        "variant_name": "Sportz",
                        "price": 850000,
                        "fuel": "Petrol",
                        "transmission": "Manual",
                        "engine": "1197cc",
                        "power": "83 bhp",
                        "mileage": 20.35,
                        "specifications": dict(seating=5, airbags=2, safety_rating=5, ground_clearance=170, boot_space=311, length=3995, width=1775, height=1505),
                        "ai_attributes": dict(ride_quality=7, city_friendliness=8, highway_comfort=6, maintenance_level=3, resale_value=7, service_network=9, beginner_friendly=True, family_score=6, elderly_friendly=False, premium_feel=6, offroad_capability=2),
                    },
                ],
            },
            {
                "model": "Creta",
                "body_type": "SUV",
                "launch_year": 2024,
                "variants": [
                    {
                        "variant_name": "SX",
                        "price": 1550000,
                        "fuel": "Petrol",
                        "transmission": "Automatic",
                        "engine": "1497cc",
                        "power": "113 bhp",
                        "mileage": 17.4,
                        "specifications": dict(seating=5, airbags=6, safety_rating=5, ground_clearance=190, boot_space=433, length=4330, width=1790, height=1635),
                        "ai_attributes": dict(ride_quality=8, city_friendliness=7, highway_comfort=8, maintenance_level=4, resale_value=8, service_network=9, beginner_friendly=True, family_score=7, elderly_friendly=True, premium_feel=7, offroad_capability=5),
                    },
                ],
            },
        ],
    },
    {
        "name": "Kia",
        "country": "South Korea",
        "data_source_type": DataSourceType.SCRAPER,
        "confidence_score": 0.75,
        "cars": [
            {
                "model": "Sonet",
                "body_type": "SUV",
                "launch_year": 2024,
                "variants": [
                    {
                        "variant_name": "HTX Diesel",
                        "price": 1050000,
                        "fuel": "Diesel",
                        "transmission": "Manual",
                        "engine": "1493cc",
                        "power": "114 bhp",
                        "mileage": 19.0,
                        "specifications": dict(seating=5, airbags=6, safety_rating=5, ground_clearance=190, boot_space=385, length=3995, width=1790, height=1642),
                        "ai_attributes": dict(ride_quality=7, city_friendliness=7, highway_comfort=7, maintenance_level=4, resale_value=6, service_network=7, beginner_friendly=False, family_score=6, elderly_friendly=False, premium_feel=6, offroad_capability=4),
                    },
                ],
            },
        ],
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    stats = {"manufacturers": 0, "cars": 0, "variants": 0, "skipped": 0}

    try:
        for m_data in DEMO_CATALOG:
            manufacturer = db.query(Manufacturer).filter(Manufacturer.name == m_data["name"]).first()
            if manufacturer is None:
                manufacturer = Manufacturer(
                    name=m_data["name"],
                    country=m_data.get("country"),
                    data_source_type=m_data["data_source_type"],
                    confidence_score=m_data.get("confidence_score"),
                    scraper_module=m_data.get("scraper_module"),
                    has_open_api=(m_data["data_source_type"] == DataSourceType.API),
                )
                db.add(manufacturer)
                db.flush()
                stats["manufacturers"] += 1

            for c_data in m_data["cars"]:
                car = (
                    db.query(Car)
                    .filter(Car.manufacturer_id == manufacturer.id, Car.model == c_data["model"])
                    .first()
                )
                if car is None:
                    car = Car(
                        manufacturer_id=manufacturer.id,
                        model=c_data["model"],
                        body_type=c_data.get("body_type"),
                        launch_year=c_data.get("launch_year"),
                    )
                    db.add(car)
                    db.flush()
                    stats["cars"] += 1

                for v_data in c_data["variants"]:
                    existing = (
                        db.query(Variant)
                        .filter(Variant.car_id == car.id, Variant.variant_name == v_data["variant_name"])
                        .first()
                    )
                    if existing is not None:
                        stats["skipped"] += 1
                        continue

                    variant = Variant(
                        car_id=car.id,
                        variant_name=v_data["variant_name"],
                        price=v_data.get("price"),
                        fuel=v_data.get("fuel"),
                        transmission=v_data.get("transmission"),
                        engine=v_data.get("engine"),
                        power=v_data.get("power"),
                        torque=v_data.get("torque"),
                        mileage=v_data.get("mileage"),
                    )
                    db.add(variant)
                    db.flush()

                    if "specifications" in v_data:
                        db.add(Specification(variant_id=variant.id, **v_data["specifications"]))
                    if "ai_attributes" in v_data:
                        db.add(AIAttributes(variant_id=variant.id, **v_data["ai_attributes"]))

                    stats["variants"] += 1

        db.commit()
    finally:
        db.close()

    print(
        f"Demo catalog seeded: {stats['manufacturers']} manufacturers, "
        f"{stats['cars']} cars, {stats['variants']} variants added "
        f"({stats['skipped']} variants already present, skipped)."
    )


if __name__ == "__main__":
    seed()
