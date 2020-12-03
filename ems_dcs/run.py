#!/usr/local/env python3
# -*-coding:utf-8-*-

# =======================================================================================================================
# 이 모듈은 인천보건환경연구원의 TCP/IP기반 환경측정망 자료 수집 시스템의 메인
# 작성자 : 이현신
# 주의 사항 : 없음
# =======================================================================================================================

import socket
import threading
import gc
import atexit
import os
import sys
import signal
import pandas

import Global
import osDB
import osLogger

from datetime import datetime


class cDataCapture(threading.Thread):
    _mChannel = None
    _mDetail = None
    _mStationInfo = None
    _mMetricInfo = None
    _mProgramInfo = None

    def __init__(self, Channel, Detail):
        ExceptLog = None
        try:
            self._mChannel = Channel
            self._mDetail = Detail
            threading.Thread.__init__(self)
        except Exception as Ex:
            if ExceptLog is None:
                ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
            ExceptLog.writeLog('[run:__init__] ' + str(Ex))
        finally:
            pass

    def run(self):
        ExceptLog = None
        ConnectLog = None
        lock = threading.Lock()
        try:
            LogMsg = '[' + datetime.now().strftime('%Y.%m.%d. %H:%M:%S') + '] <' + str(self._mDetail[0]) + ':' + str(self._mDetail[1]) + '> Connection Open'
            if ConnectLog is None:
                ConnectLog = osLogger.cOSLogger(_pPrefix='CONNECT', _pLevel='INFO')
            lock.acquire()
            ConnectLog.writeLog(LogMsg)
            lock.release()

            while True:
                # 데이터 수신 대기
                RecvPacket = str()
                RecvByteStream = (self._mChannel.recv(Global.MAX_BUF))
                RecvPacket = RecvByteStream.decode()

                print(RecvPacket)

        except Exception as Ex:
            if ExceptLog is None:
                ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
            ExceptLog.writeLog('[run:run] ' + str(Ex))
        finally:
            self._mChannel.close()
            LogMsg = '[' + datetime.now().strftime('%Y.%m.%d. %H:%M:%S') + '] <' + str(self._mDetail[0]) + ':' + str(self._mDetail[1]) + '> Connection Close'
            if ConnectLog is None:
                ConnectLog = osLogger.cOSLogger(_pPrefix='CONNECT', _pLevel='INFO')
            lock.acquire()
            ConnectLog.writeLog(LogMsg)
            lock.release()


def write(_pData: object = None):
    pass


def stopServ(_pSignum, _pFrame):
    ExceptLog = None
    StatusLog = None
    try:
        LogMsg = Global.getCurrentTime() + ' Mosquito Data Collector Server Stop [' + str(os.getpid()) + ']'
        if StatusLog is None:
            StatusLog = osLogger.cOSLogger(_pPrefix='STATUS', _pLevel='INFO')
        StatusLog.writeLog(LogMsg)
        sys.exit(0)
    except Exception as Ex:
        # 예외 로그 생성
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[run:stopServ] ' + str(Ex))
    finally:
        # 로그 객체 삭제
        if ExceptLog is not None:
            del ExceptLog
        if StatusLog is not None:
            del StatusLog


def makeDeamon():
    ExceptLog = None
    try:
        if os.fork():
            os._exit(0)

        os.setpgrp()
        os.umask(0)
        sys.stdin.close()
        sys.stdout = None
        sys.stderr = None

        signal.signal(signal.SIGINT, stopServ)
        signal.signal(signal.SIGTERM, stopServ)

    except Exception as Ex:
        # 예외 로그 생성
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[run:makeDeamon] ' + str(Ex))
    finally:
        # 로그 객체 삭제
        if ExceptLog is not None:
            del ExceptLog


def savePid(pid: str = None):
    ExceptLog = None
    try:
        if pid is None:
            raise Exception('Invalid input param : None type')
    except Exception as Ex:
        # 예외 로그 생성
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[run:savePid] ' + str(Ex))
    finally:
        # 로그 객체 삭제
        if ExceptLog is not None:
            del ExceptLog


def exitServ():
    StatusLog = None
    ExceptLog = None
    try:
        # 서버 시작 로그 생성
        LogMsg = 'Data Collector Server Stop [' + str(os.getpid()) + ']'
        if StatusLog is None:
            StatusLog = osLogger.cOSLogger(_pPrefix='STATUS', _pLevel='INFO')
        StatusLog.writeLog(LogMsg)
    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[run:exitServ] ' + str(Ex))


if __name__ == '__main__':
    atexit.register(exitServ)
    ExceptLog = None
    StatusLog = None
    try:
        # 변수 지정
        MAX_THREAD = 4
        SERVICE_PORT = 7885

        # 데몬 모드 시작
        # if (Global.OPERATION_MODE == 'D') and (Global.getOS() != 'Windows'):
        #    makeDeamon()

        # 서버 시작 로그 생성
        LogMsg = 'Data Collector Server Start [' + str(os.getpid()) + ']'
        if StatusLog is None:
            StatusLog = osLogger.cOSLogger(_pPrefix='STATUS', _pLevel='INFO')
        StatusLog.writeLog(LogMsg)

        # 서버 시작
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', SERVICE_PORT))
        server.listen(MAX_THREAD)

        while True:
            channel, details = server.accept()
            DCSInstance = cDataCapture(channel, details)
            DCSInstance.start()
            gc.collect()
    except KeyboardInterrupt as Ex:
        pass
    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[run:__main__] ' + str(Ex))
    finally:
        pass
