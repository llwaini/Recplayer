import time
from PySerialMonitor import PySerialMonitor
from Processor import Processor
import logging as log
from threading import Thread

log.basicConfig(
    # filename="coderock.log",
    level=log.DEBUG,
    format='%(asctime)s - %(message)s')

config = {
    'debug': False,
    'log': True,
    'console': True
}

psm = PySerialMonitor(debug=False, baudrate=115200)
proc = Processor()


def setup():
    if config['log']:
        log.info('Application Launched!')


def loop():

    if psm.available():
        print('Monitor print command received: ', psm.data)
        command = psm.data
        if command['CMD'] == 'record' and proc.status == 'stopped':
            print('Record Voice, voice id: ', command['CONTENT'])
            # proc.record_with_timer(file_name=command['CONTENT'])
            async_recorder(receive_msg)

        if command['CMD'] == 'play' and proc.status == 'stopped':
            print('Play Voice, voice id: ', command['CONTENT'])
            proc.play_file(file_name=command['CONTENT'])

        if command['CMD'] == 'stop' and proc.status == 'recording':
            print('Try to stop recording!')
            proc.status = 'stopped'


def async_recorder(cb):
    def func(callback):
        print("Start recording async thread! ")
        proc.record_file(file_name=psm.data['CONTENT'])
        res = 'Finished'
        callback(res)
        print('Finish recording and close thread')

    t1 = Thread(target=func, args=(cb,))
    t1.start()


def receive_msg(res):
    print("Return result: ", res)


def main():
    setup()

    if config['log']:
        log.info('Enter Loop! ')

    while True:
        loop()


if __name__ == "__main__":
    main()
