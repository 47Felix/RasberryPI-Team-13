#!/usr/bin/env bash
# Challenge III: Azure-Ressourcen fuer den Ice Truck anlegen (Azure for Students).
#
# Ausfuehren in der Azure Cloud Shell (portal.azure.com -> ">_"-Symbol, Bash)
# oder lokal mit installierter Azure CLI nach `az login`.
#
#   bash setup.sh
#
# Legt an:
#   1. Ressourcengruppe
#   2. IoT Hub, Tarif F1 (kostenlos, 8.000 Nachrichten/Tag, max. 1 F1-Hub pro Subscription)
#   3. Device-Identitaet fuer den Pi (eigener SAS-Schluessel)
#   4. Storage Account + Container "telemetry" als revisionssicheres Archiv
#   5. Message Routing: jede Nachricht -> Blob-Archiv UND -> eingebauter Endpunkt
#      (sonst sieht der Live-Monitor/ADX nichts mehr, sobald eine eigene Route existiert)
#
# Namen von IoT Hub und Storage Account muessen weltweit eindeutig sein - bei
# Fehler "name not available" einfach SUFFIX aendern.
set -euo pipefail

SUFFIX="${SUFFIX:-team13x1}"
# Region in der EU (DSGVO). Azure for Students erlaubt je nach Schule nur
# bestimmte Regionen - bei "RequestDisallowedByAzure"/Policy-Fehler auf
# westeurope oder northeurope ausweichen.
LOCATION="${LOCATION:-germanywestcentral}"
RG="rg-icetruck-${SUFFIX}"
HUB="iothub-icetruck-${SUFFIX}"
DEVICE="icetruck-team13-1"
STORAGE="sticetruck${SUFFIX}"   # nur Kleinbuchstaben/Ziffern, max. 24 Zeichen
CONTAINER="telemetry"

az extension add --name azure-iot --upgrade --only-show-errors

echo "== 1. Ressourcengruppe"
az group create -n "$RG" -l "$LOCATION" -o none

echo "== 2. IoT Hub (F1)"
az iot hub create -n "$HUB" -g "$RG" -l "$LOCATION" --sku F1 --partition-count 2 -o none

echo "== 3. Device-Identitaet"
az iot hub device-identity create -n "$HUB" -d "$DEVICE" -o none

echo "== 4. Storage Account + Container"
az storage account create -n "$STORAGE" -g "$RG" -l "$LOCATION" \
  --sku Standard_LRS --kind StorageV2 --access-tier Cool \
  --min-tls-version TLS1_2 --allow-blob-public-access false -o none
STORAGE_CS=$(az storage account show-connection-string -n "$STORAGE" -g "$RG" -o tsv)
az storage container create -n "$CONTAINER" --connection-string "$STORAGE_CS" -o none

echo "== 5. Routing"
az iot hub message-endpoint create storage-container \
  --hub-name "$HUB" -g "$RG" --en archive \
  --container "$CONTAINER" --connection-string "$STORAGE_CS" \
  --encoding json --batch-frequency 300 --chunk-size 10 \
  --file-name-format '{iothub}/{partition}/{YYYY}/{MM}/{DD}/{HH}/{mm}' -o none
az iot hub message-route create --hub-name "$HUB" -g "$RG" \
  --rn to-archive --en archive --source devicemessages --condition true -o none
az iot hub message-route create --hub-name "$HUB" -g "$RG" \
  --rn to-builtin --en events --source devicemessages --condition true -o none

echo
echo "Fertig. Device-Connection-String fuer die .env auf dem Pi (GEHEIM, nicht committen):"
az iot hub device-identity connection-string show -n "$HUB" -d "$DEVICE" -o tsv
echo
echo "Live mitlesen:  az iot hub monitor-events -n $HUB -d $DEVICE --properties app"
