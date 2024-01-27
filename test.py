import time
import os

# Assuming self.handle, x, and y are defined somewhere before this code

tap_command = f'input tap {10} {20}'
tap_count = 15  # You can adjust this count based on your needs
delay_between_taps = 0.2  # You can adjust the delay in seconds

tap_commands = ' & '.join([f'{tap_command} sleep {delay_between_taps};' for _ in range(tap_count)])

print(tap_commands)

# os.system(f'adb -s {self.handle} shell "{tap_commands}"')