import csv
import datetime
import os

def load_barcode_data(csv_file_path):
    """
    从 CSV 文件中加载条形码id数据。
    """
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return {row['ID']: row['Name'] for row in reader}

def load_scanned_ids(scanned_file_path):
    """
    从之前的扫描结果文件中加载已扫描的 ID。
    """
    with open(scanned_file_path, mode='r') as file:
        reader = csv.reader(file)
        return set(row[0] for row in reader if row)

def save_scanned_ids(scanned_ids, output_dir):
    """
    保存当前扫描会话的结果。
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    scanned_file_path = os.path.join(output_dir, f"scanned_{timestamp}.csv")
    with open(scanned_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for id in scanned_ids:
            writer.writerow([id])

def list_scanned_files(output_dir):
    """
    列出所有的扫描结果文件。
    """
    files = os.listdir(output_dir)
    return [file for file in files if file.startswith("scanned_") and file.endswith(".csv")]

def scan_barcode(barcode_data, scanned_ids):
    """
    扫描条形码并更新扫描结果。
    """
    try:
        while True:
            barcode_input = input("扫描条形码，输入 'report'或 'r' 查看未扫描名单，输入 'exit' 结束: ")
            if barcode_input.lower() == 'exit'or barcode_input.lower() == 'quit':
                break
            elif barcode_input.lower() == 'report' or barcode_input.lower() == 'r':
                unscanned_names = [name for id, name in barcode_data.items() if id not in scanned_ids]
                print("未扫描的人员名单:")
                print("\n".join(unscanned_names) if unscanned_names else "所有人都已扫描。")
                continue

            if barcode_input in barcode_data:
                if barcode_input in scanned_ids:
                    print("该条形码已扫描。")
                else:
                    print(f"{barcode_data[barcode_input]} 扫描成功。")
                    scanned_ids.add(barcode_input)
            else:
                print("无效的条形码。")
    except KeyboardInterrupt:
        print("扫描中断。")
    finally:
        return scanned_ids

def main_menu():
    """
    显示主菜单并获取用户选择。
    """
    print("1. 开始新的扫描会话")
    print("2. 继续之前的扫描会话")
    choice = input("请输入你的选择：").strip()
    return choice

def main():
    output_dir = 'results'
    os.makedirs(output_dir, exist_ok=True)

    # choice = main_menu()
    choice = '2'
    if choice == '2':
        files = list_scanned_files(output_dir)
        if files:
            print("可用的扫描结果文件：")
            for i, file in enumerate(files, 1):
                print(f"{i}. {file}")
            
            file_choice = input("选择文件编号以继续，或直接回车开始新会话: ").strip()
            if file_choice.isdigit() and 1 <= int(file_choice) <= len(files):
                scanned_file_path = os.path.join(output_dir, files[int(file_choice) - 1])
                scanned_ids = load_scanned_ids(scanned_file_path)
            else:
                scanned_ids = set()
        else:
            print("没有找到旧的扫描结果，将开始新会话。")
            scanned_ids = set()
    else:
        scanned_ids = set()

    csv_file_path = 'barcodes/barcode_data.csv'
    barcode_data = load_barcode_data(csv_file_path)
    scanned_ids = scan_barcode(barcode_data, scanned_ids)
    save_scanned_ids(scanned_ids, output_dir)

if __name__ == "__main__":
    main()
