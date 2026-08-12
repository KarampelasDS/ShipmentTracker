"""Seed the database with a realistic set of shipments and status histories.

Idempotent: shipments are keyed by tracking number, so re-running skips any
shipment that already exists instead of creating duplicates.

Run from the project root of the API:
    uv run python seed.py
"""

from datetime import datetime, timedelta

import models
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

# A fixed reference point so the relative timestamps stay stable per run.
NOW = datetime.utcnow()


def days_ago(days: float) -> datetime:
    return NOW - timedelta(days=days)


# Each shipment carries an ordered list of status events. The shipment's own
# status/created_at/updated_at are derived from those events below, so the
# timeline in the UI always matches the current status.
SHIPMENTS = [
    {
        "tracking_number": "3SABCD1928374",
        "recipient_name": "Sanne de Vries",
        "destination_country": "Netherlands",
        "carrier": "PostNL",
        "events": [
            ("created", "Shipping label created", days_ago(4.0)),
            ("picked_up", "Parcel collected from sender", days_ago(3.8)),
            ("in_transit", "Arrived at sorting centre Amsterdam", days_ago(3.2)),
            ("out_for_delivery", "Out for delivery", days_ago(2.9)),
            ("delivered", "Delivered to recipient", days_ago(2.8)),
        ],
    },
    {
        "tracking_number": "1Z999AA10123456784",
        "recipient_name": "Lukas Müller",
        "destination_country": "Germany",
        "carrier": "UPS",
        "events": [
            ("created", "Shipping label created", days_ago(2.5)),
            ("picked_up", "Picked up by carrier", days_ago(2.3)),
            ("in_transit", "Departed facility Duisburg", days_ago(1.6)),
            ("in_transit", "Arrived at facility Köln", days_ago(1.1)),
        ],
    },
    {
        "tracking_number": "05123456789012",
        "recipient_name": "Camille Laurent",
        "destination_country": "France",
        "carrier": "DPD",
        "events": [
            ("created", "Shipping label created", days_ago(1.4)),
            ("picked_up", "Parcel collected from sender", days_ago(1.2)),
            ("in_transit", "In transit to destination depot", days_ago(0.6)),
            ("out_for_delivery", "Out for delivery", days_ago(0.2)),
        ],
    },
    {
        "tracking_number": "JVGL0058812345678",
        "recipient_name": "Giulia Romano",
        "destination_country": "Italy",
        "carrier": "DHL",
        "events": [
            ("created", "Shipping label created", days_ago(6.0)),
            ("picked_up", "Picked up by carrier", days_ago(5.8)),
            ("in_transit", "Export scan, departed Netherlands", days_ago(5.3)),
            ("exception", "Held at customs, awaiting clearance", days_ago(4.5)),
            ("in_transit", "Customs cleared, resumed transit", days_ago(3.9)),
            ("delivered", "Delivered, signed for by recipient", days_ago(3.4)),
        ],
    },
    {
        "tracking_number": "323212345678901",
        "recipient_name": "Emma Peeters",
        "destination_country": "Belgium",
        "carrier": "Bpost",
        "events": [
            ("created", "Shipping label created", days_ago(0.3)),
        ],
    },
    {
        "tracking_number": "6A28471930485",
        "recipient_name": "Louis Moreau",
        "destination_country": "France",
        "carrier": "Colissimo",
        "events": [
            ("created", "Shipping label created", days_ago(3.1)),
            ("picked_up", "Parcel collected from sender", days_ago(2.9)),
            ("in_transit", "Sorted at hub Paris-Nord", days_ago(2.2)),
            ("out_for_delivery", "Out for delivery", days_ago(1.9)),
            ("exception", "Recipient not home, redelivery scheduled", days_ago(1.85)),
        ],
    },
    {
        "tracking_number": "ZXA8830471",
        "recipient_name": "Mateo García",
        "destination_country": "Spain",
        "carrier": "GLS",
        "events": [
            ("created", "Shipping label created", days_ago(5.2)),
            ("picked_up", "Picked up by carrier", days_ago(5.0)),
            ("in_transit", "Departed hub Madrid", days_ago(4.4)),
            ("out_for_delivery", "Out for delivery", days_ago(4.0)),
            ("delivered", "Delivered to neighbour, no. 12", days_ago(3.95)),
        ],
    },
    {
        "tracking_number": "3SXKLM7654321",
        "recipient_name": "Daan Jansen",
        "destination_country": "Netherlands",
        "carrier": "PostNL",
        "events": [
            ("created", "Shipping label created", days_ago(0.9)),
            ("picked_up", "Parcel collected from sender", days_ago(0.7)),
            ("in_transit", "Arrived at sorting centre Utrecht", days_ago(0.3)),
        ],
    },
    {
        "tracking_number": "JJD014600009988776",
        "recipient_name": "Hannah Schmidt",
        "destination_country": "Austria",
        "carrier": "DHL",
        "events": [
            ("created", "Shipping label created", days_ago(2.0)),
            ("picked_up", "Picked up by carrier", days_ago(1.8)),
            ("in_transit", "Departed facility Nürnberg", days_ago(1.2)),
            ("out_for_delivery", "Out for delivery", days_ago(0.4)),
        ],
    },
    {
        "tracking_number": "05987654321098",
        "recipient_name": "Zofia Kowalski",
        "destination_country": "Poland",
        "carrier": "DPD",
        "events": [
            ("created", "Shipping label created", days_ago(7.5)),
            ("picked_up", "Parcel collected from sender", days_ago(7.3)),
            ("in_transit", "In transit to destination depot", days_ago(6.6)),
            ("out_for_delivery", "Out for delivery", days_ago(6.1)),
            ("delivered", "Delivered to recipient", days_ago(6.0)),
        ],
    },
]


def seed() -> None:
    db = SessionLocal()
    created = 0
    skipped = 0
    try:
        for entry in SHIPMENTS:
            exists = (
                db.query(models.Shipment)
                .filter(models.Shipment.tracking_number == entry["tracking_number"])
                .first()
            )
            if exists:
                skipped += 1
                continue

            events = entry["events"]
            first_at = events[0][2]
            last_status, _, last_at = events[-1]

            shipment = models.Shipment(
                tracking_number=entry["tracking_number"],
                recipient_name=entry["recipient_name"],
                destination_country=entry["destination_country"],
                carrier=entry["carrier"],
                status=last_status,
                created_at=first_at,
                updated_at=last_at,
            )
            for status, note, occurred_at in events:
                shipment.events.append(
                    models.StatusEvent(status=status, note=note, occurred_at=occurred_at)
                )

            db.add(shipment)
            created += 1

        db.commit()
        print(f"Seed complete: {created} shipment(s) created, {skipped} already present.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
