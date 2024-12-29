import asyncio
import aioconsole

global_var = 0

async def periodic_handler():
    """Handler that runs every 5 seconds"""
    global global_var
    while True:
        global_var += 1
        print("Periodic handler executed:", global_var)
        await asyncio.sleep(5)

async def keyboard_handler():
    """Handler for keyboard input"""
    while True:
        user_input = await aioconsole.ainput()
        print(f"{"".join(reversed(user_input))}")

async def main():
    # Create tasks for both handlers
    periodic_task = asyncio.create_task(periodic_handler())
    keyboard_task = asyncio.create_task(keyboard_handler())
    
    # Wait for the keyboard handler to complete (when user types 'quit')
    await keyboard_task
    
    # Cancel the periodic handler
    periodic_task.cancel()
    try:
        await periodic_task
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    asyncio.run(main())
