import time
import random


def generate_retrival_reference_num():
    timestamp = int(time.time())
    random_component = random.randint(10000, 99999)


    return f"33{timestamp % 1000000:06d}{random_component:05d}"


def generate_system_trace_audit_number():
    timestamp = int(time.time())
    random_component = random.randint(1, 33)
    timestamp_part = timestamp % 1000
    # Combine timestamp_part and random_component, ensuring 6 digits total
    result = (timestamp_part * 1000 + random_component) % 1000000

    return f"{result:06d}"
