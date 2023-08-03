from saleae.data import GraphTimeDelta, GraphTime, GraphValue

def analyze(cxpi):
    # Получение данных из протокола CXPI
    messages = cxpi['messages']

    # Инициализация переменных для обработки пакетов
    packet = []
    packet_start = False

    # Итерация по сообщениям
    for message in messages:
        # Получение полей сообщения
        channel = message['channel']
        id = message['id']
        data = message['data']

        # Обработка пакета
        if packet_start:
            # Добавление данных в пакет
            packet.extend(data)

            # Проверка условия окончания пакета
            if data[0] == 1:
                # Обработка завершенного пакета
                process_packet(packet)

                # Сброс переменных пакета
                packet = []
                packet_start = False
        else:
            # Проверка условия начала пакета
            if data[0] == 0:
                packet_start = True
                packet.extend(data)

def process_packet(packet):
    # Обработка завершенного пакета
    # Здесь можно выполнить необходимые действия с данными пакета
    # Например, распарсить поля пакета, проанализировать значения и т.д.
    print(f"Processed packet: {packet}")

# Регистрация анализатора
cxpi_analyzer = {
    'name': 'CXPI Analyzer',
    'category': 'Other',
    'software_version': '0.1',
    'compatible_capture_modes': ['CXPI'],
    'parse_live': False,
    'parse_capture': True,
    'analyze': analyze
}