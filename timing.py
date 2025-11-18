import threading
import time

stop_flag = False
total_seconds = 60


def countdown(seconds):
    global stop_flag
    global total_seconds
    start = time.time()
    while not stop_flag:
        elapsed = int(time.time() - start)
        remaining = seconds - elapsed
        if remaining < 0:
            print("\nTempo scaduto!")
            stop_flag = True
            break
        print(f"\rTempo rimanente: {remaining}s    ", end="")
        time.sleep(1)
        total_seconds = remaining


def get_input():
    global stop_flag
    input()
    stop_flag = True


def start_match_with_time(remaining_seconds: int) -> int:
    global stop_flag
    global total_seconds
    total_seconds = remaining_seconds
    print("Premi un tasto per fermare il tempo e dare la risposta")
    timer_thread = threading.Thread(target=countdown, args=(total_seconds,))
    input_thread = threading.Thread(target=get_input)

    timer_thread.start()
    input_thread.start()

    input_thread.join()
    stop_flag = True
    timer_thread.join()

    print(f"\nTimer fermato: {total_seconds}")
    answer = input("Scrivi la tua risposta: ")
    return total_seconds, answer
