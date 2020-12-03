#!/usr/local/env python3
# -*-coding:utf-8-*-

# =======================================================================================================================
# 이 모듈은 인천보건환경연구원의 TCP/IP 기반 자료수집서버의 테스트
# 작성자 : 이현신
# 주의 사항 : 측정소 코드별로 데이터 형식 맞춰서 전송해야함
# =======================================================================================================================

import socket
import Global
import osLogger
from _datetime import datetime
import pandas as pd


def getChecksum(Data: str = None):
    ExceptLog = None
    RetVal = None
    try:
        if Data is None:
            raise Exception('Invalid Input Data : None')

        iLen = len(str(Data))
        CharSum = 0
        for i in range(0, iLen):
            CharSum = CharSum + ord(Data[i])
        CheckSum1 = ((CharSum & 0xF0) >> 4) + 0x30
        CheckSum2 = ((CharSum & 0x0F) >> 0) + 0x30

        RetVal = chr(CheckSum1) + chr(CheckSum2)
    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[sendData:getChecksum] ' + str(Ex))
    finally:
        return RetVal


if __name__ == '__main__':
    now = datetime.now().strftime("[%Y.%m.%d. %H:%M:%S]")
    ls = [1, now, 'nana', 'HYUNJAEJEON' ]
    Pkt1 = ls

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 7885))

    # client.send(Pkt1.encode())
    print('SEND : ', Pkt1)

    client.close()
