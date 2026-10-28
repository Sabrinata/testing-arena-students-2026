"""Starter tests for the weather module.

These tests deliberately cover only ordinary examples. They show how pytest works,
but they are not a sufficient test suite for the specification in SPECIFICATION.md.
"""

from weather import (
    average_temperature,
    filter_by_temperature,
    hottest_measurement,
    parse_measurement,
    parse_time,
)
import pytest

def test_parse_time_regular_time():
    assert parse_time("14:21") == 861
    assert parse_time("00:00") == 0
    assert parse_time("23:59") == 1439

def test_parse_time_zeros():
    assert parse_time("9:5") == 545
    assert parse_time("09:5") == 545
    assert parse_time("9:05") == 545
    assert parse_time("09:05") == 545

def test_parse_time_ValueError():
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        parse_time("-3:9")
        parse_time("2.5:7")
        parse_time("fünfzehn:4")
        parse_time("3:fünfzehn")
        parse_time("4:-7")
        parse_time("7:4.5")
    with pytest.raises(ValueError, match="Time must have HH:MM format."):
        parse_time("6.5")
        parse_time("6:5:6")
        parse_time("5;8")
        parse_time("1")
    with pytest.raises(ValueError, match="Hour must be between 0 and 23."):
        parse_time("24:7")
    with pytest.raises(ValueError, match="Minute must be between 0 and 59."):
        parse_time("12:60")
    

def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)
    assert parse_measurement("Köln;14:21;99.9") == ("Köln", 861, 99.9)

def test_parse_measurement_parse_time_error():
    with pytest.raises(ValueError, match="Minute must be between 0 and 59."):
        parse_measurement("Köln;12:60;21.7")
        parse_measurement("12:60;Köln;21.7")

def test_parse_measurement_spaces():
    assert parse_measurement(" Köln ; 14:21 ; 21.7 ") == ("Köln", 861, 21.7)

def test_parse_measurement_ValueError():
    with pytest.raises(ValueError, match="Measurement must be a string."):
        parse_measurement(["Köln","12:60",21.7])
        parse_measurement(6)
        parse_measurement(21.6)
    with pytest.raises(ValueError, match="Expected exactly three fields."):
        parse_measurement("Köln;4")
        parse_measurement("Köln;4;1;6")
    with pytest.raises(ValueError, match="Temperature must be numeric."):
        parse_measurement("Köln;12:34;7")
        parse_measurement("7.5;12:50;Köln")
    with pytest.raises(ValueError, match="City must not be empty."):
        parse_measurement(" ;12:15;7.1")

def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]

def test_filter_by_temperature_ValueError():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    with pytest.raises(ValueError, match="lower must not be greater than upper."):
            filter_by_temperature(measurements, 20.0, 15.0)

def test_filter_by_temperature_Order():
    measurements = [
        ("Düsseldorf", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Düsseldorf", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 10.0, 25.0) == measurements

def test_filter_by_temperature_List():
    measurements = [
        ("Düsseldorf", 600, 10.0),
    ]

    assert isinstance(filter_by_temperature(measurements, 10.0, 25.0),list) == True


def test_filter_by_temperature_Double():
    measurements = [
        ("Düsseldorf", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Düsseldorf", 900, 25.0),
        ("Düsseldorf", 720, 18.5),
        ("Düsseldorf", 720, 18.5)
    ]

    assert filter_by_temperature(measurements, 10.0, 25.0) == measurements

def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0

def test_average_temperature_different_cities():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
        ("Düsseldorf", 720, 18.5)
    ]

    assert average_temperature(measurements, "Köln") == 15.0
    assert average_temperature(measurements, "Düsseldorf") == 18.5

def test_average_temperature_case_sensitive():
    measurements = [
        ("Köln", 600, 10.0),
        ("köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 10.0

def test_average_temperature_ValueError():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]
    with pytest.raises(ValueError, match="No measurements found for city."):
        average_temperature(measurements, "köln")

def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)
