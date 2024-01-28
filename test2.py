import random

tap_command = f'input tap {1} {2}'
tap_count = random.randint(3, 6)  # You can adjust this count based on your needs
delay_between_taps = 0.2  # You can adjust the delay in seconds

tap_commands = f' & sleep {delay_between_taps} & '.join([f'{tap_command}' for _ in range(tap_count)])

print(tap_commands)