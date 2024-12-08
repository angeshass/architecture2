import socket
import time
import os
import fcntl

def start_client(host='127.0.0.1', port=65432):
    lock_file = "client_lock.txt"

    try:
        fp = open(lock_file, 'w')
        fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)  #
    except IOError:
        print("Процесс одного клиента уже запущен. Завершение работы.")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port)) #

            client_address = s.getsockname() #
            client_code = f"{client_address[0]}:{client_address[1]}"

            with open('client_code.txt', 'w') as f:
                f.write(client_code)

            print(f"Код клиента сохранен в файле: {client_code}")

            while True:
                try:
                    request = "ping"
                    print(f"НЕЕЕТ: {request}")
                    s.sendall(request.encode())

                    data = s.recv(1024)
                    response = data.decode()
                    print(f"Получен ответ: {response}")

                    if response == "pong":
                        print("Успешный обмен сообщениями")
                    else:
                        print("Ошибка: непредвиденный ответ")

                    time.sleep(1)

                except Exception as e:
                    print(f"Произошла ошибка: {e}")
                    break

    finally:
        # Always release the lock file, even if exceptions occur.
        os.unlink(lock_file)  #remove the lock file when finished
        print("Client finished and lock released.")


if __name__ == "__main__":
    start_client()
