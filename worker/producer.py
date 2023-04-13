from worker import create_roulette
import asyncio

counter = 0

if __name__ == "__main__":
    while True:
        asyncio.get_event_loop().run_until_complete(create_roulette(counter))
        counter += 1
