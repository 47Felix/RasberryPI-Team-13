# Auswertung / Predictive Maintenance (InfluxDB Flux)

Alle Queries laufen in Grafana (Explore oder Alert-Rule), Bucket `icetruck`.

## 1. Sensor-Ausfall erkennen (keine Daten > 2 min)
```flux
from(bucket:"icetruck") |> range(start: -10m)
  |> filter(fn:(r)=> r._measurement=="icetruck" and r._field=="sensor_board_temp_c")
  |> last() |> map(fn:(r)=>({r with age_s: float(v: uint(v: now()) - uint(v: r._time)) / 1e9}))
```
Alert wenn `age_s > 120` bzw. Grafana "No data"-Handling = Alerting.

## 2. Temperaturgrenze verletzt (Tiefkuehlung <= -18 C laut LM-05-MBL-504-PM)
```flux
from(bucket:"icetruck") |> range(start: -5m)
  |> filter(fn:(r)=> r._field=="sensor_board_temp_c" or r._field=="actor_board_temp_c")
  |> mean()
```
Alert wenn Mittelwert > Grenzwert (Prototyp misst Raumtemperatur - Grenzwert im Demo-Betrieb anpassen).

## 3. Sensor-Drift / Wackelkontakt (Abweichung beider Boards)
```flux
from(bucket:"icetruck") |> range(start: -1h)
  |> filter(fn:(r)=> r._field=="sensor_board_temp_c" or r._field=="actor_board_temp_c")
  |> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")
  |> map(fn:(r)=>({r with diff: math.abs(x: r.sensor_board_temp_c - r.actor_board_temp_c)}))
  |> mean(column:"diff")
```
(`import "math"` voranstellen.) Dauerhaft hohe Differenz = einer der KY-028 defekt -> Wartung planen (passt zum offenen Wackelkontakt-Punkt aus Challenge I).

## 4. Kuehlaggregat unter Last (Predictive Maintenance)
Anteil der Zeit mit `fan_pwm > 200` pro Tag; steigt der Wert bei gleicher Umgebung, verliert die Kuehlung Leistung.
```flux
from(bucket:"icetruck") |> range(start: -7d)
  |> filter(fn:(r)=> r._field=="fan_pwm")
  |> map(fn:(r)=>({r with _value: if r._value > 200 then 1.0 else 0.0}))
  |> aggregateWindow(every: 1d, fn: mean)
```
