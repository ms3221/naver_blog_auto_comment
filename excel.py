import os, openpyxl, time
import pandas as pd

current_directory = os.path.dirname(os.path.abspath(__file__))


def get_absolute_path(file_path):
    return os.path.join(current_directory, file_path)


excel_filename = get_absolute_path("excel/export.xlsx")


def excel_export(data):
    # 새로운 Excel 워크북 생성
    workbook = openpyxl.Workbook()

    # 현재 활성화된 시트 선택
    sheet = workbook.active

    # 이차원 배열 데이터를 시트에 추가
    for row in data:
        sheet.append(row)

    # Excel 파일 저장

    workbook.save(excel_filename)
    print(f"Excel 파일이 생성되었습니다: {excel_filename}")
    return excel_filename


def update_xlsx_row(excel_path, row_index, row_data):
    # close_specific_excel_workbook("live.xlsx")
    workbook = openpyxl.load_workbook(excel_path)
    sheet = workbook.active
    for col, el in enumerate(row_data, start=1):
        sheet.cell(row=row_index, column=col, value=el)
    workbook.save(excel_path)
    print(f"{row_index}행 업데이트 완료")
    workbook.close()


def excel_read(file_path):
    # 엑셀 파일 읽기
    df = pd.read_excel(file_path, sheet_name=0, na_values="")

    # 데이터프레임을 리스트로 변환
    all_data = df.fillna("").values.tolist()

    # 결과 출력
    return all_data
