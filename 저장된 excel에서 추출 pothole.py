import pandas as pd

# 🔹 원본 엑셀 파일 열기
input_file = "서울돌발데이터(250225~250321).xlsx"  # ← 파일명 변경 가능

# 🔹 데이터 불러오기
df = pd.read_excel(input_file)

# 🔍 필터 조건: INCIDENT_TITLE에 '<사고>' 포함, 그리고 '포트홀' 포함
filtered_df = df[
    df['INCIDENT_TITLE'].str.contains(r'<사고>', regex=True) &
    df['INCIDENT_TITLE'].str.contains('포트홀')
]

# 💾 필터링된 결과를 엑셀 파일로 저장
output_file = "pothole_onemonth.xlsx"
filtered_df.to_excel(output_file, index=False)

print(f"✅ 저장 완료! 총 {len(filtered_df)}건이 '{output_file}'에 저장되었습니다.")
