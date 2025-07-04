import re
import json
from datetime import datetime

log_pattern = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+)\s-\s(?P<level>\w+)\s-\sPayment failed for user (?P<user_id>\w+): (?P<message>.*)"
)

input_file = "logs/payment_error_timestamp.log"
output_file = "logs/structured_logs_timestamp.jsonl"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        match = log_pattern.match(line)
        if match:
            data = match.groupdict()
            # Convert timestamp to ISO format
            data["timestamp"] = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S,%f").isoformat()
            json.dump(data, outfile)
            outfile.write("\n")