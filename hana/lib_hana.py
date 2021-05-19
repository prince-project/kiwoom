import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import pythoncom
import datetime
#from pykiwoom import parser
import pandas as pd
import time
import logging
import os

sys.path.append(os.path.abspath('C:\GitHub\hana'))
#from kiwoomG_parser import *
#from kiwoomK_parser import *

logging.basicConfig(filename="log.txt", level=logging.ERROR)


class Hana:
    def __init__(self, login=False):
        self.ocx = QAxWidget("HFCOMMAGENT.HFCommAgentCtrl.1")
        self.connected = False              # for login event
        self.received = False               # for tr event
        self.tr_items = None                # tr input/output items
        self.tr_data = None                 # tr output data
        self.next = None
        self.tr_record = None
        self.tr_remained = False
        self._set_signals_slots()

        if login:
            self.CommConnect()

    def _handler_login(self, err_code):
        logging.info(f"hander login {err_code}")
        if err_code == 0:
            self.connected = True

    def _handler_tr(self, screen, rqname, trcode, record, next):
        #print('*********************************************')
        #print(next)
        logging.info(f"OnReceiveTrData {screen} {rqname} {trcode} {record} {next}")
        try:
            record = None
            items = None
            self.next = next
            print('*** %s ***' % self.next)
            #print(self.tr_remained)
            #print(self)
            #print(screen)
            #print(rqname)
            #print(record)
            #print(next)
            #print(len(next))
            #if next == 'None':
            #    print("******")
            # remained data
            if len(next) > 1:
                self.tr_remained = True
            else:
                self.tr_remained = False

            #print(self.tr_remained)
            for record in self.tr_items['output'][0]:
                #record = list(output.keys())[0]
                items = self.tr_items['output'][0][record]
                if record == self.tr_record:
                    break
            
            #print(self.tr_items['output'])
            #print(record)
            #print(self.tr_record)
            #print(items)
            rows = self.GetRepeatCnt(trcode, rqname)
            if rows == 0:
                rows = 1

            data_list = []
            for row in range(rows):
                row_data = []
                for item in items:
                    #print(item)
                    data = self.GetCommData(trcode, rqname, row, item)
                    row_data.append(data)
                data_list.append(row_data)

            # data to DataFrame
            df = pd.DataFrame(data=data_list, columns=items)
            self.tr_data = df
            self.received = True
        except:
            pass

    def _handler_msg(self, screen, rqname, trcode, msg):
        logging.info(f"OnReceiveMsg {screen} {rqname} {trcode} {msg}")

    def _handler_chejan(self, gubun, item_cnt, fid_list):
        logging.info(f"OnReceiveChejanData {gubun} {item_cnt} {fid_list}")

    def _set_signals_slots(self):
        self.ocx.OnAgentEventHandler.connect(self._handler_login)
        #self.ocx.OnReceiveTrData.connect(self._handler_tr)
        #self.ocx.OnReceiveMsg.connect(self._handler_msg)
        #self.ocx.OnReceiveChejanData.connect(self._handler_chejan)

    #-------------------------------------------------------------------------------------------------------------------
    # API 메소드 상세
    #-------------------------------------------------------------------------------------------------------------------

    ## 통신 관련
    def CommInit(self):
        """
        01
        원형: LONG CommInit(void)
        기능: 통신모듈 초기화 및 연결
        호출: 로그인 처리전에 호출한다.
        인자: void
              없음
        반환: LONG
              0: 성공, 음수: 오류
        """
        return self.ocx.dynamicCall("CommInit()")

    def CommTerminate(self, bSocketClose):
        """
        02
        원형: void CommTerminate(LONG bSocketClose)
        기능: 연결 해제
        호출: 로그아웃 처리 이후에 호출한다.
        인자: LONG bSocketClose
              1: 통신모듈 종료 및 연결 해제, 0 : 통신모듈과 연결 해제
        반환: void
              없음
        """
        self.ocx.dynamicCall("CommTerminate(int)", bSocketClose)

    def CommGetConnectState(self):
        """
        03
        원형: LONG CommGetConnectState(void)
        기능: 통신연결 상태 확인
        호출: CommInit 메소드 호출 후 통신연결 상태 확인을 위해 호출한다.
        인자: void	
              없음
        반환: LONG 
              0: 연결 끊김, 1: 연결
        """
        return self.ocx.dynamicCall("CommGetConnectState()")

    def CommLogin(self, sUserID, sPwd, sCertPwd):
        """
        04
        원형: LONG CommLogin(BSTR sUserID, BSTR sPwd, BSTR sCertPwd)
        기능: 로그인 처리
        호출: CommInit 호출 이후 통신 연결이 완료된 이후에 호출한다.
        인자: BSTR sUserID - 로그인 ID
              BSTR sPwd - 로그인 비밀번호
              BSTR sCertPwd	- 공인인증 비밀번호
        반환: LONG
              0: 실패, 1: 성공
        """
        return self.ocx.dynamicCall("CommLogin(QString, QString, QString)", sUserID, sPwd, sCertPwd)

    def CommLogout(self, sUserID):
        """
        05
        원형: LONG CommLogout(BSTR sUserID)
        기능: 로그아웃 처리
        호출: CommTerminate 호출 전에 호출한다.
        인자: BSTR sUserID - 로그인 ID
        반환: LONG
            0: 성공
        """
        return self.ocx.dynamicCall("CommLogout(QString)", sUserID)

    def GetLoginState(self):
        """
        06
        원형: LONG GetLoginState(void)
        기능: 로그인상태 확인
        호출: CommLogin 메소드 호출 이후, 로그인 상태 확인 목적으로 호출한다.
        인자: void
              없음
        반환: LONG
            0: 로그아웃, 1: 로그인
        """
        return self.ocx.dynamicCall("GetLoginState()")

    def SetLoginMode(self, nOption, nMode):
        """
        07
        원형: void SetLoginMode(LONG nOption, LONG nMode)
        기능: 로그인모드 설정
        호출: CommLogin 메소드 호출전, 로그인 접속 설정을 한다..
        인자: LONG nOption
            0: 모의투자 구분, 1: 시세전용 구분
            LONG nMode	
            if nOption(0) then  0:실거래, 1:국내모의, 2:해외모의
            if nOption(1) then  0:공인인증, 1:시세전용
        반 환: void
        예) m_commAgentCtrl.SetLoginMode(0, 0) //실거래 로그인
            m_commAgentCtrl.SetLoginMode(0, 1) //국내모의 로그인
            m_commAgentCtrl.SetLoginMode(1, 1) //시세전용 로그인(인증서X)
        """
        self.ocx.dynamicCall("SetLoginMode(int, int)", nOption, nMode)

    def GetLoginMode(self, nOption):
        """
        08
        원형: LONG GetLoginMode(LONG nOption)
        기능: 로그인상태 확인
        호출: CommLogin 메소드 호출 이후, 로그인 상태 확인 목적으로 호출한다.
        인자: LONG nOption
            0: 모의투자 체크, 1: 시제전용, 2: 직원/고객 로그인
        반환: LONG	
            -1: 실패, 
            성공: -1보다 큰 양수
        """
        return self.ocx.dynamicCall("GetLoginMode(int)", nOption)

    ## 리소스관련
    def LoadTranResource(self, strFilePath):
        """
        10
        원형: LONG LoadTranResource(BSTR strFilePath)
        기능: Tran조회 I/O Block 정보 리소스파일 로드
        호출: Tran조회 시에 반드시 리소스파일이 에이전트 컨트롤에 적재되어 있어야한다.
        인자: BSTR strFilePath	
            Tran I/O Block 정보 리소스파일(*.res) 경로
        반환: LONG	
            0: 실패, 1: 성공
        """
        return self.ocx.dynamicCall("LoadTranResource(QString)", strFilePath)

    def LoadRealResource(self, strFilePath):
        """
        11
        원형: LONG LoadRealResource(BSTR strFilePath)
        기능: 실시간 Block 정보 리소스파일 로드
        호출: 실시간 등록 시에 반드시 리소스파일이 에이전트 컨트롤에 적재되어 있어야한다.
        인자: BSTR strFilePath	
            실시간Block정보 리소스파일(*.res) 경로
        반환: LONG	
            0: 실패, 1: 성공
        """
        return self.ocx.dynamicCall("LoadRealResource(QString)", strFilePath)

    ## 통신조회관련공통
    def CreateRequestID(self):
        """
        15
        원형: LONG CreateRequestID(void)
        기능: 조회고유ID 생성(Request ID)
        호출: Tran/FID조회 시, RQ ID를 먼저 생성한다.
        인자: Void
            없음
        반환: LONG 신규 RQ ID 반환
            음수: 실패, 2보다 큰 정수: 성공)
        """
        return self.ocx.dynamicCall("CreateRequestID()")

    def GetCommRecvOptionValue(self, nOptionType):
        """
        16
        원형: BSTR GetCommRecvOptionValue(LONG nOptionType)
        기능: 조회응답 부가정보/옵션값 반환
        호출: Tran/FID조회(OnGetTranData, OnGetFidData) 응답 이벤트 안에서만 호출한다.
        인자: LONG nOptionType
            CommRecvOpt::TranCode= 0 : Tr코드
            CommRecvOpt::PrevNextCode= 1 : 연속데이타구분 
            (0:없음, 1:이전, 2:다음, 3:이전/다음)
            CommRecvOpt::PrevNextKey= 2 : 연속조회키
            CommRecvOpt::MsgCode= 3 : 메시지코드
            CommRecvOpt::Msg= 4 : 메시지
            CommRecvOpt::SubMsgCode= 5 : 부가메시지코드
            CommRecvOpt::SubMsg=6 : 부가메시지
        반환: BSTR nOptionType에 대응하는 문자열값 반환
        """
        return self.ocx.dynamicCall("GetCommRecvOptionValue(int)", nOptionType)

    def ReleaseRqId(self, nRqId):
        """ 
        17   
        원형: LONG ReleaseRqId(LONG nRqId)
        기능: 조회고유ID(Request ID) 할당 해제
        호출: CreateRequestID 함수로 생성(할당)한RQ ID를 해제할 때 사용.
        인자: LONG nRqId	
            CreateRequestID로 생성(할당) 받은 RQ ID
        반환: void
            없음
        """
        self.ocx.dynamicCall("ReleaseRqId(int)", nRqId)

    ## Tran조회관련
    def SetTranInputData(self, nRqId, strTrCode, strRecName, strItem, strValue):
        """
        20
        원형: LONG SetTranInputData(LONG nRqId, BSTR strTrCode, BSTR strRecName, BSTR strItem, BSTR strValue)
        기능: Tran조회, 항목별 입력값을 입력한다
        호출: RequestTran 호출 전에 통신 Input데이터 입력 목적으로 호출한다.
        인자: LONG nRqId - 조회고유ID(Request ID) - CreateRequestID메소드로 생성
              BSTR strTrCode - 서비스Tr코드(Tran 리소스파일(*.res)파일의 'TR_CODE=' 항목)
              BSTR strRecName - Input레코드명(Tran 리소스파일(*.res)파일의 'REC_NAME=' 항목)
              BSTR strItem - Input항목명(Tran 리소스파일(*.res)파일의 'ITEM=' 항목)
              BSTR strValue	- Input항목에 대응하는 입력값
        반환: LONG
            0: 실패, 1: 성공
        """
        return self.ocx.dynamicCall("SetTranInputData(int, QString, QString, QString, QString)",  nRqId, strTrCode, strRecName, strItem, strValue)

    def RequestTran(self, nRqId, sTrCode, sIsBenefit, sPrevOrNext, sPrevNextKey, sScreenNo, sTranType, nRequestCount):
        """
        21
        원형: LONG RequestTran(LONG nRqId, BSTR sTrCode, BSTR sIsBenefit, BSTR sPrevOrNext, BSTR sPrevNextKey, BSTR sScreenNo, BSTR sTranType, LONG nRequestCount)
        기능: Tran조회 요청
        호출: 서버에 Tran조회 요청 시 호출
        인자: LONG nRqId - 조회고유ID(Request ID) - (CreateRequestID메소드로 생성)
              BSTR sTrCode - 서비스Tr코드(Tran 리소스파일(*.res)파일의 'TR_CODE=' 항목)
              BSTR sIsBenefit - 수익계좌여부("Y", "N")
              BSTR sPrevOrNext - 연속조회구분 ("0" :일반조회, "1" : 연속조회 첫 조회, "2" : 이전조회, "3" : 다음조회)
              BSTR sPrevNextKey - 다음/이전 조회 시 연속구분이 되는 키값 입력(조회응답으로 내려 온다.)
              BSTR sScreenNo - 화면번호(ex-> "9999")
              BSTR sTranType - Q': 조회,'U': Update (보통 조회는 'Q', 주문 등은 'U'를 입력한다.)
              LONG RequestCount - 조회 응답으로 받을 최대 데이터 건수(Maxium : 9999)
        반환: LONG
            음수: 실패, 0보다 큰 정수: 성공
        """
        return self.ocx.dynamicCall("RequestTran(int, QString, QString, QString, QString, QString, QString, int)",  nRqId, sTrCode, sIsBenefit, sPrevOrNext, sPrevNextKey, sScreenNo, sTranType, nRequestCount)

    def GetTranOutputRowCnt(self, strTrCode, strRecName):
        """
        22
        원형: LONG GetTranOutputRowCnt(BSTR strTrCode, BSTR strRecName)
        기능: Tran조회응답 데이터 건수 반환
        호출: Tran조회응답 이벤트(OnGetTranData) 안에서만 호출한다.
        인자: BSTR strTrCode - 서비스 Tr코드(Tran 리소스파일(*.res)파일의 'TR_CODE=' 항목)
            BSTR strRecName - Input 레코드명(Tran 리소스파일(*.res)파일의 'REC_NAME=' 항목) 
        반환: LONG
            0: 데이터 없음, 0보다 큰 정수: 데이터 건수
        """
        return self.ocx.dynamicCall("GetTranOutputRowCnt(QString, QString)",  strTrCode, strRecName)

    def GetTranOutputData(self, strTrCode, strRecName, strItemName, nRow):
        """
        23
        원형: BSTR GetTranOutputData(BSTR strTrCode, BSTR strRecName, BSTR strItemName, LONG nRow)
        기능: Tran조회 항목별 응답데이터 반환
        호출: Tran조회 응답 이벤트(OnGetTranData) 안에서만 호출한다.
        인자: BSTR strTrCode
              BSTR strRecName
              BSTR strItemName
              LONG nRow
        반환: BSTR
        """
        return self.ocx.dynamicCall("GetTranOutputData(QString, QString, QString, int)",  strTrCode, strRecName, strItemName, nRow)

    def SetTranInputArrayCnt(self, nRqId, strTrCode, strRecName, nRecCnt):
        """
        24
        원형: LONG SetTranInputArrayCnt(LONG nRqId, BSTR strTrCode, BSTR strRecName, LONG nRecCnt)
        기능: Tran조회 입력 데이터 건수 설정
        호출: RequestTran 호출 전에 통신 Input데이터 건수 입력 목적으로 호출한다.
        인자: LONG nRqId
              BSTR strTrCode
              BSTR strRecName : 입력 레코드명
              LONG nRecCnt : 데이터 입력 건수
        반환: LONG
              0: 실패, 1: 성공
        """
        return self.ocx.dynamicCall("SetTranInputArrayCnt(int, QString, QString, int)",  nRqId, strTrCode, strRecName, nRecCnt)

    def SetTranInputArrayData(self, nRqId, strTrCode, strRecName, strItem, strValue, nArrayIndex):
        """
        25
        원형: LONG SetTranInputArrayData(LONG nRqId, BSTR strTrCode, BSTR strRecName, BSTR strItem, BSTR strValue, LONG nArrayIndex)
        기능: Tran조회 복수건 입력
        호출: RequestTran 호출 전에 통신 복수건 Input데이터 입력 목적으로 호출한다.
        인자: LONG nRqId
              BSTR strTrCode
              BSTR strRecName : 입력 레코드명
              BSTR strItem : 항목명
              BSTR strValue : 입력값
              LONG nArrayIndex : 레코드 인덱스(0부터 시작)
        반환: LONG
              0 : 실패, 1 : 성공
        """
        return self.ocx.dynamicCall("SetTranInputArrayData(int, QString, QString, QString, QString, int)",  nRqId, strTrCode, strRecName, strItem, strValue, nArrayIndex)





    def CommConnect(self, block=True, login_type=0): # checked
        """
        로그인 윈도우를 실행합니다.
        :param block: True: 로그인완료까지 블록킹 됨, False: 블록킹 하지 않음
        : 0 - 버전 수동처리, 1 - 버전 자동처리
        :return: None
        """
        self.ocx.dynamicCall("CommConnect(%s)"%login_type)
        if block:
            while not self.connected:
                pythoncom.PumpWaitingMessages()

    def CommRqData(self, rqname, trcode, next, screen): # checked
        """
        TR을 서버로 송신합니다.
        :param rqname: 사용자가 임의로 지정할 수 있는 요청 이름
        :param trcode: 요청하는 TR의 코드
        :param next: 0: 처음 조회, 2: 연속 조회
        :param screen: 화면번호 ('0000' 또는 '0' 제외한 숫자값으로 200개로 한정된 값
        :return: None
        """
        #print("***** CommRqData *****")
        #print(rqname)
        #print(trcode)
        self.ocx.dynamicCall("CommRqData(QString, QString, QString, QString)", rqname, trcode, next, screen)

    def SetInputValue(self, id, value): #checked
        """
        TR 입력값을 설정하는 메서드
        :param id: TR INPUT의 아이템명
        :param value: 입력 값
        :return: None
        """
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

    def GetCommData(self, trcode, rqname, index, item): #checked
        """
        수신 데이터를 가져가는 메서드
        :param trcode: TR 코드
        :param rqname: 요청 이름
        :param index: 멀티데이터의 경우 row index
        :param item: 얻어오려는 항목 이름
        :return: 수신 데이터
        :ex) 현재가출력 - GetCommData("OPT00001", "해외선물기본정보", 0, "현재가")
        """
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, item)
        return data.strip()

    #def CommTerminate(self): #checked
    #    """
    #    OpenAPI의 서버 접속을 해제한다
    #    """
    #    self.ocx.dynamicCall("CommTerminate()")

    def GetRepeatCnt(self, trcode, rqname): #checked
        """
        레코드 반복횟수를 반환
        멀티데이터의 행(row)의 개수를 얻는 메서드
        :param trcode: TR코드
        :param rqname: 사용자가 설정한 요청이름
        :return: 멀티데이터의 행의 개수
        :        레코드의 반복횟수
        :ex) GetRepeatCnt("OPT00001", "해외선물체결데이타")
        """
        count = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return count

    def DisconnectRealData(self, screen): #checked
        """
        화면번호에 대한 리얼 데이터 요청을 해제하는 메서드
        :param screen: 화면번호
        :return: None
        """
        self.ocx.dynamicCall("DisconnectRealData(QString)", screen)

    def GetCommRealData(self, code, fid): #checked
        """
        실시간 데이터를 반환
        ex) GetCommRealData("해외선물시세", 10)
        """
        data = self.ocx.dynamicCall("GetCommRealData(QString, int)", code, fid)
        return data

    def GetChejanData(self, fid): #checked
        """
        체결잔고 데이터 반환
        ex) GetChejanData(910) //체결가격
        """
        data = self.ocx.dynamicCall("GetChejanData(int)", fid)
        return data

    def SendOrder(self, rqname, screen, accno, order_type, code, quantity, price, stop, hoga, order_no): #checked
        """
        주문을 서버로 전송하는 메서드
        시장가 주문시 주문단가는 0으로 입력해야 함 (가격을 입력하지 않음을 의미)
        :param rqname: 사용자가 임의로 지정할 수 있는 요청 이름
        :param screen: 화면번호[4] (1~9999 :숫자값으로만 가능)
        :param accno: 계좌번호[10]
        :param order_type: 주문유형 (1:신규매도, 2:신규매수, 3:매도취소, 4:매수취소, 5:매도정정, 6:매수정정)
        :param code: 종목코드
        :param quantity: 주문수량
        :param price: 주문단가
        :param stop: Stop단가
        :param hoga: 거래구분 (1:시장가, 2:지정가, 3:STOP, 4:STOP LIMIT)
        :param order_no: 원주문번호
        :return:
        ex)
        지정가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 2, “6AH16”, 10, “0.7900”, “2”, “”);
        시장가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 2, “6AH16”, 10, “0”, “1”, “”);
        매수 정정 - openApi.SendOrder(“RQ_1”,“0101”, “5015123410”, 6, “6AH16”, 10, “0.7800”, “0”, “200060”);
        매수 취소 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 4, “6AH16”, 10, “0”, “0”, “200061”);
        """
        ret = self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, QString, QString, QString, QString)",
                                   [rqname, screen, accno, order_type, code, quantity, price, stop, hoga, order_no])
        return ret


    def GetLoginInfo(self, tag): #checked
        """
        로그인한 사용자 정보를 반환하는 메서드
        :param tag: ("ACCOUNT_CNT, "ACCNO", "USER_ID", "USER_NAME", "KEY_BSECGB", "FIREW_SECGB")
        :return: tag에 대한 데이터 값
        """
        data = self.ocx.dynamicCall("GetLoginInfo(QString)", tag)

        if tag == "ACCNO":
            return data.split(';')[:-1]
        else:
            return data
    
    def GetGlobalFutureItemlist(self): #checked
        """
        해외선물 상품리스트를 반환
        """
        data = self.ocx.dynamicCall("GetGlobalFutureItemlist()")
        return data
    
    def GetGlobalOptionItemlist(self): #checked
        """
        해외옵션 상품리스트를 반환
        """
        data = self.ocx.dynamicCall("GetGlobalFutureItemlist()")
        return data
    
    def GetGlobalFutureCodelist(self, item): #checked
        """
        해외상품별 해외선물 종목코드리스트를 반환
        :param item: 해외상품
        :return:
        """
        data = self.ocx.dynamicCall("GetGlobalFutureCodelist(QString)", item)
        return data

    def GetGlobalOptionCodelist(self, item): #checked
        """
        해외상품별 해외옵션 종목코드리스트를 반환
        :param item: 해외상품
        :return:
        """
        data = self.ocx.dynamicCall("GetGlobalFutureCodelist(QString)", item)
        return data

    def GetConnectState(self): #checked
        """
        현재접속 상태를 반환하는 메서드
        :return: 0:미연결, 1: 연결완료
        """
        ret = self.ocx.dynamicCall("GetConnectState()")
        return ret

    def GetAPIModulePath(self): #checked
        """
        OpenAPI 모듈의 경로를 반환하는 메서드
        :return: 모듈의 경로
        """
        ret = self.ocx.dynamicCall("GetAPIModulePath()")
        return ret

    def GetCommonFunc(self, func_name, param): #checked
        """
        공통함수로 추후 추가함수가 필요시 사용할 함수
        :param func_name: 함수명
        :param param: 인자값
        :return: 문자값으로 반환
        """
        ret = self.ocx.dynamicCall("GetCommonFunc(QString, QString)", [func_name, param])
        return ret

    def GetConvertPrice(self, code, price, ntype): # checked
        """
        가격 진법에 따라 변환된 가격을 반환
        :param code: 종목코드
        :param price: 가격
        :param ntype: 타입(0 : 진법->10진수, 1 : 10진수->진법)
        :return: 문자값으로 반환
        """
        ret = self.ocx.dynamicCall("GetConvertPrice(QString, QString, int)", [code, price, ntype])
        return ret 

    def GetGlobalFutOpCodeInfoByType(self, gubun, stype): #checked
        """
        해외선물옵션종목코드정보를 타입별로 반환
        :param gubun: 0(해외선물), 1(해외옵션)
        :param stype: IDX(지수), CUR(통화), INT(금리), MLT(금속), ENG(에너지), CMD(농산물)
        :return: 종목코드정보리스트들을 문자값으로 반환
        """
        ret = self.ocx.dynamicCall("GetGlobalFutOpCodeInfoByType(int, QString)", [gubun, stype])
        return ret 

    def GetGlobalFutOpCodeInfoByCode(self, scode): #checked
        """
        해외선물옵션종목코드정보를 종목코드별로 반환
        :param scode: 해외선물옵션 종목코드
        :return: 종목코드정보리스트들을 문자값으로 반환
        """
        ret = self.ocx.dynamicCall("GetGlobalFutOpCodeInfoByCode(QString)", scode)
        return ret 

    def GetGlobalFutureItemlistByType(self, stype): #checked
        """
        해외선물상품리스트를 타입별로 반환
        :param stype: IDX(지수), CUR(통화), INT(금리), MLT(금속), ENG(에너지), CMD(농산물)
        :return: 상품리스트를 문자값으로 반환
        """
        ret = self.ocx.dynamicCall("GetGlobalFutureItemlistByType(QString)", stype)
        return ret 

    def GetGlobalFutureCodeByItemMonth(self, sitem, smonth): #checked
        """
        해외선물종목코드를 상품/월물별로 반환
        :param sitem: 상품코드(6A, ES..)
        :param smonth: “201606”
        :return: 종목코드를 문자값으로 반환
        """
        ret = self.ocx.dynamicCall("GetGlobalFutureCodeByItemMonth(QString, QString)", [sitem, smonth])
        return ret 

    def GetGlobalOptionCodeByMonth(self, sitem, cp_gubun, act_price, smonth): #checked
        """
        해외옵션종목코드를 상품/콜풋/행사가/월물별로 반환
        :param sitem: 상품코드(6A, ES..)
        :param cp_gubun: C(콜)/P(풋)
        :param act_price: 0.760
        :param smonth: “201606”
        :return: 종목코드를 문자값으로 반환
        """
        ret = self.ocx.dynamicCall("GetGlobalOptionCodeByMonth(QString, QString, QString, QString)", [sitem, cp_gubun, act_price, smonth])
        return ret 

    def GetGlobalOptionMonthByItem(self, sitem): #checked
        """
        해외옵션월물리스트를 상품별로 반환
        :param sitem: 상품코드(6A, ES..)
        :return: 월물리스트를 문자값으로 반환
        """
        ret = self.ocx.dynamicCall("GetGlobalOptionMonthByItem(QString)", sitem)
        return ret 

    def GetGlobalOptionActPriceByItem(self, sitem): #checked
        """
        해외옵션행사가리스트를 상품별로 반환
        :param sitem: 상품코드(6A, ES..)
        :return: 행사가리스트를 문자값으로 반환
        """
        ret = self.ocx.dynamicCall("GetGlobalOptionActPriceByItem(QString)", sitem)
        return ret 

    def GetGlobalFutureItemTypelist(self): #checked
        """
        해외선물상품타입리스트를 반환
        :return: 상품타입리스트를 문자값으로 반환; e.g) IDX;CUR;INT;MLT;ENG;CMD; 반환
        """
        ret = self.ocx.dynamicCall("GetGlobalFutureItemTypelist()")
        return ret

    def GetCommFullData(self, tr_code, record_name, gubun): #checked
        """
        수신된 전체데이터를 반환
        :param tr_code: Tran 코드
        :param record_name: 레코드명
        :param gubun: 0 : 전체(싱글+멀티), 1 : 싱글데이타, 2 : 멀티데이타
        :return: 수신 전체데이터를 문자값으로 반환
        :비고
            WKOAStudio의 TR목록탭에서 필드 사이즈 참조.(필드명 옆 가로안의 값들)
            모든 시세/원장 조회에 사용 가능하며, 특히 차트데이타 같은 대용량 데이터를 한번에 받아서 처리가능
        """
        ret = self.ocx.dynamicCall("GetCommFullData(QString, QString, int)", [tr_code, record_name, gubun])
        return ret 

    def block_request(self, *args, **kwargs):
        trcode = args[0].lower()
        lines = read_trinfo(trcode, dir_path)
        #print(trcode)
        #print(lines)
        self.tr_items = parse_trinfo(trcode, lines)
        self.tr_record = kwargs["output"]
        next = kwargs["next"]

        # set input
        for id in kwargs:
            if id.lower() != "output" and id.lower() != "next":
                self.SetInputValue(id, kwargs[id])

        # initialize
        self.received = False
        self.tr_remained = False

        #print(trcode)
        #print(args)
        #print(kwargs)
        #print(self.tr_items)
        #print(self.tr_record)
        # request
        #print(self.tr_record)
        #print("11111 %s" % self.next)
        if self.tr_record == 'single':
            #print("***** single *****")
            self.CommRqData(trcode, trcode, next, "0101")
        else:
            self.CommRqData(trcode, trcode, next, "0101")
        #print("22222 %s" % self.next)
        while not self.received:
            pythoncom.PumpWaitingMessages()

        return self.tr_data



if not QApplication.instance():
    app = QApplication(sys.argv)

"""
if __name__ == "__main__":
    # 로그인
    kiwoom = KiwoomG()
    kiwoom.CommConnect(block=True)

    # 조건식 load
    kiwoom.GetConditionLoad()

    conditions = kiwoom.GetConditionNameList()

    # 0번 조건식에 해당하는 종목 리스트 출력
    condition_index = conditions[0][0]
    condition_name = conditions[0][1]
    codes = kiwoom.SendCondition("0101", condition_name, condition_index, 0)

    print(codes)
"""