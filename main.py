import time
import threading
import subprocess
import RPi.GPIO as GPIO
import board
import neopixel

# ---- CONFIGURATION ---- #

# GPIO Pins
BUTTON_PIN = 17         # Big red button
MOTOR_IN1 = 23          # L298N IN1
MOTOR_IN2 = 24          # L298N IN2
NUM_PIXELS = 30         # Adjust based on your LED strip
PIXEL_PIN = board.D18   # GPIO18 (PWM pin for NeoPixel)

# Files
SOUND_FILE = "scary_sound.mp3"

# Durations
LIGHTNING_DURATION = 5  # seconds
MOTOR_DURATION = 3      # seconds

# ---- SETUP ---- #

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Use pull-up resistor
GPIO.setup(MOTOR_IN1, GPIO.OUT)
GPIO.setup(MOTOR_IN2, GPIO.OUT)

# Initialize NeoPixel
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=1.0, auto_write=False)

# ---- EFFECT FUNCTIONS ---- #

def play_sound():
    """Play scary sound via mpg123 command-line player."""
    subprocess.run(["mpg123", "-q", SOUND_FILE])

def lightning_effect(duration):
    """Flash the LED strip randomly for lightning effect."""
    end_time = time.time() + duration
    while time.time() < end_time:
        pixels.fill((255, 255, 255))
        pixels.brightness = 0.8 + 0.2 * (time.time() % 1)  # Slight brightness flicker
        pixels.show()
        time.sleep(0.05)
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(0.05)

def activate_motor(duration):
    """Spin the motor forward for specified time."""
    GPIO.output(MOTOR_IN1, GPIO.HIGH)
    GPIO.output(MOTOR_IN2, GPIO.LOW)
    time.sleep(duration)
    GPIO.output(MOTOR_IN1, GPIO.LOW)
    GPIO.output(MOTOR_IN2, GPIO.LOW)

def trigger_sequence():
    """Trigger all actions in parallel: light, sound, motor."""
    threading.Thread(target=lightning_effect, args=(LIGHTNING_DURATION,), daemon=True).start()
    threading.Thread(target=play_sound, daemon=True).start()
    activate_motor(MOTOR_DURATION)

# ---- MAIN LOOP ---- #

print("🎃 Ready. Waiting for button press...")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button pressed
            print("👻 Triggered!")
            trigger_sequence()
            # Debounce / wait until button released
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.1)
            time.sleep(0.5)  # Cooldown before allowing next trigger
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
    pixels.fill((0, 0, 0))
    pixels.show()