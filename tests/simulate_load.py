import socket
import threading
import time
import random

# Server details
SERVER_IP = "10.129.131.148"
SERVER_PORT = 8010
COMMANDS_FILE = "commands.txt"
RESULTS_FILE = "results.csv"

# Thread function to simulate a single user
def simulate_user(thread_id):
    try:
        with open(COMMANDS_FILE, "r") as file:
            commands = file.readlines()

        # Connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_IP, SERVER_PORT))
            response_times = []

            for command in commands:
                command = command.strip() + "\r\n"
                start_time = time.time()
                client_socket.sendall(command.encode())
                response = client_socket.recv(1024).decode()
                end_time = time.time()

                response_time = (end_time - start_time) * 1_000_000 # convert to micro-sec
                print('response_time: ', response_time)
                response_times.append(response_time)

                # Log the server's response
                print(f"Thread {thread_id}: Sent: {command.strip()}, Received: {response.strip()}, Time: {response_time:.2f}s")
                wait_time = random.uniform(0.5, 1)  # Generates a random float between 1 and 5
                time.sleep(wait_time)

            command = 'exit\r\n'
            client_socket.send(command.encode())

            # Save results to a CSV
            with open(RESULTS_FILE, "a") as results:
                for command, response_time in zip(commands, response_times):
                    results.write(f"{thread_id},{command.strip()},{response_time:.4f}\n")

    except Exception as e:
        print(f"Thread {thread_id}: Error occurred - {e}")

# Main function to simulate concurrent users
def main():
    num_users = 10  # Number of concurrent users
    threads = []

    # Open the results file and write the header
    with open(RESULTS_FILE, "w") as results:
        results.write("ThreadID,Command,ResponseTime\n")

    # Start threads
    for i in range(num_users):
        thread = threading.Thread(target=simulate_user, args=(i,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print(f"Simulation complete. Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    main()
