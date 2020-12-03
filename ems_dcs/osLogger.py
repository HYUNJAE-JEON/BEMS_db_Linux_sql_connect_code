#!/usr/bin/env python3
# -*-coding:utf-8-*-

# =======================================================================================================================
# 이 모듈은 로그를 생성하는 기능 수행
# 작성자 : 이현신
# 생성일자 : 2020. 02. 02.
# =======================================================================================================================


import os
import logging as log
import logging.handlers
from datetime import datetime


class cOSLogger:
    _mLog = None
    _mBaseDirectory = None
    _mTodayDirectory = None
    _mFileName = None
    _mFullPath = None
    _mPrefix = None
    _mPostfix = None
    _mLevel = log.WARNING
    _mExceptionLog = log.getLogger('ExceptionLog')

    # 생성자
    def __init__(self, _pBase: str = None, _pPrefix: str = None, _pPostfix: str = None, _pLevel: str = 'WARNING'):
        try:
            # 로그 파일 저장 경로 설정
            if _pBase is None:
                self._mBaseDirectory = str(os.path.join(os.getcwd(), 'LOG'))
            else:
                self._mBaseDirectory = _pBase

            # 로그 파일 Prefix 설정
            if _pPrefix is not None:
                self._mPrefix = _pPrefix

            # 로그 파일 Postfix 설정
            if _pPostfix is not None:
                self._mPostfix = _pPostfix

            # 로그 객체 생성
            if self._mLog is None:
                self._mLog = log.getLogger('OSLogger')

            # 레벨설정
            self.setLevel(_pLevel)

            # 콘솔 출력 핸들러 추가
            if not self._mLog.hasHandlers():
                self._mLog.addHandler(log.StreamHandler())

            # 본 모듈의 예외 로그 출력
            if not self._mExceptionLog.hasHandlers():
                self._mExceptionLog.addHandler(log.StreamHandler())
        except Exception as ex:
            if self._mExceptionLog.hasHandlers():
                self._mExceptionLog.log(str(ex))
            else:
                self._mExceptionLog.addHandler(log.StreamHandler())
                self._mExceptionLog.log(str(ex))

    # 레벨 설정
    def setLevel(self, _pLevel: str = 'WARNING'):
        try:
            if _pLevel.strip() == 'DEBUG':
                self._mLevel = log.DEBUG
                self._mLog.setLevel(log.DEBUG)
            elif _pLevel.strip() == 'INFO':
                self._mLevel = log.INFO
                self._mLog.setLevel(log.INFO)
            elif _pLevel.strip() == 'WARNING':
                self._mLevel = log.WARNING
                self._mLog.setLevel(log.WARNING)
            elif _pLevel.strip() == 'ERROR':
                self._mLevel = log.ERROR
                self._mLog.setLevel(log.ERROR)
            elif _pLevel.strip() == 'CRITICAL':
                self._mLevel = log.CRITICAL
                self._mLog.setLevel(log.CRITICAL)
            else:
                strExcept = str()
                strExcept = '[OSLogger] Invalid Level\n'
                strExcept += '\tDEBUG\n'
                strExcept += '\tINFO\n'
                strExcept += '\tWARNING\n'
                strExcept += '\tERROR\n'
                strExcept += '\tCRITICAL\n'
                raise Exception(strExcept)

        except Exception as ex:
            if self._mExceptionLog.hasHandlers():
                self._mExceptionLog.log(str(ex))
            else:
                self._mExceptionLog.addHandler(log.StreamHandler())
                self._mExceptionLog.log(str(ex))

    # 로그 파일 이름 및 저장 경로 생성 함수
    def setPath(self):
        try:
            strYear = datetime.today().strftime("%Y")
            strMonth = datetime.today().strftime("%m")
            strDay = datetime.today().strftime("%d")
            strHour = datetime.now().strftime("%H")
            self._mTodayDirectory = str(os.path.join(self._mBaseDirectory, strYear, strMonth, strDay, strHour))

            if self._mPrefix is None:
                strPrefix = str()
            else:
                strPrefix = str(self._mPrefix) + '_'

            if self._mPostfix is None:
                strPostfix = str()
            else:
                strPostfix = '_' + str(self._mPostfix)

            self._mFileName = strPrefix.strip() + strYear + strMonth + strDay + strHour + strPostfix.strip() + '.LOG'
            self._mFullPath = str(os.path.join(self._mTodayDirectory, self._mFileName))

            if not (os.path.isdir(self._mTodayDirectory)):
                os.makedirs(self._mTodayDirectory)

        except OSError as ex:
            if ex.errno != os.error.errno.EEXIST:
                self._mExceptionLog.error('Failed to make Log Directory : ' + self._mTodayDirectory)
            else:
                self._mExceptionLog.error(str(ex))

    # 로그 저장 함수
    def writeLog(self, _pMsg: str = None, _pLevel: str = None):
        try:
            # 파일 출력 핸들러 추가
            self.setPath()
            fileHandler = log.handlers.RotatingFileHandler(self._mFullPath)
            formatter = log.Formatter('[%(levelname)s : %(asctime)s] > %(message)s')
            fileHandler.setFormatter(formatter)
            self._mLog.addHandler(fileHandler)
            if _pLevel is not None:
                self.setLevel(_pLevel)
            self._mLog.log(self._mLevel, _pMsg)
            self._mLog.removeHandler(fileHandler)

        except Exception as Ex:
            if self._mExceptionLog.hasHandlers():
                self._mExceptionLog.log(str(Ex))
            else:
                self._mExceptionLog.addHandler(log.StreamHandler())
                self._mExceptionLog.log(str(Ex))


if __name__ == '__main__':
    logger = cOSLogger(_pPrefix='Exception')
    logger.writeLog('TEST', 'INFO')
    logger = cOSLogger(_pPrefix='Exception')
    logger.writeLog('Test', 'WARNING')
    logger = cOSLogger(_pPrefix='Exception')
    logger.writeLog('tttt', 'WARNING')
