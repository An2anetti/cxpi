from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame

class PacketMarkerState(Enum):
    STANDARD = 0
    NONSTANDARD = 1

class PacketMarkerAnalyzer(HighLevelAnalyzer):
    result_types = {
        'packet_marker': {
            'format': '{{data.packet_marker}}',
            'unit': 'Marker'
        }
    }

    def __init__(self):
        self.packet_duration = None
        self.standard_packet_duration = 11  # Длительность стандартного пакета в микросекундах
        self.nonstandard_packet_duration = 21  # Длительность нестандартного пакета в микросекундах
        self.packet_state = None

    def add_packet_marker(self, start_time, end_time, state):
        duration = end_time - start_time
        packet_marker = 0 if state == PacketMarkerState.STANDARD else 1
        self.frames.append(AnalyzerFrame(start_time, duration, 'packet_marker', {'packet_marker': packet_marker}))

    def decode(self):
        for frame in self.data.frames:
            if self.packet_duration is None:
                self.packet_duration = frame.duration
                self.packet_state = PacketMarkerState.STANDARD
            elif frame.duration == self.packet_duration:
                if self.packet_state != PacketMarkerState.STANDARD:
                    self.add_packet_marker(frame.start_time, frame.end_time, self.packet_state)
                    self.packet_state = PacketMarkerState.STANDARD
            elif frame.duration == self.nonstandard_packet_duration:
                if self.packet_state != PacketMarkerState.NONSTANDARD:
                    self.add_packet_marker(frame.start_time, frame.end_time, self.packet_state)
                    self.packet_state = PacketMarkerState.NONSTANDARD
            else:
                if self.packet_state is not None:
                    self.add_packet_marker(frame.start_time, frame.end_time, self.packet_state)
                    self.packet_state = None

# Здесь вы можете добавить свои собственные настройки, если необходимо
settings = []

# Создание экземпляра анализатора
packet_marker_analyzer = PacketMarkerAnalyzer()

# Запуск анализатора
packet_marker_analyzer.run(settings)
