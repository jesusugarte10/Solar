import RPi.GPIO as GPIO
import time

# Define GPIO pins for software I2C (SDA and SCL)
SDA_PIN = 17  # GPIO 0 (BCM pin 17)
SCL_PIN = 18  # GPIO 1 (BCM pin 18)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SDA_PIN, GPIO.OUT)
GPIO.setup(SCL_PIN, GPIO.OUT)

# I2C start condition
def i2c_start():
    GPIO.output(SDA_PIN, GPIO.HIGH)
    GPIO.output(SCL_PIN, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(SDA_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(SCL_PIN, GPIO.LOW)
    time.sleep(0.1)

# I2C stop condition
def i2c_stop():
    GPIO.output(SDA_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(SCL_PIN, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(SDA_PIN, GPIO.HIGH)
    time.sleep(0.1)

# I2C write byte
def i2c_write_byte(byte):
    for i in range(8):
        GPIO.output(SDA_PIN, (byte & (1 << (7 - i))) != 0)
        time.sleep(0.1)
        GPIO.output(SCL_PIN, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(SCL_PIN, GPIO.LOW)
        time.sleep(0.1)

# I2C read byte
def i2c_read_byte():
    byte = 0
    GPIO.setup(SDA_PIN, GPIO.IN)
    for i in range(8):
        time.sleep(0.1)
        GPIO.output(SCL_PIN, GPIO.HIGH)
        time.sleep(0.1)
        bit = GPIO.input(SDA_PIN)
        byte |= (bit << (7 - i))
        GPIO.output(SCL_PIN, GPIO.LOW)
        time.sleep(0.1)
    GPIO.setup(SDA_PIN, GPIO.OUT)
    return byte

# Function to read UV light value from LTR-390 (example)
def read_uv_light_value():
    # Example: Send I2C start condition
    i2c_start()

    # Example: Write I2C address + write bit
    i2c_write_byte(0xA0)  # Replace with your I2C device address + write bit

    # Example: Write register address to read from
    i2c_write_byte(0x00)  # Replace with your register address

    # Example: Restart I2C communication
    i2c_start()

    # Example: Write I2C address + read bit
    i2c_write_byte(0xA1)  # Replace with your I2C device address + read bit

    # Example: Read 1 byte of data
    data = i2c_read_byte()

    # Example: End I2C communication
    i2c_stop()

    return data

# Example usage
try:
    while True:
        # Read UV light value from LTR-390 (or other I2C device)
        uv_light_value = read_uv_light_value()
        print("UV Light Value:", uv_light_value)

        # Wait before the next reading
        time.sleep(1)  # Adjust as needed

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on Ctrl+C exit
