import socket
import struct
import re
from urllib.parse import parse_qsl



class Byond:
    def get_data(self, host, port, string):
        packet_id = b'\x83'
        try:
            sock = socket.create_connection((host, port))
        except socket.error:
            return
    
        packet = struct.pack('>xcH5x', packet_id, len(string) + 6) + bytes(string, encoding='windows-1251') + b'\x00'
        sock.send(packet)
    
        data = sock.recv(4096)
        sock.close()
        return data
       
    
    def decode_data(self, resp):
        if resp[0] == 0x00 and resp[1] == 0x83:
            return str(resp[5:-1], 'windows-1251')
            
    def parse_data(self, resp):
        return dict(parse_qsl(resp))
        
        
    def request_topic(self, host, port, string):
        encoded_responce = self.get_data(host, port, string)
        if(encoded_responce):
            decoded_responce = self.decode_data(encoded_responce)
            parsed_responce = self.parse_data(decoded_responce)
            return parsed_responce
