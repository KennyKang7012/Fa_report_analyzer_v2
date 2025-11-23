"""
FA Report Analyzer - 使用範例
展示如何在程式中使用 FA 報告分析器
"""

from fa_report_analyzer import FAReportAnalyzer
from pathlib import Path
import json

def example_1_basic_usage():
    """範例 1: 基本使用"""
    print("=" * 70)
    print("範例 1: 基本使用 - 分析單一報告")
    print("=" * 70)
    
    # 創建分析器 (在 claude.ai 環境中不需要 api_key)
    analyzer = FAReportAnalyzer()
    
    # 分析報告
    result = analyzer.analyze_report(
        input_file='sample_fa_report.txt',
        output_file='evaluation_example1.txt'
    )
    
    # 顯示結果
    print(f"\n總分: {result['total_score']:.1f}")
    print(f"等級: {result['grade']}")
    print(f"\n優點:")
    for strength in result['strengths'][:3]:
        print(f"  • {strength}")
    
    print("\n" + "=" * 70 + "\n")

def example_2_batch_analysis():
    """範例 2: 批次分析多份報告"""
    print("=" * 70)
    print("範例 2: 批次分析 - 分析多份報告")
    print("=" * 70)
    
    # 假設有多份報告
    report_files = [
        'sample_fa_report.txt',
        # 'report2.txt',
        # 'report3.pdf',
    ]
    
    analyzer = FAReportAnalyzer()
    results = []
    
    for i, report_file in enumerate(report_files, 1):
        if not Path(report_file).exists():
            print(f"跳過不存在的文件: {report_file}")
            continue
            
        print(f"\n[{i}/{len(report_files)}] 分析 {report_file}...")
        
        try:
            result = analyzer.analyze_report(
                input_file=report_file,
                output_file=f'batch_evaluation_{i}.txt'
            )
            results.append({
                'file': report_file,
                'score': result['total_score'],
                'grade': result['grade']
            })
            print(f"  ✓ 完成 - 分數: {result['total_score']:.1f}, 等級: {result['grade']}")
        except Exception as e:
            print(f"  ✗ 錯誤: {e}")
    
    # 顯示統計
    if results:
        print("\n批次分析統計:")
        print(f"  總報告數: {len(results)}")
        print(f"  平均分數: {sum(r['score'] for r in results) / len(results):.1f}")
        print(f"  最高分數: {max(r['score'] for r in results):.1f}")
        print(f"  最低分數: {min(r['score'] for r in results):.1f}")
    
    print("\n" + "=" * 70 + "\n")

def example_3_custom_analysis():
    """範例 3: 自訂分析 - 只讀取特定維度"""
    print("=" * 70)
    print("範例 3: 自訂分析 - 查看各維度詳細評分")
    print("=" * 70)
    
    analyzer = FAReportAnalyzer()
    
    # 分析報告
    result = analyzer.analyze_report(
        input_file='sample_fa_report.txt',
        output_file=None  # 不保存文件
    )
    
    # 顯示各維度詳細資訊
    print("\n各維度詳細評分:")
    print("-" * 70)
    
    for dim_name, dim_info in result['dimension_scores'].items():
        print(f"\n【{dim_name}】")
        print(f"  權重: {analyzer.dimensions[dim_name]}%")
        print(f"  得分: {dim_info['score']:.1f} / {analyzer.dimensions[dim_name]}")
        print(f"  完成度: {dim_info['percentage']:.1f}%")
        print(f"  評語: {dim_info['comment']}")
    
    print("\n" + "=" * 70 + "\n")

def example_4_export_json():
    """範例 4: 匯出 JSON 格式結果"""
    print("=" * 70)
    print("範例 4: 匯出結果為 JSON 格式")
    print("=" * 70)
    
    analyzer = FAReportAnalyzer()
    
    # 分析報告
    result = analyzer.analyze_report(
        input_file='sample_fa_report.txt',
        output_file='evaluation_example4.txt'
    )
    
    # 匯出為 JSON
    json_file = 'evaluation_result.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 結果已匯出為 JSON: {json_file}")
    print("\nJSON 內容預覽:")
    print("-" * 70)
    print(json.dumps(result, ensure_ascii=False, indent=2)[:500] + "...")
    
    print("\n" + "=" * 70 + "\n")

def example_5_reading_files():
    """範例 5: 讀取不同格式的文件"""
    print("=" * 70)
    print("範例 5: 讀取不同格式的報告文件")
    print("=" * 70)
    
    analyzer = FAReportAnalyzer()
    
    # 支援的文件類型
    test_files = [
        ('sample_fa_report.txt', 'TXT 文字檔'),
        # ('fa_report.pdf', 'PDF 文件'),
        # ('fa_report.docx', 'Word 文件'),
    ]
    
    for file_path, file_type in test_files:
        if not Path(file_path).exists():
            print(f"\n⚠ {file_type}: {file_path} - 文件不存在,跳過")
            continue
        
        try:
            print(f"\n讀取 {file_type}: {file_path}")
            content = analyzer.read_report(file_path)
            print(f"  ✓ 成功讀取")
            print(f"  文件大小: {len(content)} 字元")
            print(f"  預覽: {content[:100]}...")
        except Exception as e:
            print(f"  ✗ 讀取失敗: {e}")
    
    print("\n" + "=" * 70 + "\n")

def main():
    """主程式"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "FA Report Analyzer - 使用範例" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    examples = [
        ("基本使用", example_1_basic_usage),
        ("批次分析", example_2_batch_analysis),
        ("自訂分析", example_3_custom_analysis),
        ("匯出 JSON", example_4_export_json),
        ("讀取文件", example_5_reading_files),
    ]
    
    print("可用的範例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print("  0. 執行所有範例")
    print()
    
    choice = input("請選擇要執行的範例 (0-5): ")
    
    try:
        choice = int(choice)
        if choice == 0:
            # 執行所有範例
            for name, func in examples:
                try:
                    func()
                except Exception as e:
                    print(f"✗ 範例執行失敗: {e}\n")
        elif 1 <= choice <= len(examples):
            # 執行選定的範例
            examples[choice - 1][1]()
        else:
            print("無效的選擇")
    except ValueError:
        print("請輸入有效的數字")
    except Exception as e:
        print(f"執行過程發生錯誤: {e}")
    
    print("\n完成!")

if __name__ == "__main__":
    main()
