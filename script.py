import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
# 클래스 정의
class Major:
    def __init__(self, title, semititle, job, loc):
        self.title = title  # 기업명
        self.semititle = semititle  # 공채 제목
        self.job = job  # 직무
        self.loc = loc  # 세부사항(위치 등)
    def show_title(self):
        print(f"{self.title} - {self.semititle} / 직무 : {self.job} / 위치 : {self.loc}")
    def job_csv(self):
        return [self.title, self.semititle, self.job, self.loc]
# 웹 크롤링 함수
def crawl_data(driver):
    sleep(2)  # 페이지 로딩 시간 기다리기
    title_list = driver.find_elements(By.CSS_SELECTOR, "a.coLink b")  # 기업명
    semititle_list = driver.find_elements(By.CSS_SELECTOR, "a.link")  # 공채 제목
    job_list = driver.find_elements(By.CLASS_NAME, "sTit")  # 직무
    loc_list = driver.find_elements(By.CLASS_NAME, "sDsc")  # 세부 직무(위치 등)
    data_list = []
    for title, semititle, job, loc in zip(title_list, semititle_list, job_list, loc_list):
        major = Major(title.text, semititle.text, job.text, loc.text)
        data_list.append(major)
        major.show_title()  # 데이터 출력
    return data_list
# CSV 저장 함수
def save_to_csv(data_list, filename="job_data.csv"):
    with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["기업명", "공채 제목", "직무", "세부사항"])  # 헤더
        for major in data_list:
            writer.writerow(major.job_csv())  # 데이터 저장
    print(f"CSV 파일 '{filename}' 저장 완료!")
# 자동 실행 처리
def main():
    # Chrome 웹 드라이버 열기
    driver = webdriver.Chrome()
    # 웹페이지 열기
    driver.get("https://www.jobkorea.co.kr/Top100/?Main_Career_Type=1&Search_Type=2&BizJobtype_Bctgr_Code=0&BizJobtype_Bctgr_Name=%EC%A0%84%EC%B2%B4&BizJobtype_Code=0&BizJobtype_Name=%EC%A0%84%EC%B2%B4&Major_Big_Code=5&Major_Big_Name=%EA%B3%B5%ED%95%99&Edu_Level_Code=9&Edu_Level_Name=%EC%A0%84%EC%B2%B4&Edu_Level_Name=%EC%A0%84%EC%B2%B4&MidScroll=0&duty-depth1=on")
    # "공학 전체"부터 "S-50"까지 순차적으로 클릭
    for i in range(1, 10):  # S-1부터 S-50까지 반복
        # "공학 전체" 클래스가 "S-1"부터 "S-50"까지 차례대로 클릭
        element = driver.find_element(By.CSS_SELECTOR, f"label[for='lbl-duty-depth2-S-{i}']")
        ActionChains(driver).move_to_element(element).click().perform()
        sleep(2)  # 클릭 후 페이지 로딩 시간 기다리기
        # 데이터 크롤링
        data_list = crawl_data(driver)
        # CSV 파일명 설정
        filename = f"job_data_S_{i}.csv"
        save_to_csv(data_list, filename)
    # 웹 드라이버 종료
    driver.quit()
# 실행
if __name__ == "__main__":
    main()
