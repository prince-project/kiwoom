/*----------------------------------------*
| 프로그램명 : 하나금융투자 Open API 예제
| 버      전 : v 
| 배포  일자 :
| 기      타 :
*----------------------------------------*/

#pragma once
#include "hfcommagent.h"
#include "afxwin.h"
#include "afxcmn.h"
#include "afxdtctl.h"

// CStockSiseDlg 대화 상자입니다.

class CStockSiseDlg : public CDialog
{
public:
	CStockSiseDlg(CWnd* pParent = NULL);   // 표준 생성자입니다.

// 대화 상자 데이터입니다.
	enum { IDD = IDD_STOCK_SISE_DLG };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 지원입니다.

	HICON m_hIcon;

	// 생성된 메시지 맵 함수
	virtual BOOL OnInitDialog();

private:
	//호가 배경색 브러쉬
	CBrush m_brushSellBack;			//매수 배경색 브러쉬
	CBrush m_brushBuyBack;			//매도 배경색 브러쉬

	BOOL m_bCommConnect;			//통신연결 상태(TRUE:연결, FALSE:끊김)
	CString m_strLoginID;			//로그인 ID
	CString m_strLoginPwd;			//로그인 비밀번호
	CString m_strCertPwd;			//공인인증 비밀번호

	//Requet ID(조회 고유키)
	int m_nRqIdHoga;				//주식 5단계호가 조회 Request ID
	int m_nRqIdCurPrice;			//주식 현재가 조회 Request ID
	int m_nRqIdTick;				//주식 시간대별체결 조회 Request ID
	int m_nRqIdCodeList;			//주식 종목 리스트(마스터) 조회 Request ID
	int m_nRqIdChart;				//주식 차트 데이터 조회 Request ID
	int m_nRqIdPortfolio;			//관심종목형(Portfolio) 조회 Request ID
	int m_nRqIdCurRate;				//환율 조회 Request ID
	int m_nRqIdKospi;				//지수인덱스 조회 Request ID
	int m_nRqIdMem;					//거래원 순매수매도 조회 Request ID

	int m_nSeverType;				//0-리얼, 1-국내모의, 2-해외무의

	//실시간 등록키(종목코드)
	CString m_strHogaRealKey;		//주식 5단계호가 실시간 등록키
	CString m_strCurPriceRealKey;	//주식 현재가 실시간 등록키
	CString m_strTickRealKey;		//주식 시간대별체결 실시간 등록키

	//연속조회키
	CString m_strTickNextRqKey;		//주식 시간대별체결 연속조회키(다음 조회)
	CString m_strCodeListNextRqKey;	//주식 종목 리스트(마스터) 연속조회키(다음 조회)
	CString m_strChartNextRqKey;	//주식 차트 데이터 연속조회키(다음 조회)

private:
	//주식 시간대별체결 리스트 컨트롤 초기화
	void InitListTick();

	//주식 종목 리스트 컨트롤 초기화
	void InitListCode();

	//주식 차트 리스트 컨트롤 초기화
	void InitListChart();

	//주식 관심종목형 리스트 컨트롤 초기화
	void InitListPortfolio();

	//대비부호
	CString GetDiffSign(CString strSignCode);

	//주식 5단계호가 조회/실시간 데이터 컨트롤 입력
	void SetHogaData(CString* arrSellHoga, CString* arrBuyHoga, CString* arrSellRemain,
		CString* arrBuyRemain, CString* arrSellCnt, CString* arrBuyCnt);

public:
	/****************************************************
	 * Control
	 ****************************************************/
	CHFCommAgent m_CommAgent;	//API Agent control
	CEdit m_editUserID;			//로그인ID
	CEdit m_editPwd;			//로그인 비밀번호
	CEdit m_editAuthPwd;		//공인인증서 비밀번호

	CEdit m_editSymbolPrice;	//주식 현재가 종목코드
	CEdit m_editSymbol;			//주식 5단계호가 종목코드
	CEdit m_editSymbolTick;		//주식 시간대별체결 종목코드
	CListCtrl m_listTick;		//주식 시간대별체결 리스트
	CListCtrl m_listCode;		//주식 종목 리스트
	CListCtrl m_listPortfolio;	//주식 관심종목형 리스트

	CButton m_chkAutoReq;		//자동 다음 조회 체크박스

	CEdit m_editSymbolChart;	// 주식 차트 종목코드
	CButton m_chkAutoReqChart;	// 차트 자동 다음 조회 체크박스
	CListCtrl m_listChart;		// 주식 차트 리스트
	CEdit m_editChartCnt;		// 주식 차트 조회 데이터 조회 건수
	CDateTimeCtrl m_dateTimeFrom;	//차트 조회 일자 시작
	CDateTimeCtrl m_dateTimeTo;		//차트 조회 일자 종료

	DECLARE_MESSAGE_MAP()

	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	afx_msg void OnDestroy();
	afx_msg void OnClose();
	afx_msg void OnTimer(UINT_PTR nIDEvent);
	afx_msg HBRUSH OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor);
	afx_msg void OnNMDblclkListSymbol(NMHDR *pNMHDR, LRESULT *pResult);
	afx_msg void OnRadioChartTerm(UINT nID);

	//접속서버 라디오
	afx_msg void OnRdoSelectServer(UINT nID);

	/****************************************************
	* 통모듈 초기화 및 연결/해제
	****************************************************/
	afx_msg void OnBnClickedInitcomm();			//통신 연결
	afx_msg void OnBnClickedTerminate();		//통신연결 해제

	/****************************************************
	* 로그인/로그아웃
	****************************************************/
	afx_msg void OnBnClickedLogin();			//로그인
	afx_msg void OnBnClickedLogout();			//로그아웃

	/****************************************************
	* 종목 리스트(마스터) 조회
	****************************************************/
	afx_msg void OnBnClickedBtnReqCodeList();	//종목 리스트 조회
	afx_msg void OnBnClickedBtnReqCodeListNext();//종목 리스트 다음 조회

	/****************************************************
	* 주식 현재가 조회
	****************************************************/
	afx_msg void OnBnClickedBtnReqPrice();		//주식 현재가 조회

	/****************************************************
	* 주식 5단계호가 조회
	****************************************************/
	afx_msg void OnBnClickedBtnReqHoga();		//주식 5단계호가 조회

	/****************************************************
	* 주식 시간대별체결 조회
	****************************************************/
	afx_msg void OnBnClickedBtnReqTick();		//주식 시간대별체결 조회
	afx_msg void OnBnClickedBtnReqTickNext();	//주식 시간대별체결 다음 조회

	/****************************************************
	* 주식 차트 데이터 조회
	****************************************************/
	afx_msg void OnBnClickedBtnReqChart();		//주식 차트 데이터 조회
	afx_msg void OnBnClickedBtnReqChartNext();	//주식 차트 다음 데이터 조회

	/****************************************************
	* 관심종목형(Portfolio) 조회
	****************************************************/
	afx_msg void OnBnClickedBtnReqPortfolio();

	/****************************************************
	* 환율 조회
	****************************************************/
	afx_msg void OnBnClickedBtnReqCurRate();

	/****************************************************
	* 지수 조회
	****************************************************/
	afx_msg void OnBnClickedBtnReqKospi();

	/****************************************************
	* 거래원 순매수매도 상위
	****************************************************/
	afx_msg void OnBnClickedBtnReqMem();

	/****************************************************
	* 거래원별 순매수 순매도 상위
	****************************************************/
	afx_msg void OnBnClickedBtnMemRank();

	/****************************************************
	* 대화창 종료
	****************************************************/
	afx_msg void OnBnClickedOk();

	DECLARE_EVENTSINK_MAP()

	/****************************************************
	* API Agent Event Handler
	****************************************************/
	//조회 Tran데이터 수신 이벤트
	void OnGetTranData(LONG nRequestId, LPCTSTR pBlock, long nBlockLength);

	//Fid조회 데이터 수신 이벤트
	void OnGetFidData(LONG nRequestId, LPCTSTR pBlock, long nBlockLength);

	//실시간 데이터 수신 이벤트
	void OnGetRealData(LPCTSTR strRealName, LPCTSTR strRealKey, LPCTSTR pBlock, long nBlockLength);

	//에이전트 이벤트 핸들러
	void OnAgentEventHandler(long nEventType, long nParam, LPCTSTR strParam);
};
