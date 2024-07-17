import requests
import threading

class Checker:

    def __init__(self) -> None:
        self.username_file = "list.txt" # the usenrames list (input)
        self.untaken_file = "untaken.txt" # the outputfile -> will show which usernames are avaliable / unclaimed. (output)
        self.link = "https://github.com/"
        self.lock = threading.Lock()

    def add_to_untaken(self, username: str) -> None:
        print(f"{username} is untaken maybe I should use that haha")
        with self.lock:
            with open(self.untaken_file, "a") as f:
                f.write(f'{username}\n')

    def check_if_taken(self, username: str) -> None:
        print(f"Checking username: {username}")
        r = requests.get(f'{self.link}{username}')
        if r.status_code == 404:  # if page doesn't exist
            self.add_to_untaken(username)
        else:
            print(f"{username} is taken :(")


    def check_usernames(self) -> None:
        with open(self.username_file, "r") as f:
            usernames = f.read().splitlines()

        print(f"{len(usernames)} usernames to check")

        for username in usernames:
            self.check_if_taken(username)

        

        threads = []
        for username in usernames:
             thread = threading.Thread(target=self.check_if_taken, args=(username))
             threads.append(thread)
             thread.start()
    
        for thread in threads:
             thread.join()

if __name__ == "__main__":

    checker = Checker()
    checker.check_usernames()


