import serial
import logging
import time
import asyncio

notebook = logging


class PySerialMonitor(asyncio.Protocol):

    def __init__(self, debug=False, os='Mac', baudrate=57600, timeout=1000):
        self.os = os
        self.debug = debug
        self.baudrate = baudrate

        self.timeout = timeout
        self.port = None
        self.usb_info = None

        self.serial = serial.Serial()
        self.is_connected = False

        self.data = {}

    def connect(self):

        import serial.tools.list_ports
        target_ports = []

        for p in list(serial.tools.list_ports.comports()):
            print(p.device, p.description)

            if ('Serial' or 'UNO' or 'Mega' or 'CP210') in p.description:
                target_ports.append(p)

        for p in target_ports:
            try:
                # if self.debug:
                print(p.device, p.description, p.usb_info())
                self.usb_info = p.usb_info()
                self.serial = serial.Serial(p.device, self.baudrate, timeout=1, exclusive=True)
                break
            except Exception as e:
                # notebook.error('serial connecting error', e, exc_info=True)
                pass

        if self.serial.is_open is False:
            self.is_connected = False
            self.port = None
            if self.debug:
                print("Monitor: Couldn't open a serial port.")
                print("Monitor: Try again!")
        else:
            self.is_connected = True
            self.port = self.serial.port
            if self.debug:
                print("Monitor is open: " + str(self.serial.is_open))
                print("Monitor port: " + self.serial.port)

    def available(self):
        packet = ''
        s = False
        r = False

        if self.is_connected is True:
            packet, r = self.read_line()
            if r is True and self.debug is True:
                print('Monitor byteArray: ', packet, len(packet))
        else:
            self.reconnect()
            time.sleep(1)

        if r is True and len(packet) > 0:
            self.data, s = self.read_protocol(packet)

        return s

    def read_protocol(self, data):
        d = {}
        dState = False
        d['TIMESTAMP'] = self.local_time()
        # print(d)

        try:
            data = data.strip('\r\n')
            list = data.split(' ')
            length = len(list)
            # print(list, length)

            if length == 1:
                d['CMD'] = list[0]
                dState = True
                if self.debug:
                    print('Monitor command received: ', d['CMD'])
            elif length == 2:
                d["CMD"] = list[0]
                d['CONTENT'] = list[1]
                dState = True
                if self.debug:
                    print('Monitor command received: ', d['CMD'], d['CONTENT'])
        except Exception as e:
            notebook.error('Decoding packet error', exc_info=True)

        # print(d)
        return d, dState

    def read_line(self):
        packet = ''
        state = False
        try:
            packet = self.serial.readline()
            packet = packet.decode()
            state = True
        except Exception as e:
            self.is_connected = False
            notebook.error('Serial reading error', exc_info=True)

        return packet, state

    def reconnect(self):
        notebook.info('Reconnecting...')
        debug = self.debug
        os = self.os
        baudrate = self.baudrate
        timeout = self.timeout
        self.__init__(debug=debug, os=os, baudrate=baudrate, timeout=timeout)
        self.connect()

    def local_time(self):
        return round(time.time(), 2)
