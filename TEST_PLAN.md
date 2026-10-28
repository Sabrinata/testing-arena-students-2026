# Test Plan

## `parse_time(time_text)`

[x] Führende Nullen
```python
parse_time("9:5") == 545
parse_time("09:5") == 545
parse_time("9:05") == 545
parse_time("09:05") == 545
```

[x] Normalen Beispiele:
```python
parse_time("14:21") == 861
```

[x] Grenzwerte:
```python
parse_time("00:00") == 0
parse_time("23:59") == 1439
```

Value Error bei
[x] Eingabe besteht nicht aus 2 Bestandteilen, getrennt durch :
[x] Eingabe ist keine Natürliche Zahl
[x] Stunden sind nicht zwischen 0 und einschließlich 23
[x] Minuten sind nicht zwischen 0 und einschließlich 59


## `parse_measurement(line)`

Reguläre Eingabe:
[x] Uhrzeit wird nach den Regeln von parse_time(HH:MM) verarbeitet
[x] Temperatur ist ein float

[x] Führende und nachfolgende Leerzeichen der 3 Teile in der Eingabe werden entfernt

Value Error bei
[x] Eingabe ist kein String
[x] Eingabe hat nicht genau 3 Teile durch ; getrennt
[x] Eingabe ist in der richtigen Reihenfolfe "Stadt;Uhrzeit;Temperatur"
[x] Temperatur ist kein float
[x] Städtename ist nicht leer sein anch entfernen der Leerzeichen

[x] keine Plausibilitätsprüfung

## `filter_by_temperature(measurements, lower, upper)`

[] Die Grenzen sind: `lower <= temperature <= upper`.




