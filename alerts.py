import winsound
import time

def trigger_alert():
    """
    Triggers a console message and a system beep on Windows.
    """
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ALERT: Motion detected!")
    # A more distinctive "Sci-Fi" double chime
    try:
        winsound.Beep(1200, 150) # High short tone
        time.sleep(0.05)
        winsound.Beep(1500, 300) # Higher longer tone
    except Exception as e:
        print(f"Could not play sound: {e}")

if __name__ == "__main__":
    trigger_alert()
