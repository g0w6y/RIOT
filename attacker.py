import json
import random
import time
from datetime import datetime
import logging
import argparse
from faker import Faker

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('attack_simulation.log'),
        logging.StreamHandler()
    ]
)

fake = Faker()

DEVICE_TYPES = [
    "thermostat", "security_camera", "smart_lock", 
    "motion_sensor", "smart_plug", "voice_assistant"
]

DEVICE_MODELS = {
    "thermostat": ["Nest-T300", "Ecobee-4", "Honeywell-T6"],
    "security_camera": ["Arlo-Pro3", "Ring-StickUp", "Wyze-Cam"],
    "smart_lock": ["August-4th", "Schlage-Connect", "Yale-Assure"],
    "motion_sensor": ["Philips-Hue", "Samsung-Smart", "Eufy-Security"],
    "smart_plug": ["TP-Link-Kasa", "Wemo-Mini", "Meross-Smart"],
    "voice_assistant": ["Echo-Dot", "Google-Nest", "HomePod-Mini"]
}

ATTACK_TYPES = {
    "bruteforce": {"pattern": "Multiple failed authentication attempts", "target": ["smart_lock", "voice_assistant"], "frequency": 0.3},
    "ddos": {"pattern": "High frequency requests from single IP", "target": ["all"], "frequency": 0.2},
    "injection": {"pattern": "Malicious command injection detected", "target": ["voice_assistant", "thermostat"], "frequency": 0.15},
    "recon": {"pattern": "Port scanning activity detected", "target": ["security_camera", "motion_sensor"], "frequency": 0.2},
    "malware": {"pattern": "Known malware signature detected", "target": ["all"], "frequency": 0.15}
}

NORMAL_ACTIVITIES = [
    "Device turned on", "Device turned off", "Routine check-in",
    "Firmware update check", "Scheduled temperature adjustment",
    "Motion detected", "Voice command processed", "Energy usage report",
    "Device status update", "Network connectivity check"
]

def generate_device_id(device_type):
    prefix = {"thermostat": "THRM", "security_camera": "CAM", "smart_lock": "LOCK",
              "motion_sensor": "MOTN", "smart_plug": "PLUG", "voice_assistant": "VOICE"}.get(device_type, "DEV")
    return f"{prefix}-{fake.unique.bothify(text='####-????').upper()}"

def generate_log_entry(is_attack=False):
    device_type = random.choice(DEVICE_TYPES)
    device_model = random.choice(DEVICE_MODELS[device_type])
    device_id = generate_device_id(device_type)
    ip_address = fake.ipv4()
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    if is_attack:
        attack_type = random.choices(list(ATTACK_TYPES.keys()), weights=[atk["frequency"] for atk in ATTACK_TYPES.values()], k=1)[0]
        attack_info = ATTACK_TYPES[attack_type]
        if "all" not in attack_info["target"]:
            device_type = random.choice(attack_info["target"])
            device_model = random.choice(DEVICE_MODELS[device_type])
            device_id = generate_device_id(device_type)
        return {
            "timestamp": timestamp,
            "device_id": device_id,
            "device_type": device_type,
            "device_model": device_model,
            "ip_address": ip_address,
            "status": "ANOMALY",
            "attack_type": attack_type,
            "message": attack_info["pattern"],
            "severity": random.choice(["high", "critical"]),
            "protocol": random.choice(["HTTP", "MQTT", "CoAP", "TCP"]),
            "port": random.randint(1024, 65535),
            "payload_size": random.randint(500, 5000)
        }
    else:
        return {
            "timestamp": timestamp,
            "device_id": device_id,
            "device_type": device_type,
            "device_model": device_model,
            "ip_address": ip_address,
            "status": "NORMAL",
            "message": random.choice(NORMAL_ACTIVITIES),
            "severity": "low",
            "protocol": random.choice(["HTTP", "MQTT", "CoAP", "TCP"]),
            "port": random.choice([80, 443, 1883, 5683]),
            "payload_size": random.randint(50, 500)
        }

def simulate_traffic(duration_min=5, attack_ratio=0.3, log_file="device_data.log"):
    end_time = time.time() + duration_min * 60
    total_logs = 0
    attacks_generated = 0
    
    logging.info(f"Starting traffic simulation for {duration_min} minutes (Attack ratio: {attack_ratio*100}%)")
    
    try:
        with open(log_file, "a") as f:
            while time.time() < end_time:
                time.sleep(random.uniform(0.1, 2))
                is_attack = random.random() < attack_ratio
                log_entry = generate_log_entry(is_attack)
                f.write(json.dumps(log_entry) + "\n")
                f.flush()
                
                if is_attack:
                    attacks_generated += 1
                    print(f"\033[91m[ATTACK] {log_entry}\033[0m")
                else:
                    print(f"\033[92m[NORMAL] {log_entry}\033[0m")
                
                total_logs += 1
                
    except KeyboardInterrupt:
        logging.info("Simulation interrupted by user")
    
    logging.info(f"Generated {total_logs} logs ({attacks_generated} attacks)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RIOT IDS/IPS Attack Simulator")
    parser.add_argument("--duration", type=int, default=5, help="Duration in minutes (default: 5)")
    parser.add_argument("--attack-ratio", type=float, default=0.3, help="Attack ratio (0.0-1.0, default: 0.3)")
    parser.add_argument("--log-file", default="device_data.log", help="Output log file (default: device_data.log)")
    
    args = parser.parse_args()
    
    print("\n=== RIOT Attack Simulator ===")
    print(f"Duration: {args.duration} minutes")
    print(f"Attack Ratio: {args.attack_ratio*100}%")
    print(f"Log File: {args.log_file}\n")
    
    simulate_traffic(
        duration_min=args.duration,
        attack_ratio=args.attack_ratio,
        log_file=args.log_file
    )
