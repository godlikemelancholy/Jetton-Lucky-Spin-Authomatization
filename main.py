from utils import load_sessions, spin
import threading
from art import text2art
import os
from queue import Queue
from time import sleep


def intro():
    print(text2art("Umbrella", "tarty1"))
    sleep(1.5)
    os.system("cls")
    print(text2art("Development", "tarty1"))
    sleep(1.5)
    os.system("cls")


def worker(queue, thread_id):
    while not queue.empty():
        session = queue.get()
        spin(session, thread_id)
        queue.task_done()


def main():
    intro()
    num_threads = int(input("Введите количество потоков: "))
    sessions = load_sessions()

    queue = Queue()
    for session in sessions:
        queue.put(session)

    threads = [
        threading.Thread(target=worker, args=(queue, thread_id + 1))
        for thread_id in range(num_threads)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Все потоки отработали.")
    input()


if __name__ == '__main__':
    main()
