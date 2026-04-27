import logging
from scapy.all import sniff
from scapy.layers.inet import IP


class NetworkDataSniffer:
    """
    This class provides functionality to sniff and capture network packets
    from a specified network interface. It allows capturing a limited number
    of packets and processes them to extract relevant metadata such as source IP,
    destination IP, and payload. The class also includes logging capabilities for
    monitoring and debugging.

    :ivar network_interface: The network interface from which packets will be
        captured (e.g., 'eth0', 'wlan0').
    :type network_interface: str
    :ivar packet_count: The number of packets to be captured during sniffing.
        Defaults to 10 if not specified.
    :type packet_count: int
    :ivar captured_data: A list to store metadata of captured packets. Each
        entry is a dictionary containing packet information such as source IP,
        destination IP, and payload.
    :type captured_data: list[dict[str, Any]]
    :ivar logger: A logger instance used for recording events, errors, and
        informational messages during the sniffing process.
    :type logger: logging.Logger
    """

    def __init__(self, network_interface, packet_count=10):
        """
        Initialize the sniffer with a specified network interface and packet count.

        :param network_interface: Network interface to monitor (e.g., 'eth0', 'wlan0').
        :param packet_count: Number of packets to capture (default: 10).
        """
        self.network_interface = network_interface
        self.packet_count = packet_count
        self.captured_data = []
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger():
        """
        Configures and returns a logger instance.

        :return: Configured logger instance.
        """
        logger = logging.getLogger('NetworkDataSniffer')
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def _process_packet(self, packet):
        """
        Processes a packet and extracts relevant metadata.

        :param packet: Captured network packet.
        """
        if IP in packet:
            packet_info = {
                "src_ip": packet[IP].src,
                "dst_ip": packet[IP].dst,
                "payload": str(packet[IP].payload)
            }
            self.captured_data.append(packet_info)
            self.logger.info(f"Packet Captured: {packet_info}")

    def sniff_network_data(self):
        """
        Starts sniffing packets on the specified network interface.

        :return: List of captured packet metadata as dictionaries.
        """
        self.logger.info(f"Starting network sniffing on interface '{self.network_interface}'...")
        try:
            sniff(iface=self.network_interface, count=self.packet_count, prn=self._process_packet, store=False)
            self.logger.info("Network sniffing completed successfully.")
        except PermissionError:
            self.logger.error("Permission denied. Please run the script with elevated privileges (e.g., 'sudo').")
        except Exception as e:
            self.logger.error(f"An error occurred during sniffing: {str(e)}")
        return self.captured_data


if __name__ == "__main__":
    # Example usage of the NetworkDataSniffer class
    logging.basicConfig(level=logging.INFO)

    # Replace 'eth0' with the appropriate network interface for your system
    network_interface = "eth0"
    packet_count = 5

    sniffer = NetworkDataSniffer(network_interface=network_interface, packet_count=packet_count)
    captured_data = sniffer.sniff_network_data()

    # Display captured data
    if captured_data:
        print("\nSniffed Packets:")
        for index, packet in enumerate(captured_data, start=1):
            print(f"{index}. Source: {packet['src_ip']}, Destination: {packet['dst_ip']}, Payload: {packet['payload']}")