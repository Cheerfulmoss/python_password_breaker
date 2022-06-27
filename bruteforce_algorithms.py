from itertools import product
from string import printable
from time import time
from threading import Thread


class PasswordBreaker:

    def __init__(self):
        self.guessed_password = ""
        self.attempts = 0
        self.stop_threads = False
        self.characters = printable

    def guess_password(self, password, lengths_list):
        while self.stop_threads is False:
            if type(lengths_list) == list:
                running = True
                while running:
                    for length in lengths_list:
                        for guess in product(self.characters, repeat=length):
                            if self.stop_threads:
                                break
                            self.attempts += 1
                            guess = "".join(guess)
                            if guess == password:
                                self.guessed_password = guess
                                self.stop_threads = True
                                print(f"Thread finished successfully, {length}")
                                running = False
                                break
                        if self.stop_threads:
                            break
                    running = False
            else:
                for guess in product(self.characters, repeat=lengths_list):
                    if self.stop_threads:
                        break
                    self.attempts += 1
                    guess = "".join(guess)
                    if guess == password:
                        self.guessed_password = guess
                        self.stop_threads = True
                        print(f"Thread finished successfully, {lengths_list}")
                        break

    def start_threads(self, password, lengths_list, max_threads):
        for letter in password:
            if letter not in self.characters:
                raise ValueError(f"Invalid characters")
        for length in lengths_list:
            if length < 1:
                raise ValueError(f"Length less than zero")
        threads = list()

        if len(lengths_list) > max_threads:
            split_lengths_list = [lengths_list[i::max_threads] for i in range(max_threads)]
            for index in range(max_threads):
                t = Thread(target=self.guess_password, args=(password, split_lengths_list[index]))
                threads.append(t)
        else:
            for length in lengths_list:
                t = Thread(target=self.guess_password, args=(password, length))
                threads.append(t)
        start_time = time()
        for thread in threads:
            thread.start()
        for finished_thread in threads:
            finished_thread.join()
        total_time = time() - start_time
        return self.guessed_password, self.attempts, total_time
