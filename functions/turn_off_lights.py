import asyncio
from kasa import SmartPlug

# Define the IP addresses for your smart plugs
LED_PLUG_IP = "enter_your_led_plug_ip_here" 
DESK_LIGHTS_IP = "enter_your_led_plug_ip_here"

async def turn_off_device(ip: str):
    """Turn off a smart plug device using its IP address."""
    plug = SmartPlug(ip)
    await plug.update()  # Get the current state
    if plug.is_on:
        print(f"Turning off device at {ip}...")
        await plug.turn_off()
        print(f"Device at {ip} is now OFF.")
    else:
        print(f"Device at {ip} is already OFF.")

async def turn_off_lights():
    """Turn on all smart plug devices (lights)."""
    await asyncio.gather(
        turn_off_device(LED_PLUG_IP),
        turn_off_device(DESK_LIGHTS_IP)
    )

# Run the function to turn on the lights
if __name__ == "__main__":
    asyncio.run(turn_off_lights())
