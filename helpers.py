import os
import sys
import requests
import subprocess

EMAILS = [
  {
    "uuid": "def456",
    "subject": "Order Confirmation - #98374",
    "sender_email": "orders@onlinestore.com",
    "sender_name": "Online Store",
    "date": "2025-04-10T18:45:00Z",
    "body": "Thanks for your purchase!\n\nOrder #98374\nEstimated delivery: April 15\n\nItems:\n- Wireless Mouse\n- USB-C Cable"
  },
  {
    "uuid": "4d5e6f",
    "subject": "Team Meeting Rescheduled",
    "sender_email": "manager@company.com",
    "sender_name": "Team Manager",
    "date": "2025-04-11T14:55:00Z",
    "body": "Hey team,\n\nTomorrow's meeting has been moved to Friday at 3pm. Let me know if there are conflicts.\n\n- Manager"
  },
  {
    "uuid": "abc123",
    "subject": "Your Weekly Newsletter",
    "sender_email": "news@weeklydigest.com",
    "sender_name": "Weekly Digest",
    "date": "2025-04-11T08:00:00Z",
    "body": "This week's highlights: How to improve your productivity, Top 10 tech stories, and more. Read now!"
  },
  {
    "uuid": "1a2b3c",
    "subject": "Invoice Due Tomorrow",
    "sender_email": "billing@acme-corp.com",
    "sender_name": "Acme Billing",
    "date": "2025-04-11T09:23:00Z",
    "body": "Hi,\n\nJust a reminder that your invoice #4579 is due tomorrow. Please ensure payment to avoid late fees.\n\nThanks,\nAcme Billing"
  },
  {
    "uuid": "ghi789",
    "subject": "Your Subscription is Active",
    "sender_email": "no-reply@streamflix.com",
    "sender_name": "StreamFlix",
    "date": "2025-04-09T07:30:00Z",
    "body": "Welcome! Your StreamFlix subscription is now active. Enjoy unlimited streaming anytime, anywhere."
  },
  {
    "uuid": "7g8h9i",
    "subject": "Lunch?",
    "sender_email": "friend@example.com",
    "sender_name": "Jessie",
    "date": "2025-04-10T12:05:00Z",
    "body": "Yo, want to grab lunch sometime this week? I'm free Thursday or Friday."
  }
]

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear, partly cloudy, and overcast",
    2: "Mainly clear, partly cloudy, and overcast",
    3: "Mainly clear, partly cloudy, and overcast",
    45: "Fog and depositing rime fog",
    48: "Fog and depositing rime fog",
    51: "Drizzle: Light, moderate, and dense intensity",
    53: "Drizzle: Light, moderate, and dense intensity",
    55: "Drizzle: Light, moderate, and dense intensity",
    56: "Freezing Drizzle: Light and dense intensity",
    57: "Freezing Drizzle: Light and dense intensity",
    61: "Rain: Slight, moderate and heavy intensity",
    63: "Rain: Slight, moderate and heavy intensity",
    65: "Rain: Slight, moderate and heavy intensity",
    66: "Freezing Rain: Light and heavy intensity",
    67: "Freezing Rain: Light and heavy intensity",
    71: "Snow fall: Slight, moderate, and heavy intensity",
    73: "Snow fall: Slight, moderate, and heavy intensity",
    75: "Snow fall: Slight, moderate, and heavy intensity",
    77: "Snow grains",
    80: "Rain showers: Slight, moderate, and violent",
    81: "Rain showers: Slight, moderate, and violent",
    82: "Rain showers: Slight, moderate, and violent",
    85: "Snow showers slight and heavy",
    86: "Snow showers slight and heavy",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight and heavy hail",
    99: "Thunderstorm with slight and heavy hail"
}

def get_json(url: str) -> dict:
    headers = {
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def notification(title: str, body: str, timeout=59):
    args = [
        sys.executable,
        os.path.join(os.path.dirname(__file__), "simple_ui.py"),
        "--title", title.split("\n")[0],
        "--content", body.replace("\n", "<br>"),
        "--timeout", str(timeout),
    ]
    result = subprocess.run(
        args,
        shell=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        close_fds=True,
    )
    if result.returncode != 0:
        raise Exception(f"failed to run simple_ui.py: {result.returncode}")