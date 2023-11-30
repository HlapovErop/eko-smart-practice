## [Схема сервиса](https://drive.google.com/file/d/1pdrCUZRihZ5TtESavYojzATk-VhXok2h/view?usp=sharing)

В качестве брокера под данный сценарий я считаю, что необходимо выбрать Apache Kafka.

Так как сценарий описывает высоконагруженную, критическую систему, в которой необходима обработка большого количества 
сообщений (обработка в реальном времени), гарантированная доставка сообщений.

1. Потенциальные преимущества брокер::
- Высокая пропускная способность: брокер очередей сообщений может обрабатывать большие объемы данных в режиме реального времени.
- Распределенная обработка: брокер позволяет распределять сообщения по разным хендлерам для параллельной обработки данных.
- Гарантированная доставка: брокер обеспечивает гарантированную доставку сообщений, что помогает избежать потери данных.

Потенциальные проблемы брокера очередей сообщений в данном сценарии:.
- Возможные задержки: при плохой настройке, возможны задержки в обработке данных.

2. Подробное описание блоков в системе:
- Источник данных фондового рынка (API): в данном блоке осуществляется получение потоковых данных о фондовом рынке в реальном времени.
- Обработчики данных (handlers): здесь данные из очереди обрабатываются и анализируются для выявления определенных трендов 
или сигналов на фондовом рынке.
- Брокер очередей сообщений (apache kafka): этот блок обрабатывает и распределяет потоковые сообщения по разным обработчикам 
для параллельной обработки данных.
- Хранилище данных (finance_db): этот блок предназначен для хранения исторических данных о фондовом рынке для последующего 
анализа и использования их в других системах.
- Пользовательский интерфейс (UI): здесь осуществляется визуализация данных и предоставление пользователю возможности 
мониторинга состояния фондового рынка.
 