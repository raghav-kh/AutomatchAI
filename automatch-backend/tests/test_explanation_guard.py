from app.recommendation.explanation_guard import is_consistent
from app.recommendation.reasons import trade_off_component_keys, TRADE_OFF_TEMPLATES


def test_consistent_when_no_weak_components():
    text = "This car is a great fit for your family and budget."
    assert is_consistent(text, []) is True


def test_flags_contradiction_praising_a_trade_off():
    text = "It has an excellent service network across the country, which is a big plus."
    assert is_consistent(text, ["service_network"]) is False


def test_does_not_flag_unrelated_praise():
    text = "It has excellent safety ratings and a strong resale value."
    # service_network is the weak spot, but the praise here is about safety/resale, not service network
    assert is_consistent(text, ["service_network"]) is True


def test_does_not_flag_when_trade_off_mentioned_without_positive_marker():
    text = "Note that the service network is somewhat limited in smaller towns."
    assert is_consistent(text, ["service_network"]) is True


def test_trade_off_component_keys_maps_back_correctly():
    trade_offs = [TRADE_OFF_TEMPLATES["service_network"], TRADE_OFF_TEMPLATES["resale_value"]]
    keys = trade_off_component_keys(trade_offs)
    assert set(keys) == {"service_network", "resale_value"}


def test_unknown_trade_off_text_ignored_gracefully():
    keys = trade_off_component_keys(["some text not in the template map"])
    assert keys == []
