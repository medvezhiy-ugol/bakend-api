from worker import create_roulette

counter = 0

if __name__ == "__main__":
    while True:
        create_roulette(counter)
        counter += 1
