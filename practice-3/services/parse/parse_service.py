import requests
from bs4 import BeautifulSoup
import pika


def scrape_website_and_send_to_queue(target_url):
    try:
        response = requests.get(target_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        person_name = soup.find('h1').get_text().strip()
        html_code = str(soup)

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        queue_name = 'parsed_data_queue'
        channel.queue_declare(queue=queue_name)

        html_code_bytes = html_code.encode('utf-8')
        message_body = f"{target_url}\n{person_name}\n{html_code_bytes}"
        channel.basic_publish(exchange='', routing_key=queue_name, body=message_body)

        print(f"{target_url} результат отправлен в очередь.")

        connection.close()

    except requests.RequestException as req_exc:
        print(f"Ошибка в отправке запроса: {req_exc}")
    except Exception as exc:
        print(f"Неожиданная ошибка: {exc}")


if __name__ == "__main__":
    url_to_scrape = "https://career.habr.com/alishermadaminov9717"
    scrape_website_and_send_to_queue(url_to_scrape)