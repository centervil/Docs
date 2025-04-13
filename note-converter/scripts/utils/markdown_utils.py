#!/usr/bin/env python3
"""
マークダウン処理のユーティリティモジュール

マークダウンの解析、変換、整形などの機能を提供します。
"""
import re
import logging

# ロギング設定
logger = logging.getLogger(__name__)


def parse_markdown(markdown_text):
    """
    マークダウンテキストを解析して構造化データに変換します
    
    Args:
        markdown_text (str): 入力マークダウンテキスト
        
    Returns:
        dict: 以下のキーを持つ辞書
            - headers: 見出し情報のリスト
            - lists: リスト情報のリスト
            - code_blocks: コードブロック情報のリスト
            - paragraphs: 段落テキストのリスト
    """
    logger.info("マークダウンの解析を開始")
    
    # 構造化データを格納する辞書
    result = {
        "headers": [],
        "lists": [],
        "code_blocks": [],
        "paragraphs": []
    }
    
    # 各要素の抽出
    result["headers"] = extract_headers(markdown_text)
    result["lists"] = extract_lists(markdown_text)
    result["code_blocks"] = extract_code_blocks(markdown_text)
    
    # 段落の抽出（コードブロックと見出しを除外）
    paragraphs = []
    lines = markdown_text.split('\n')
    current_paragraph = []
    in_code_block = False
    
    for line in lines:
        # コードブロック内の場合はスキップ
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        
        if in_code_block:
            continue
            
        # 見出し行はスキップ
        if re.match(r'^#{1,6}\s+', line.strip()):
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
            continue
            
        # リスト項目はスキップ
        if re.match(r'^\s*[-*+]\s+', line.strip()):
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
            continue
            
        # 空行は段落の区切り
        if not line.strip():
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
            continue
            
        # それ以外は段落として追加
        current_paragraph.append(line.strip())
    
    # 最後の段落があれば追加
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))
        
    result["paragraphs"] = paragraphs
    
    logger.info(f"マークダウン解析完了: {len(result['headers'])}件の見出し、{len(result['lists'])}件のリスト、{len(result['code_blocks'])}件のコードブロック、{len(result['paragraphs'])}件の段落を検出")
    return result


def extract_headers(markdown_text):
    """
    マークダウンから見出し要素を抽出します
    
    Args:
        markdown_text (str): 入力マークダウンテキスト
        
    Returns:
        list: 見出し情報の辞書リスト。各辞書は以下のキーを持ちます:
            - level: 見出しレベル (1-6)
            - text: 見出しテキスト
            - index: マークダウン内での位置（行番号）
    """
    headers = []
    pattern = r'^(#{1,6})\s+(.+)$'
    
    for i, line in enumerate(markdown_text.split('\n')):
        match = re.match(pattern, line.strip())
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headers.append({
                "level": level,
                "text": text,
                "index": i
            })
    
    return headers


def extract_lists(markdown_text):
    """
    マークダウンからリスト要素を抽出します
    
    Args:
        markdown_text (str): 入力マークダウンテキスト
        
    Returns:
        list: リスト情報の辞書リスト。各辞書は以下のキーを持ちます:
            - items: リスト項目の辞書リスト
                - text: 項目テキスト
                - level: インデントレベル
                - index: マークダウン内での位置（行番号）
            - nested_items: ネストされたリスト項目の辞書リスト
                - text: 項目テキスト
                - level: インデントレベル (2以上)
                - parent_index: 親項目のインデックス
                - index: マークダウン内での位置（行番号）
    """
    lists = []
    current_list = {
        "items": [],
        "nested_items": []
    }
    in_list = False
    list_pattern = r'^(\s*)[-*+]\s+(.+)$'
    
    lines = markdown_text.split('\n')
    for i, line in enumerate(lines):
        match = re.match(list_pattern, line)
        if match:
            indent = len(match.group(1))
            text = match.group(2).strip()
            level = (indent // 2) + 1  # インデントから階層レベルを計算
            
            if not in_list:
                in_list = True
                current_list = {
                    "items": [],
                    "nested_items": []
                }
            
            # 最上位リストか、ネストされたリストか判断
            if level == 1:
                current_list["items"].append({
                    "text": text,
                    "level": level,
                    "index": i
                })
            else:
                # 親項目のインデックスを特定（直近の上位レベル項目）
                parent_index = None
                for j in range(len(current_list["items"]) - 1, -1, -1):
                    if current_list["items"][j]["level"] < level:
                        parent_index = j
                        break
                
                current_list["nested_items"].append({
                    "text": text,
                    "level": level,
                    "parent_index": parent_index,
                    "index": i
                })
        else:
            # リスト以外の要素が登場したらリスト終了
            if in_list and not line.strip():
                continue  # 空行はまだリストの一部と見なす
                
            if in_list and len(current_list["items"]) > 0:
                lists.append(current_list)
                in_list = False
    
    # 最後のリストがあれば追加
    if in_list and len(current_list["items"]) > 0:
        lists.append(current_list)
    
    return lists


def extract_code_blocks(markdown_text):
    """
    マークダウンからコードブロックを抽出します
    
    Args:
        markdown_text (str): 入力マークダウンテキスト
        
    Returns:
        list: コードブロック情報の辞書リスト。各辞書は以下のキーを持ちます:
            - language: 言語指定（ない場合は空文字列）
            - code: コードブロックの内容
            - start_index: 開始行番号
            - end_index: 終了行番号
    """
    code_blocks = []
    lines = markdown_text.split('\n')
    in_code_block = False
    current_block = {
        "language": "",
        "code": [],
        "start_index": 0,
        "end_index": 0
    }
    
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            if not in_code_block:
                # コードブロック開始
                in_code_block = True
                language = line.strip()[3:].strip()  # ```の後の言語指定
                current_block = {
                    "language": language,
                    "code": [],
                    "start_index": i
                }
            else:
                # コードブロック終了
                in_code_block = False
                current_block["end_index"] = i
                code_blocks.append(current_block)
        elif in_code_block:
            # コードブロック内の行を追加
            current_block["code"].append(line)
    
    # コードブロックの内容を文字列に変換
    for block in code_blocks:
        block["code"] = '\n'.join(block["code"])
    
    return code_blocks


def format_markdown_for_note(markdown_text):
    """
    マークダウンをnote.com向けに最適化します
    
    Args:
        markdown_text (str): 入力マークダウンテキスト
        
    Returns:
        str: note.com向けに最適化されたマークダウンテキスト
    """
    # クリーンアップ処理
    cleaned_markdown = clean_markdown(markdown_text)
    
    # note.com向けの変換
    # 1. 見出し前の空行を確保
    pattern_heading = r'(^|\n)(#{1,6}\s+.+)'
    replacement_heading = r'\1\n\2'
    result = re.sub(pattern_heading, replacement_heading, cleaned_markdown)
    
    # 2. リスト項目のインデント調整
    pattern_list = r'(\n\s*[-*+]\s+.+)'
    replacement_list = r'\1'
    result = re.sub(pattern_list, replacement_list, result)
    
    # 3. 全体のフォーマット調整
    result = re.sub(r'\n{3,}', '\n\n', result)  # 3つ以上連続する改行を2つに
    
    # 4. コードブロックの前後に空行を追加
    pattern_code_block = r'(^|\n)(```.*)'
    replacement_code_block = r'\1\n\2'
    result = re.sub(pattern_code_block, replacement_code_block, result)
    
    return result.strip()


def clean_markdown(markdown_text):
    """
    マークダウンの不要な空白行や余分な空白を整理します
    
    Args:
        markdown_text (str): 入力マークダウンテキスト
        
    Returns:
        str: 整理されたマークダウンテキスト
    """
    # コードブロックを一時的に退避
    code_blocks = []
    code_block_pattern = r'```(.*?)\n(.*?)```'
    
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"CODE_BLOCK_PLACEHOLDER_{len(code_blocks) - 1}"
    
    # コードブロックを退避
    text = re.sub(code_block_pattern, save_code_block, markdown_text, flags=re.DOTALL)
    
    # 1. 行頭と行末の余分な空白を削除
    lines = []
    for line in text.split('\n'):
        lines.append(line.strip())
    
    # 2. 連続する空行を1つにまとめる
    result_lines = []
    prev_empty = False
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 空行の処理
        if not line:
            if not prev_empty:
                result_lines.append('')
                prev_empty = True
        else:
            # 見出し行の処理
            if line.startswith('#'):
                if result_lines and result_lines[-1] != '':
                    result_lines.append('')
                result_lines.append(line)
                prev_empty = False
            # リスト項目の処理
            elif line.startswith('-') or line.startswith('*') or line.startswith('+'):
                # 次の行もリスト項目かチェック
                if i + 1 < len(lines) and (lines[i + 1].startswith('-') or lines[i + 1].startswith('*') or lines[i + 1].startswith('+')):
                    # 連続するリスト項目の場合
                    if result_lines and not result_lines[-1].startswith('-') and not result_lines[-1].startswith('*') and not result_lines[-1].startswith('+'):
                        if result_lines[-1] != '':
                            result_lines.append('')
                    result_lines.append(line)
                    prev_empty = False
                else:
                    # 単独のリスト項目の場合
                    if not prev_empty and result_lines:
                        result_lines.append('')
                    result_lines.append(line)
                    prev_empty = False
            else:
                # 通常のテキスト行
                result_lines.append(line)
                prev_empty = False
        i += 1
    
    # 3. リスト項目を連続させる
    i = 0
    while i < len(result_lines) - 1:
        if (result_lines[i].startswith('-') or result_lines[i].startswith('*') or result_lines[i].startswith('+')) and result_lines[i+1] == '':
            # リスト項目の後の空行を確認
            if i + 2 < len(result_lines) and (result_lines[i+2].startswith('-') or result_lines[i+2].startswith('*') or result_lines[i+2].startswith('+')):
                # 次のリスト項目の前の空行を削除
                result_lines.pop(i+1)
                continue
        i += 1
    
    # 4. 末尾の改行を削除
    while result_lines and not result_lines[-1]:
        result_lines.pop()
    
    # 結果を文字列に戻す
    text = '\n'.join(result_lines)
    
    # 5. コードブロックを復元
    for i, code_block in enumerate(code_blocks):
        text = text.replace(f"CODE_BLOCK_PLACEHOLDER_{i}", code_block)
    
    return text 