import socket
import json


def start_server(host='127.0.0.1', port=65432):
    server_info = {
        'host': host,
        'port': port
    }

    with open('server_info.json', 'w') as f:
        json.dump(server_info, f)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))  # привязываем сокет сервера к хосту и порту
        s.listen(2)  # начинаем прослушиваение входящих подключений
        print("Сервер запущен. Ожидание соединения...")
        conn, addr = s.accept()  # принимаем клиента
        print(conn, addr)
        with conn:
            print(f"Подключено к {addr}")
            while True:
                data = conn.recv(1024)  #получаем данные с клиента (что значит 1024?)

                if not data:  # ???
                    break

                message = data.decode()
                print(f"Получено сообщение: {message}")

                if message == "ping":
                    response = "pong"
                else:
                    response = "Ошибка: неизвестное сообщение"

                conn.sendall(response.encode())
                print(f"Отправлено сообщение: {response}")


if __name__ == "__main__":
    try:
        start_server()
    except OSError:
        print("Этот сервер уже работает")
