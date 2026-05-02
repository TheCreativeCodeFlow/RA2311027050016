import sys, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from notification_app_be.services.processor import compute_top_notifications

sample=[
    {"id":"a","type":"placement","timestamp":1700000000000},
    {"id":"b","type":"result","timestamp":1690000000000},
    {"id":"c","type":"event","timestamp":1700000500},
    {"id":"d","type":"placement","timestamp":"2023-11-14T12:00:00Z"},
    {"id":"e","type":"result","timestamp":1700001000000},
]
print(json.dumps(compute_top_notifications(sample, limit=3), indent=2))
