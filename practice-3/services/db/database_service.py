from cassandra.cluster import Cluster
import pika


def save_data_to_cassandra(data):
    cassandra_cluster = Cluster(['127.0.0.1'])
    cassandra_session = cassandra_cluster.connect()

    try:
        cassandra_session.execute(
            """
            CREATE KEYSPACE IF NOT EXISTS my_keyspace WITH REPLICATION = 
            {'class' : 'SimpleStrategy', 'replication_factor' : 1}
            """
        )
        cassandra_session.execute("USE my_keyspace")

        cassandra_session.execute(
            """
            CREATE TABLE IF NOT EXISTS person_data (
                url text PRIMARY KEY,
                person_name text,
                html_code text
            )
            """
        )

        cassandra_session.execute(
            """
            INSERT INTO person_data (url, person_name, html_code)
            VALUES (%s, %s, %s)
            """,
            (data['url'], data['person_name'], data['html_code'])
        )

        print(f"{data['url']} сохранено в базу данных")
    except Exception as e:
        print(f"Ошибка в подключении к Cassandra: {e}")
    finally:
        cassandra_cluster.shutdown()


def process_message(ch, method, properties, body):
    message_data = body.decode('utf-8').split('\n')
    parsed_data = {
        'url': message_data[0],
        'person_name': message_data[1],
        'html_code': message_data[2]
    }

    save_data_to_cassandra(parsed_data)


def consume_messages_from_queue(queue_name='parsed_data_queue'):
    try:
        rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
        rabbitmq_channel = rabbitmq_connection.channel()

        rabbitmq_channel.queue_declare(queue=queue_name)
        rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=process_message, auto_ack=True)

        print('Сервер в ожидании')
        rabbitmq_channel.start_consuming()
    except Exception as e:
        print(f"Ошибка подключения к очереди: {e}")
    finally:
        if rabbitmq_connection and rabbitmq_connection.is_open:
            rabbitmq_connection.close()


if __name__ == "__main__":
    consume_messages_from_queue()
