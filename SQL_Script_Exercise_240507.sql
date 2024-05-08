# 실행 Ctrl + Enter

CREATE DATABASE DB_SQLSTK;   # 스키마 : 데이터베이스의 구조와 제약조건에 관해 전반적인 명세를 기술한 것
SHOW DATABASES;
SELECT * FROM STOCK;   # STOCK 테이블의 내용을 모두 보여주기
SELECT STK_CD, STK_NM FROM STOCK;   # STOCK 테이블의 내용 중 종목 코드와 종목 이름 만 출력
SELECT STK_CD, STK_NM, EX_CD FROM STOCK ORDER BY STK_NM;  # STOCK 테이블의 일부 항목만 추출하여 이름을 기준으로 정렬

# 필요한 데이터만 골라내기(WHERE)
SELECT * FROM STOCK WHERE SEC_NM = '자동차' ORDER BY STK_NM;   # 섹터명 '자동차'를 추출하고 이름순으로 정렬

SELECT STK_CD, STK_NM, SEC_NM, EX_CD  # 필요한 항목을 설정
FROM STOCK                            # 테이블 선택
WHERE EX_CD = 'KD'
AND (SEC_NM = '담배' OR SEC_NM = '주류제조업')   # AND와 OR을 혼합해서 사용할 때, 괄호를 적절하게 사용, OR 연결을 사용하는 경우 괄호 사용 습관화할 것
ORDER BY STK_CD ASC;  # ASC 오름차순, DESC 내림차순

SELECT STK_CD, STK_NM, SEC_NM
FROM STOCK
WHERE STK_NM = '삼성전자';  # 특정 이름 지정하여 검색

# 특수조건 : LIKE, IN, BETWEEN
# 기업명에 동일한 이름이 포함되는 계열사 조회하기
SELECT STK_CD, STK_NM, SEC_NM
FROM STOCK
WHERE STK_NM LIKE '삼성%'        # '삼성'이 앞에 포함된 기업명 추출하여 오름차순으로 정렬
ORDER BY STK_NM ASC;            # '삼성'이 포함되어도 계열사가 아닐 수 있다.  

SELECT STK_CD, STK_NM, SEC_NM
FROM STOCK
WHERE SEC_NM = '반도체'
ORDER BY STK_NM ASC;

## 다른 테이블 열어보기
SELECT * FROM HISTORY_DT
ORDER BY DT DESC;   # 일별 정보 : 가장 최신자료가 2020년 12월 30일 종가임을 알 수 있다.


# 테이블 별칭
# FROM절 테이블명 뒤에 한 칸을 띄고 별칭 T1을 정해서 입력한다.
SELECT  T1.STK_CD ,T1.STK_NM ,T1.SEC_NM    # 각 컬럼이 테이블 T1에서 온 것을 의미한다.
FROM    STOCK T1                   # STOCK 테이블을 T1으로 별칭을 지정한다.
WHERE   T1.STK_NM = '삼성전자'
ORDER BY T1.STK_CD ASC;

# Chap 4. 봉 차트와 일별 주가
SELECT T1.* FROM HISTORY_DT T1;   # 별칭을 부여하고 테이블의 내부 내용을 확인

SELECT T1.*     # 테이블의 별칭 T1
FROM HISTORY_DT T1
WHERE T1.DT = STR_TO_DATE('20190102', '%Y%m%d') # 날짜형 변환 : 문자열 20190102를 YYYY-MM-DD / 주의 m 소문자
AND T1.C_PRC > T1.O_PRC     # 종가(C_PRC)가 시가(O_PRC)보다 큰 경우 : 양봉
ORDER BY T1.CHG_RT DESC;    # 양봉 조건인 항목을 찾아서 등락순으로 정리

# 데이터베이스를 이용한 통계 분석(240508)
# 위의 양봉인 조건인 종목의 이름을 확인할 방법 / 양봉 or 음봉 항목의 갯수 통계

# INNER JOIN문의 활용(240508)
# 양봉 종목의 이름 확인
 SELECT * FROM HISTORY_DT;
 SELECT * FROM STOCK;
 SELECT T1.*     # 테이블의 별칭 T1
 
FROM HISTORY_DT T1
	INNER JOIN STOCK T2
    ON (T2.STK_CD = T1.STK_CD)
WHERE T1.DT = STR_TO_DATE('20190102', '%Y%m%d') # 날짜형 변환 : 문자열 20190102를 YYYY-MM-DD / 주의 m 소문자
AND T1.C_PRC > T1.O_PRC     # 종가(C_PRC)가 시가(O_PRC)보다 큰 경우 : 양봉
ORDER BY T1.CHG_RT DESC;    # 양봉 조건인 항목을 찾아서 등락순으로 정리
# 위의 SQL 수정 필요 : 원하는 결과는 '양봉'인 종목의 이름을 출력하는 것

# INNER JOIN 예제 (240508)
SELECT T1.STK_CD, T2.STK_NM, T1.C_PRC, T1.O_PRC
#SELECT T2.STK_NM
FROM  HISTORY_DT T1           
	INNER JOIN STOCK T2
		  ON (T1.STK_CD = T2.STK_CD)     # 테이블의 별칭 T1
WHERE T1.DT = STR_TO_DATE('20190103', '%Y%m%d') # 날짜형 변환 : 문자열 20190102를 YYYY-MM-DD / 주의 m 소문자
#AND T1.C_PRC > T1.O_PRC;     # 종가(C_PRC)가 시가(O_PRC)보다 큰 경우 : 양봉
AND T1.C_PRC/T1.O_PRC > 1.2;  # 종가가 시가 대비 20% 이상 상승 마감한 경우	
    
