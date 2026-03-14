import csv
from dataset_generation import get_feature_flow

def test_tsv_generation(pcap_file_path, output_tsv_path):
    print(f"[{pcap_file_path}] TSV 데이터 생성 테스트 시작\n")
    
    # main.py에서 사용하는 기본 설정값
    payload_length = 256
    payload_packet = 10 
    dummy_label = 0 # 테스트용 임시 레이블
    
    # 실제 데이터셋 생성 로직 호출
    feature_data = get_feature_flow(pcap_file_path, payload_length, payload_packet)
    print(f"{feature_data}")
    
    if feature_data == -1:
        print("결과: flowcontainer 분석 에러이거나 패킷이 3개 미만이라 제외되었습니다.")
        return
        
    flow_data_string = feature_data[0]
    
    # TSV 파일용 리스트 구성
    dataset_file = [["label", "text_a"]]
    dataset_file.append([dummy_label, flow_data_string])
    
    # 파일 저장
    with open(output_tsv_path, 'w', newline='', encoding='utf-8') as f:
        tsv_w = csv.writer(f, delimiter='\t')
        tsv_w.writerows(dataset_file)
        
    print(f"테스트 완료: {output_tsv_path} 파일이 생성되었습니다.")
    print(f"추출된 text_a의 총 길이: {len(flow_data_string)}")
    print(f"text_a 미리보기: {flow_data_string[:100]}...\n")

if __name__ == "__main__":
    target_pcap = "E:\\pre-data\\fine-tuning-for-tls-version\\captures\\splitcap\\3lift_com\\3lift_com_R1_105826_091044604\\3lift_com_R1_105826_091044604.pcap.TCP_3-171-185-32_443_192-168-0-197_59518.pcap"
    output_tsv = "single_pcap_test.tsv"
    
    # 테스트 실행
    test_tsv_generation(target_pcap, output_tsv)
    
    # 상세 검증 로직
    with open(output_tsv, 'r', encoding='utf-8') as f:
        import csv
        reader = csv.DictReader(f, delimiter='\t')
        row = next(reader)
        text_a = row['text_a']
        
        # 1. SEP 개수 확인 (조기 종료 여부)
        sep_count = text_a.count("[SEP]")
        print(f"--- 상세 검증 결과 ---")
        print(f"[*] 추출된 패킷 수(SEP 개수): {sep_count} / 10")
        
        # 2. 데이터 시작 패턴 확인 (TCP 제거 여부)
        # TCP 헤더가 제거되었다면 첫 바이트는 TLS 레코드 유형(16) 또는 핸드셰이크 유형(01)이어야 함
        first_tokens = text_a.strip().split(' ')[:2]
        print(f"[*] 데이터 시작 토큰: {' '.join(first_tokens)}")

        if sep_count < 10:
            print("[+] 결과: ServerHello 이후 ACK 조건에 의해 조기 종료되었습니다.")
        else:
            print("[-] 결과: 조기 종료 조건에 걸리지 않았습니다.")