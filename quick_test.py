"""
快速測試腳本
用於驗證 FA Report Analyzer 是否正確安裝和運行
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """檢查 Python 版本"""
    print("[1/5] 檢查 Python 版本...")
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("⚠ 警告: 建議使用 Python 3.8 或更高版本")
        return False
    return True

def check_dependencies():
    """檢查必要的依賴套件"""
    print("\n[2/5] 檢查依賴套件...")
    
    required_packages = {
        'anthropic': '必要',
        'pandas': '必要',
        'PyPDF2': '選用 (PDF支援)',
        'docx': '選用 (Word支援)'
    }
    
    results = {}
    for package, package_type in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {package} - 已安裝 ({package_type})")
            results[package] = True
        except ImportError:
            print(f"✗ {package} - 未安裝 ({package_type})")
            results[package] = False
    
    return results

def install_missing_packages(missing_packages):
    """安裝缺少的套件"""
    print("\n[3/5] 安裝缺少的套件...")
    
    # 必要套件
    required = []
    if not missing_packages.get('anthropic'):
        required.append('anthropic')
    if not missing_packages.get('pandas'):
        required.append('pandas')
    
    if required:
        print(f"安裝必要套件: {', '.join(required)}")
        cmd = [sys.executable, '-m', 'pip', 'install'] + required + ['--break-system-packages']
        subprocess.run(cmd)
    
    # 選用套件
    optional = []
    if not missing_packages.get('PyPDF2'):
        response = input("\n是否安裝 PDF 支援 (PyPDF2)? (y/n): ")
        if response.lower() == 'y':
            optional.append('PyPDF2')
    
    if not missing_packages.get('docx'):
        response = input("是否安裝 Word 支援 (python-docx)? (y/n): ")
        if response.lower() == 'y':
            optional.append('python-docx')
    
    if optional:
        print(f"安裝選用套件: {', '.join(optional)}")
        cmd = [sys.executable, '-m', 'pip', 'install'] + optional + ['--break-system-packages']
        subprocess.run(cmd)

def check_files():
    """檢查必要的檔案"""
    print("\n[4/5] 檢查檔案...")
    
    required_files = [
        'fa_report_analyzer.py',
        'sample_fa_report.txt'
    ]
    
    all_exist = True
    for filename in required_files:
        if Path(filename).exists():
            print(f"✓ {filename}")
        else:
            print(f"✗ {filename} - 找不到")
            all_exist = False
    
    return all_exist

def run_test():
    """執行測試"""
    print("\n[5/5] 執行測試分析...")
    
    try:
        # 導入模組測試
        from fa_report_analyzer import FAReportAnalyzer
        print("✓ 模組導入成功")
        
        # 測試分析器創建
        analyzer = FAReportAnalyzer()
        print("✓ 分析器創建成功")
        
        # 測試讀取報告
        if Path('sample_fa_report.txt').exists():
            content = analyzer.read_report('sample_fa_report.txt')
            print(f"✓ 報告讀取成功 ({len(content)} 字元)")
            
            # 詢問是否執行完整分析
            response = input("\n是否執行完整 AI 分析? (需要 API key 或在 claude.ai 環境中) (y/n): ")
            if response.lower() == 'y':
                print("\n開始完整分析...")
                result = analyzer.analyze_report('sample_fa_report.txt')
                print(f"\n✓ 分析完成!")
                print(f"  總分: {result['total_score']:.1f}")
                print(f"  等級: {result['grade']}")
        else:
            print("⚠ 找不到範例報告,跳過讀取測試")
        
        return True
        
    except Exception as e:
        print(f"✗ 測試失敗: {e}")
        return False

def main():
    """主程式"""
    print("=" * 60)
    print("FA Report Analyzer - 快速測試")
    print("=" * 60)
    print()
    
    # 1. 檢查 Python 版本
    if not check_python_version():
        sys.exit(1)
    
    # 2. 檢查依賴
    dependencies = check_dependencies()
    
    # 3. 安裝缺少的套件
    if not all([dependencies['anthropic'], dependencies['pandas']]):
        response = input("\n發現缺少必要套件,是否自動安裝? (y/n): ")
        if response.lower() == 'y':
            install_missing_packages(dependencies)
        else:
            print("\n請手動安裝必要套件:")
            print("  pip install anthropic pandas --break-system-packages")
            sys.exit(1)
    
    # 4. 檢查檔案
    if not check_files():
        print("\n⚠ 部分檔案缺失,請確保所有檔案都在正確位置")
        sys.exit(1)
    
    # 5. 執行測試
    if run_test():
        print("\n" + "=" * 60)
        print("✓ 所有測試通過!")
        print("=" * 60)
        print("\n使用方法:")
        print("  python fa_report_analyzer.py -i your_report.txt")
        print("\n查看完整文檔:")
        print("  cat README.md")
    else:
        print("\n" + "=" * 60)
        print("✗ 測試失敗")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
