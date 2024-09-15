import asyncio
import serial_asyncio

class Output(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('Porta serial conectada')

    def data_received(self, data):
        print(f'Recebido: {data.decode()}')

    def connection_lost(self, exc):
        print('Conexão perdida')

async def main():
    port = 'COM9'
    baudrate = 9600
    loop = asyncio.get_running_loop()

    transport, protocol = await serial_asyncio.create_serial_connection(
        loop, Output, port, baudrate=baudrate
    )

    
    
asyncio.run(main())
