#!/usr/local/env python3
# -*-coding:utf-8-*-

# =======================================================================================================================
# 이 모듈은 프로그램 전역에서 사용되는 상수, 공통함수, 변수를 정의
# 작성자 : 이현신
# =======================================================================================================================

import os
import platform
import osLogger
from datetime import datetime

os.putenv("NLS_LANG", "KOREAN_KOREA.KO16KSC5601")

# DB 접속용 변수
MARIA_DB_USER = 'root'
MARIA_DB_PASS = 'P@s$w0rd'
MARIA_DB_IP = '127.0.0.1'
MARIA_DB_PORT = '3306'
MARIA_DB_NAME = 'EMS_DCS'

MAX_BUF = 1024


def readConfiguration(FileName: str = './Service.json'):
    ExceptLog = None
    try:
        global SERVICE_TYPE
        global SERVICE_PORT
        global MAX_THREAD
        global MAX_TIMEOUT
        global MAX_RETRY_COUNT
        global SMS_CALLBACK
        global SMS_ALARM_RECV
        global COMM_METHOD
        global OPERATION_MODE

        if os.path.exists(FileName):
            import json
            with open(FileName) as JsonFile:
                Conf = json.load(JsonFile)
                if 'SERVICE_TYPE' in Conf.keys():
                    SERVICE_TYPE = Conf['SERVICE_TYPE']
                if 'SERVICE_PORT' in Conf.keys():
                    SERVICE_PORT = Conf['SERVICE_PORT']
                if 'MAX_THREAD' in Conf.keys():
                    MAX_THREAD = Conf['MAX_THREAD']
                if 'MAX_TIMEOUT' in Conf.keys():
                    MAX_TIMEOUT = Conf['MAX_TIMEOUT']
                if 'MAX_RETRY_COUNT' in Conf.keys():
                    MAX_RETRY_COUNT = Conf['MAX_RETRY_COUNT']
                if 'SMS_CALLBACK' in Conf.keys():
                    SMS_CALLBACK = Conf['SMS_CALLBACK']
                if 'SMS_ALARM_RECV' in Conf.keys():
                    SMS_ALARM_RECV = Conf['SMS_ALARM_RECV']
                if 'COMM_METHOD' in Conf.keys():
                    COMM_METHOD = Conf['COMM_METHOD']
                if 'OPERATION_MODE' in Conf.keys():
                    OPERATION_MODE = Conf['OPERATION_MODE']
            JsonFile.close()
    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[Global:readConfiguration] ' + str(Ex))

    finally:
        pass


def printConfiguration():
    ExceptLog = None
    try:
        print('Serivce Type : ' + str(SERVICE_TYPE))
        print('Communication Type : ' + str(COMM_METHOD))
        print('Serivce Port : ' + str(SERVICE_PORT))
        print('Max Thread : ' + str(MAX_THREAD))
        print('Max Timeout : ' + str(MAX_TIMEOUT))
        print('Max Retry Count : ' + str(MAX_RETRY_COUNT))
        print('Database Type : ' + str(DB_TYPE))
        print('SMS Callback : ' + str(SMS_CALLBACK))
        print('SMS Recv List : ' + str(SMS_ALARM_RECV))

    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[Global:convertHexString] ' + str(Ex))
    finally:
        pass


def convertHexString(_pData: str = None):
    ExcepLog = None
    retVal = None
    try:
        strHex = str()
        for idx in range(0, len(_pData)):
            strHex += '\\x{:02X}'.format(ord(_pData[idx]))
        retVal = strHex
    except Exception as Ex:
        if ExcepLog is None:
            ExcepLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExcepLog.writeLog('[Global:convertHexString] ' + str(Ex))
        retVal = None
    finally:
        return retVal


def byte2Hex(_pData: bytearray = None):
    retVal = None
    ExcepLog = None
    try:
        strRet = str()
        for byte in _pData:
            strRet += '\\x{:02X}'.format(byte)
        retVal = strRet
    except Exception as Ex:
        if ExcepLog is None:
            ExcepLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExcepLog.writeLog('[Global:byte2Hex] ' + str(Ex))
        retVal = None
    finally:
        return retVal


def getCurrentTime():
    retVal = datetime.now().strftime("[%Y.%m.%d. %H:%M:%S]")
    return retVal


def getFileName(_pPathPrefix: str = None, _pFilePrefix: str = None, _pExtension: str = 'TXT'):
    ExcepLog = None
    retVal = None
    try:
        strYear = datetime.now().strftime("%Y")
        strMonth = datetime.now().strftime("%m")
        strDay = datetime.now().strftime("%d")
        strHour = datetime.now().strftime("%H")

        if _pPathPrefix is None:
            strPath = os.path.join(os.getcwd(), strYear, strMonth, strDay)
        else:
            strPath = os.path.join(os.getcwd(), _pPathPrefix, strYear, strMonth, strDay)

        if _pFilePrefix is None:
            strFile = strYear + strMonth + strDay + strHour + '.' + _pExtension
        else:
            strFile = _pFilePrefix + '_' + strYear + strMonth + strDay + strHour + '.' + _pExtension

        retVal = os.path.join(strPath, strFile)
    except Exception as Ex:
        if ExcepLog is None:
            ExcepLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExcepLog.writeLog('[Global:getFileName] ' + str(Ex))
        retVal = None
    finally:
        return retVal


def saveFile(_pFileName, _pData):
    ExcepLog = None
    retVal = None
    try:
        strDir = os.path.dirname(_pFileName)
        if not os.path.isdir(strDir):
            # 디렉토리가 존재하지 않는 경우이므로 디렉토리 생성
            os.makedirs(os.path.join(strDir))

        with open(_pFileName, "a") as file:
            file.write(_pData)
            file.write('\n')
            file.close()
        retVal = True
    except Exception as Ex:
        if ExcepLog is None:
            ExcepLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExcepLog.writeLog('[Global:saveFile] ' + str(Ex))
        retVal = False
    finally:
        return retVal


def saveRawFile(_pFilename: str = None, _pData: bytes = None):
    ExcepLog = None
    retVal = None
    try:
        strDir = os.path.dirname(_pFilename)
        if not os.path.isdir(strDir):
            os.makedirs(os.path.join(strDir))

        FD = open(_pFilename, "ab")
        for byte in _pData:
            FD.write(byte.to_bytes(1, byteorder='big'))
        FD.close()
        retVal = True
    except Exception as Ex:
        if ExcepLog is None:
            ExcepLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExcepLog.writeLog('[Global:saveRawFile] ' + str(Ex))
        retVal = False
    finally:
        return retVal


def isNum(Number: str = None):
    retVal = None
    try:
        float(Number)
        retVal = True
    except ValueError:
        retVal = False
    finally:
        return retVal


def getDateTime(pTime: str = None):
    ExceptLog = None
    RetVal = None
    try:
        if pTime is None:
            raise Exception('Invalid input data <YYYYMMDDHHmmSS> : None data')

        if len(pTime) == 14:
            RetVal = datetime(int(pTime[0:4]), int(pTime[4:6]), int(pTime[6:8]), int(pTime[8:10]), int(pTime[10:12]), int(pTime[12:14]))
        elif len(pTime) == 12:
            RetVal = datetime(int(pTime[0:4]), int(pTime[4:6]), int(pTime[6:8]), int(pTime[8:10]), int(pTime[10:12]), 0)
        elif len(pTime) == 10:
            RetVal = datetime(int(pTime[0:4]), int(pTime[4:6]), int(pTime[6:8]), int(pTime[8:10]), 0, 0)
        elif len(pTime) == 8:
            RetVal = datetime(int(pTime[0:4]), int(pTime[4:6]), int(pTime[6:8]), 0, 0, 0)

    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[Global:getDateTime] ' + str(Ex))
    finally:
        return RetVal


def getOS():
    ExceptLog = None
    RetVal = None
    try:
        System = str(platform.system()).strip()
        if System == 'Windows':
            RetVal = System
        elif System == 'Darwin':
            RetVal = 'MacOS'
        elif System == 'Linux':
            RetVal = System
        else:
            raise Exception('Unknown OS Type : ' + System)

    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[Global:getOS] ' + str(Ex))
    finally:
        return RetVal


if __name__ == '__main__':
    """
    ll = [34, 35, 36, 37, 38, 39]
    bb = bytes(ll)
    saveRawFile('./TEST.DAT', bb)
    
    osName = getOS()
    print(osName)
    """
    readConfiguration()
    printConfiguration()

