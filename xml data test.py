import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 🔗 UTIC XML API URL
xml_url = "https://www.utic.go.kr/guide/imsOpenData.do?key=(키값))"
csv_file = "incident_seoul_bridge_accident.csv"  
refresh_interval = 1800  # 30분마다 갱신

def fetch_and_update():
    try:
        if os.path.exists(csv_file):
            df_existing = pd.read_csv(csv_file, encoding='utf-8-sig')
        else:
            df_existing = pd.DataFrame()

        response = requests.get(xml_url, verify=False)
        response.encoding = 'utf-8'
        xml_data = response.text
        root = ET.fromstring(xml_data)

        new_data = []
        for record in root.findall('record'):
            address = record.findtext('addressJibun')
            title = record.findtext('incidentTitle')

            # ✅ 조건: 주소가 '서울'로 시작 AND incidentTitle에 '대교' 포함 AND '[사고]' 포함
            if address and address.startswith("서울") and title and '대교' in title and '[사고]' in title:
                entry = {
                    'incidentId': record.findtext('incidentId'),
                    'incidentTypeCd': record.findtext('incidenteTypeCd'),
                    'incidentSubTypeCd': record.findtext('incidenteSubTypeCd'),
                    'addressJibun': address,
                    'locationDataX': record.findtext('locationDataX'),
                    'locationDataY': record.findtext('locationDataY'),
                    'incidentTitle': title,
                    'startDate': record.findtext('startDate'),
                    'endDate': record.findtext('endDate'),
                    'lane': record.findtext('lane'),
                    'roadName': record.findtext('roadName'),
                    'updateDate': record.findtext('updateDate'),
                }
                new_data.append(entry)

        df_new = pd.DataFrame(new_data)

        if not df_existing.empty:
            df_combined = pd.concat([df_existing, df_new])
            df_combined.drop_duplicates(subset=['incidentId'], keep='first', inplace=True)
        else:
            df_combined = df_new

        df_combined.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"✅ [{time.strftime('%Y-%m-%d %H:%M:%S')}] '[사고] + 서울 + 대교' 사고 저장 완료: {len(df_combined)}건")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

print("🔄 '[사고] + 서울 + 대교' 사고 자동 갱신 시작 (종료하려면 Ctrl+C)...")
while True:
    fetch_and_update()
    time.sleep(refresh_interval)
