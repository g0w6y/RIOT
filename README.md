![License: NC-OSL](https://img.shields.io/badge/License-NC--OSL-blue.svg)]
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-%2344cc11)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-%23000)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-%23f7931e)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Data-Pandas-%23150458)](https://pandas.pydata.org/)
[![Faker](https://img.shields.io/badge/Simulator-Faker-%23cc99ff)](https://faker.readthedocs.io/)
![HTML5](https://img.shields.io/badge/Frontend-HTML5-%23E34F26?style=for-the-badge&logo=html5&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# RIOT IDS/IPS – Intrusion Detection & Prevention System

RIOT IDS/IPS is a lightweight, real-time anomaly detection system built using machine learning to detect and prevent intrusions in IoT environments. Designed for both simulation and practical demonstration, it features a sleek login UI, real-time anomaly monitoring, device blocking capabilities, and a detailed analytics dashboard.

## Live Page

View Live Page : https://g0w6y.github.io/RIOT

## Features

- **Intrusion Detection** with supervised (Random Forest) and unsupervised (Isolation Forest) models
- **Anomaly Detection** based on simulated IoT traffic
- **Device Blocking/Unblocking** for suspicious IPs
- **Interactive Dashboard** to view system metrics and alerts
- **Glassmorphism Login UI** with particle background effects
- **Session-based Authentication** (client-side logic, ready for Flask integration)
- **Extensible Backend API** using Flask

## Tech Stack

| Layer         | Tools/Frameworks                        |
|--------------|------------------------------------------|
| Backend       | Python, Flask, Scikit-learn              |
| Frontend      | HTML5, CSS3, JavaScript, FontAwesome     |
| ML Models     | RandomForestClassifier, IsolationForest  |
| UI Enhancements | Particles.js, Inter font, custom CSS  |

## Project Structure

```
├── main.py           # Flask backend with ML models and APIs
├── attacker.py       # Script to simulate normal and malicious IoT traffic
├── login.html
├── dashboard.html
├── device_data.log   # Log file with device behavior data
├── README.md         # You’re here!
```

## How It Works

1. **Training**:
   - `main.py` trains ML models using provided log data.
   - Two approaches: Supervised (labeled data) and Unsupervised (anomaly detection).

2. **Simulation**:
   - `attacker.py` simulates IoT traffic including port scans, DDoS-like floods, etc.
   - Data is continuously appended to `device_data.log`.

3. **Detection & Dashboard**:
   - Flask app reads the log, detects anomalies, and displays them in the dashboard.
   - Suspicious devices can be blocked/unblocked via buttons.

4. **Login Page**:
   - UI styled with animated particles and glassmorphism.
   - Validates credentials and redirects to `/dashboard`.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/g0w6y/RIOT.git
cd RIOT
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` isn't available, use:

```bash
pip install flask scikit-learn
```

### 4. Run the Application

```bash
python main.py
```

- App will start on `http://localhost:5000`
- Visit `/` for the login page
- Credentials: `admin / password123`

### 5. Run the Attacker Simulation

In a new terminal:

```bash
python attacker.py
```

## Screenshots

| Login Page | Dashboard |
|------------|-----------|
| ![login](https://i.ibb.co/v6rr17qB/IMG-20250405-WA0011.jpg) |![dashboard](https://i.ibb.co/270snGs2/IMG-20250405-WA0010.jpg)
 

## Future Improvements

- Add database-backed authentication & registration
- Real-time WebSocket updates for incoming attacks
- Extend detection rules using signature-based methods
- Integrate with real IoT edge devices (Raspberry Pi, ESP8266)

## 📜 License
   This project is licensed under the **Non-Commercial Open Source License (NC-OSL)**.  
   - ✅ **Allowed**: Personal use, modification, distribution (with attribution)  
   - ❌ **Prohibited**: Commercial use without explicit permission  
   - **Attribution Required**: Derivative works must credit the original author and link to this repository.  
   See full terms in [LICENSE.md](LICENSE.md).

---
   > **Disclaimer**: This software is provided "as-is" for non-commercial use only.  
   > For commercial licensing inquiries, contact the author.
   
---

Made with ❤️ By g0w6y 
