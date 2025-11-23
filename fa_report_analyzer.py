"""
FA Report Analyzer - 失效分析報告評估工具
專業的 FA 報告分析系統，使用 AI 進行全面評估
"""

import json
import anthropic
from pathlib import Path
from datetime import datetime
import pandas as pd
from typing import Dict, List, Tuple
import sys

class FAReportAnalyzer:
    """FA 報告分析器"""
    
    def __init__(self, api_key: str = None):
        """初始化分析器
        
        Args:
            api_key: Anthropic API key (如果在 claude.ai 環境中則不需要)
        """
        self.api_key = api_key
        self.client = anthropic.Anthropic(api_key=api_key) if api_key else None
        
        # 評估維度與權重
        self.dimensions = {
            "基本資訊完整性": 15,
            "問題描述與定義": 15,
            "分析方法與流程": 20,
            "數據與證據支持": 20,
            "根因分析": 20,
            "改善對策": 10
        }
        
        # 評分標準
        self.grade_criteria = {
            'A': (90, 100, '卓越報告'),
            'B': (80, 89, '良好報告'),
            'C': (70, 79, '合格報告'),
            'D': (60, 69, '待改進報告'),
            'F': (0, 59, '不合格報告')
        }
    
    def read_report(self, file_path: str) -> str:
        """讀取 FA 報告文件
        
        Args:
            file_path: 報告文件路徑
            
        Returns:
            報告內容文本
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"找不到文件: {file_path}")
        
        # 根據文件類型讀取
        if file_path.suffix.lower() == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_path.suffix.lower() == '.pdf':
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            except ImportError:
                print("警告: 需要安裝 PyPDF2 來讀取 PDF 文件")
                print("請執行: pip install PyPDF2 --break-system-packages")
                sys.exit(1)
        
        elif file_path.suffix.lower() in ['.doc', '.docx']:
            try:
                import docx
                doc = docx.Document(file_path)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                return text
            except ImportError:
                print("警告: 需要安裝 python-docx 來讀取 Word 文件")
                print("請執行: pip install python-docx --break-system-packages")
                sys.exit(1)
        
        else:
            raise ValueError(f"不支援的文件格式: {file_path.suffix}")
    
    def create_analysis_prompt(self, report_content: str) -> str:
        """創建分析提示詞
        
        Args:
            report_content: 報告內容
            
        Returns:
            完整的分析提示詞
        """
        prompt = f"""請分析這份 Failure Analysis Report,並根據以下評估維度進行全面評分:

【評估維度與權重】
1. **基本資訊完整性** (15%)
   - 產品資訊(型號、批號、製造日期)
   - 客戶資訊與投訴內容
   - FA 編號與日期
   - 負責工程師資訊

2. **問題描述與定義** (15%)
   - 失效現象描述的清晰度
   - 失效模式的準確性
   - 問題範圍與影響評估
   - 失效率數據

3. **分析方法與流程** (20%)
   - 分析方法的適當性(如:光學檢查、SEM、FIB、X-ray等)
   - 分析步驟的邏輯性與完整性
   - 實驗設計的合理性
   - 分析設備使用的正確性

4. **數據與證據支持** (20%)
   - 分析數據的充分性
   - 圖片/圖表的清晰度與標註
   - 量化數據的準確性
   - 對照組/比較樣本的使用

5. **根因分析** (20%)
   - 根本原因的深度與準確度
   - 因果關係的邏輯推導
   - 5-Why 或 Fishbone 分析的應用
   - 排除其他可能原因的論證

6. **改善對策** (10%)
   - 短期與長期對策的完整性
   - 對策的可行性與有效性
   - 預防措施的提出
   - 驗證計畫

【評分標準】
- **A級 (90-100分)**:卓越報告
- **B級 (80-89分)**:良好報告
- **C級 (70-79分)**:合格報告
- **D級 (60-69分)**:待改進報告
- **F級 (<60分)**:不合格報告

請以 JSON 格式回傳評估結果,格式如下:

{{
  "total_score": <總分數字>,
  "grade": "<等級字母>",
  "dimension_scores": {{
    "基本資訊完整性": {{"score": <分數>, "percentage": <百分比>, "comment": "<評語>"}},
    "問題描述與定義": {{"score": <分數>, "percentage": <百分比>, "comment": "<評語>"}},
    "分析方法與流程": {{"score": <分數>, "percentage": <百分比>, "comment": "<評語>"}},
    "數據與證據支持": {{"score": <分數>, "percentage": <百分比>, "comment": "<評語>"}},
    "根因分析": {{"score": <分數>, "percentage": <百分比>, "comment": "<評語>"}},
    "改善對策": {{"score": <分數>, "percentage": <百分比>, "comment": "<評語>"}}
  }},
  "strengths": [
    "<具體優點1>",
    "<具體優點2>",
    "<具體優點3>"
  ],
  "improvements": [
    {{"priority": "高", "item": "<待改進項目>", "suggestion": "<具體改善建議>"}},
    {{"priority": "中", "item": "<待改進項目>", "suggestion": "<具體改善建議>"}}
  ],
  "summary": "<總評與建議>"
}}

重要:你的回應必須是純 JSON 格式,不要包含任何其他文字、markdown 標記或程式碼區塊符號。

【FA 報告內容】
{report_content}
"""
        return prompt
    
    def analyze_with_ai(self, report_content: str) -> Dict:
        """使用 AI 分析報告
        
        Args:
            report_content: 報告內容
            
        Returns:
            分析結果字典
        """
        prompt = self.create_analysis_prompt(report_content)
        
        try:
            # 調用 Claude API
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # 解析回應
            response_text = message.content[0].text.strip()
            
            # 移除可能的 markdown 標記
            response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            # 解析 JSON
            result = json.loads(response_text)
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            print(f"回應內容: {response_text[:500]}...")
            raise
        except Exception as e:
            print(f"分析過程發生錯誤: {e}")
            raise
    
    def calculate_grade(self, total_score: float) -> Tuple[str, str]:
        """計算等級
        
        Args:
            total_score: 總分
            
        Returns:
            (等級, 等級描述)
        """
        for grade, (min_score, max_score, description) in self.grade_criteria.items():
            if min_score <= total_score <= max_score:
                return grade, description
        return 'F', '不合格報告'
    
    def generate_report(self, analysis_result: Dict, output_path: str = None) -> str:
        """生成評估報告
        
        Args:
            analysis_result: 分析結果
            output_path: 輸出文件路徑(可選)
            
        Returns:
            報告文本
        """
        total_score = analysis_result['total_score']
        grade = analysis_result['grade']
        grade_desc = [desc for g, (_, _, desc) in self.grade_criteria.items() if g == grade][0]
        
        # 生成報告內容
        report = []
        report.append("=" * 80)
        report.append("FA 報告評估結果")
        report.append("=" * 80)
        report.append(f"\n生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 1. 總分與等級
        report.append("【總分與等級】")
        report.append(f"總分: {total_score:.1f} 分")
        report.append(f"等級: {grade} 級 - {grade_desc}")
        report.append("")
        
        # 2. 各維度評分表
        report.append("【各維度評分表】")
        report.append("-" * 80)
        
        # 創建 DataFrame
        dimension_data = []
        for dim_name, dim_info in analysis_result['dimension_scores'].items():
            dimension_data.append({
                '評估維度': dim_name,
                '權重': f"{self.dimensions[dim_name]}%",
                '得分': f"{dim_info['score']:.1f}",
                '完成度': f"{dim_info['percentage']:.1f}%",
                '評語': dim_info['comment']
            })
        
        df = pd.DataFrame(dimension_data)
        report.append(df.to_string(index=False))
        report.append("")
        
        # 3. 優點分析
        report.append("【優點分析】")
        for i, strength in enumerate(analysis_result['strengths'], 1):
            report.append(f"{i}. {strength}")
        report.append("")
        
        # 4. 待改進項目
        report.append("【待改進項目】(依優先級排序)")
        for i, item in enumerate(analysis_result['improvements'], 1):
            report.append(f"\n{i}. [{item['priority']}優先級] {item['item']}")
            report.append(f"   改善建議: {item['suggestion']}")
        report.append("")
        
        # 5. 總評與建議
        report.append("【總評與建議】")
        report.append(analysis_result['summary'])
        report.append("")
        
        report.append("=" * 80)
        report.append("報告結束")
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        
        # 保存到文件
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"\n✓ 評估報告已保存至: {output_path}")
        
        return report_text
    
    def analyze_report(self, input_file: str, output_file: str = None) -> Dict:
        """完整的報告分析流程
        
        Args:
            input_file: 輸入的 FA 報告文件路徑
            output_file: 輸出的評估報告文件路徑
            
        Returns:
            分析結果字典
        """
        print("=" * 80)
        print("FA 報告分析工具")
        print("=" * 80)
        
        # 1. 讀取報告
        print(f"\n[1/3] 讀取報告文件: {input_file}")
        report_content = self.read_report(input_file)
        print(f"✓ 成功讀取報告 ({len(report_content)} 字元)")
        
        # 2. AI 分析
        print("\n[2/3] 使用 AI 進行深度分析...")
        analysis_result = self.analyze_with_ai(report_content)
        print("✓ 分析完成")
        
        # 3. 生成報告
        print("\n[3/3] 生成評估報告...")
        if not output_file:
            output_file = f"fa_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        report_text = self.generate_report(analysis_result, output_file)
        
        print("\n" + "=" * 80)
        print("分析完成!")
        print("=" * 80)
        
        return analysis_result


def main():
    """主程式"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='FA Report Analyzer - 失效分析報告評估工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例用法:
  # 分析 FA 報告
  python fa_report_analyzer.py -i fa_report.pdf -o evaluation.txt
  
  # 使用 API key (如果需要)
  python fa_report_analyzer.py -i fa_report.pdf -k your_api_key
        """
    )
    
    parser.add_argument('-i', '--input', required=True,
                        help='輸入的 FA 報告文件路徑 (支援 .txt, .pdf, .docx)')
    parser.add_argument('-o', '--output',
                        help='輸出的評估報告文件路徑 (預設: 自動生成)')
    parser.add_argument('-k', '--api-key',
                        help='Anthropic API key (在 claude.ai 環境中不需要)')
    
    args = parser.parse_args()
    
    try:
        # 創建分析器
        analyzer = FAReportAnalyzer(api_key=args.api_key)
        
        # 執行分析
        result = analyzer.analyze_report(args.input, args.output)
        
        # 顯示摘要
        print(f"\n總分: {result['total_score']:.1f} 分")
        print(f"等級: {result['grade']}")
        
    except Exception as e:
        print(f"\n錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
