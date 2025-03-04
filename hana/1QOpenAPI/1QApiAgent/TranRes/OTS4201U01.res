BEGIN_TRAN_LAYOUT

	TR_CODE=OTS4201U01, TR_NAME=해외주식온라인주문매수, SERVER=A, ENCODE=0, COMPRESS=0, CERT=0;

	BEGIN_RECORD

		'*******************************************
		'* 통신입력 부분입니다.
		'*******************************************
		REC_NAME=OTS4201U01_in, INOUT=0, ARRAY=0, ARRINFO=;
		BEGIN_INPUT0_ITEM
			 INDEX=0, ITEM=CTNO, TYPE=string, SIZE=9, CAPTION=종합계좌대체번호;
			 INDEX=1, ITEM=APNO, TYPE=string, SIZE=3, CAPTION=계좌상품번호;
			 INDEX=2, ITEM=PWD, TYPE=string, SIZE=64, CAPTION=비밀번호;
			 INDEX=3, ITEM=OVRS_SMBL_CD, TYPE=string, SIZE=12, CAPTION=해외상징코드;
			 INDEX=4, ITEM=OSTK_MKT_CD, TYPE=string, SIZE=2, CAPTION=해외주식시장코드;
			 INDEX=5, ITEM=SELL_BUY_DCD, TYPE=string, SIZE=1, CAPTION=매도매수구분코드;
			 INDEX=6, ITEM=OSTK_ORDR_PRC_DCD, TYPE=string, SIZE=1, CAPTION=해외주식주문가격구분코드;
			 INDEX=7, ITEM=OSTK_ORDR_CND_DCD, TYPE=string, SIZE=1, CAPTION=해외주식주문조건구분코드;
			 INDEX=8, ITEM=ORDR_QNT, TYPE=string, SIZE=19, CAPTION=주문수량;
			 INDEX=9, ITEM=OSTK_ORDR_PRC, TYPE=string, SIZE=24, CAPTION=해외주식주문가격;
			 INDEX=10, ITEM=WRAP_PLN_SN, TYPE=string, SIZE=11, CAPTION=WRAP계획일련번호;
		END_INPUT0_ITEM

		'*******************************************
		'* 통신출력 부분입니다.
		'*******************************************
		REC_NAME=OTS4201U01_out, INOUT=1, ARRAY=0, ARRINFO=;
		BEGIN_OUTPUT0_ITEM
			 INDEX=0, ITEM=ORDR_SN, TYPE=string, SIZE=11, CAPTION=주문일련번호;
		END_OUTPUT0_ITEM

	END_RECORD

END_TRAN_LAYOUT



/**********************************************
 개발 편의를 위한 SetTranInputData 메소드 MFC 소스 템플릿
 I N - P U T
 **********************************************/
CString strCTNO;		//종합계좌대체번호
CString strAPNO;		//계좌상품번호
CString strPWD;		//비밀번호
CString strOVRS_SMBL_CD;		//해외상징코드
CString strOSTK_MKT_CD;		//해외주식시장코드
CString strSELL_BUY_DCD;		//매도매수구분코드
CString strOSTK_ORDR_PRC_DCD;		//해외주식주문가격구분코드
CString strOSTK_ORDR_CND_DCD;		//해외주식주문조건구분코드
CString strORDR_QNT;		//주문수량
CString strOSTK_ORDR_PRC;		//해외주식주문가격
CString strWRAP_PLN_SN;		//WRAP계획일련번호

int nRequestId = 0;

m_CommAgent.SetTranInputData(nRequestId, "OTS4201U01", "OTS4201U01_in", "CTNO", strCTNO);		//종합계좌대체번호
m_CommAgent.SetTranInputData(nRequestId, "OTS4201U01", "OTS4201U01_in", "APNO", strAPNO);		//계좌상품번호
m_CommAgent.SetTranInputData(nRequestId, "OTS4201U01", "OTS4201U01_in", "PWD", strPWD);		//비밀번호
m_CommAgent.SetTranInputData(nRequestId, "OTS4201U01", "OTS4201U01_in", "OVRS_SMBL_CD", strOVRS_SMBL_CD);		//해외상징코드
m_CommAgent.SetTranInputData(nRequestId, "OTS4201U01", "OTS4201U01_in", "OSTK_MKT_CD", strOSTK_MKT_CD);		//해외주식시장코드
m_CommAgent.SetTranInputData(nRequestId, "OTS4201U01", "OTS4201U01_in", "SELL_BUY_DCD", strSELL_BUY_DCD);		//매도매수구분코드
m_CommAgent.SetTranInputData(nRequestId, "OTS4201U01", "OTS4201U01_in", "OSTK_ORDR_PRC_DCD", strOSTK_ORDR_PRC_DCD);		//해외주식주문가격구분코드
m_CommAgent.SetTranInputData(nRequestId, "OTS4201U01", "OTS4201U01_in", "OSTK_ORDR_CND_DCD", strOSTK_ORDR_CND_DCD);		//해외주식주문조건구분코드
m_CommAgent.SetTranInputData(nRequestId, "OTS4201U01", "OTS4201U01_in", "ORDR_QNT", strORDR_QNT);		//주문수량
m_CommAgent.SetTranInputData(nRequestId, "OTS4201U01", "OTS4201U01_in", "OSTK_ORDR_PRC", strOSTK_ORDR_PRC);		//해외주식주문가격
m_CommAgent.SetTranInputData(nRequestId, "OTS4201U01", "OTS4201U01_in", "WRAP_PLN_SN", strWRAP_PLN_SN);		//WRAP계획일련번호




/**********************************************
 개발 편의를 위한 GetTranOutputData 메소드 MFC 소스 템플릿
 O U T - P U T
 **********************************************/
CString strORDR_SN = m_CommAgent.GetTranOutputData("OTS4201U01", "OTS4201U01_out", "ORDR_SN", 0);		//주문일련번호
