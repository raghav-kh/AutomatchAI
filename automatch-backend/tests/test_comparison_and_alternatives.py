import pytest

from app.crud import manufacturer as manufacturer_crud
from app.crud import car as car_crud
from app.crud import variant as variant_crud
from app.schemas.manufacturer import ManufacturerCreate
from app.schemas.car import CarCreate
from app.schemas.variant import VariantCreate
from app.schemas.specification import SpecificationCreate, AIAttributesCreate
from app.recommendation.comparison import compare_variants
from app.recommendation.alternative import find_alternatives


@pytest.fixture()
def two_variants(db_session):
    m = manufacturer_crud.create_manufacturer(db_session, ManufacturerCreate(name="Test OEM"))
    car1 = car_crud.create_car(db_session, CarCreate(model="XUV 3XO", body_type="SUV", manufacturer_id=m.id))
    car2 = car_crud.create_car(db_session, CarCreate(model="Elevate", body_type="SUV", manufacturer_id=m.id))

    v1 = variant_crud.create_variant(
        db_session,
        car1.id,
        VariantCreate(
            variant_name="AX7",
            price=1400000,
            specifications=SpecificationCreate(safety_rating=4, boot_space=300),
            ai_attributes=AIAttributesCreate(premium_feel=5.0, resale_value=5.0, maintenance_level=6.0),
        ),
    )
    v2 = variant_crud.create_variant(
        db_session,
        car2.id,
        VariantCreate(
            variant_name="VX",
            price=1450000,
            specifications=SpecificationCreate(safety_rating=5, boot_space=458),
            ai_attributes=AIAttributesCreate(premium_feel=8.0, resale_value=8.0, maintenance_level=3.0),
        ),
    )
    return v1, v2


def test_compare_variants_returns_rows_in_requested_order(db_session, two_variants):
    v1, v2 = two_variants
    rows = compare_variants(db_session, [v2.id, v1.id])
    assert [r.variant_id for r in rows] == [v2.id, v1.id]
    assert rows[0].car_model == "Elevate"


def test_compare_variants_raises_on_missing_id(db_session, two_variants):
    v1, _ = two_variants
    with pytest.raises(ValueError):
        compare_variants(db_session, [v1.id, 99999])


def test_alternatives_surfaces_better_variant_with_reasons(db_session, two_variants):
    v1, v2 = two_variants  # v2 (Elevate) is better on refinement, resale, maintenance
    results = find_alternatives(db_session, v1)
    assert len(results) == 1
    alt = results[0]
    assert alt.car_model == "Elevate"
    assert "Better refinement" in alt.reasons
    assert "Better resale value" in alt.reasons
    assert "More reliable, lower maintenance" in alt.reasons


def test_alternatives_excludes_same_car_siblings(db_session):
    m = manufacturer_crud.create_manufacturer(db_session, ManufacturerCreate(name="Same Car OEM"))
    car = car_crud.create_car(db_session, CarCreate(model="Nexon", body_type="SUV", manufacturer_id=m.id))
    v1 = variant_crud.create_variant(
        db_session, car.id, VariantCreate(variant_name="XM", price=900000, ai_attributes=AIAttributesCreate(premium_feel=3.0))
    )
    variant_crud.create_variant(
        db_session, car.id, VariantCreate(variant_name="XZ Plus", price=950000, ai_attributes=AIAttributesCreate(premium_feel=9.0))
    )
    # XZ Plus is a trim of the same car -- should not be suggested as an "alternative"
    assert find_alternatives(db_session, v1) == []


def test_alternatives_empty_when_no_price(db_session, two_variants):
    v1, _ = two_variants
    v1.price = None
    assert find_alternatives(db_session, v1) == []


def test_alternatives_respects_price_band(db_session):
    m = manufacturer_crud.create_manufacturer(db_session, ManufacturerCreate(name="Band OEM"))
    car1 = car_crud.create_car(db_session, CarCreate(model="Cheap SUV", body_type="SUV", manufacturer_id=m.id))
    car2 = car_crud.create_car(db_session, CarCreate(model="Expensive SUV", body_type="SUV", manufacturer_id=m.id))

    v1 = variant_crud.create_variant(
        db_session, car1.id, VariantCreate(variant_name="Base", price=800000, ai_attributes=AIAttributesCreate(premium_feel=3.0))
    )
    variant_crud.create_variant(
        db_session,
        car2.id,
        VariantCreate(variant_name="Top", price=3000000, ai_attributes=AIAttributesCreate(premium_feel=9.0)),  # way out of price band
    )
    assert find_alternatives(db_session, v1) == []
