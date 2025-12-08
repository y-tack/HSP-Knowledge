#!/usr/bin/env python3
"""
HSP-Knowledge 記事編集権限チェックスクリプト

既存記事の編集時に、編集者がその記事に過去にコミットしたことがあるかを確認します。
新規作成の場合は無条件で許可します。

使用方法:
    python check_author_permission.py <file_path> <pr_author> [--base-branch <branch>]

返り値 (JSON):
    - is_new_file: 新規ファイルかどうか
    - is_permitted: 編集が許可されるかどうか
    - pr_author: PRの作成者
    - file_authors: ファイルに過去にコミットしたユーザー一覧
    - reason: 判定理由
"""

import json
import os
import subprocess
import sys
from typing import List, Set


def get_file_authors(file_path: str, base_branch: str = "main") -> Set[str]:
    """
    指定ファイルに対してコミットしたことがあるGitHubユーザー名を取得する
    
    Note: git log の %an はコミット作成者名、%ae はメールアドレス
    GitHub上でのPRマージでは、通常GitHubユーザー名がコミット作成者となる
    """
    try:
        # base_branch上でのファイルのコミット履歴を取得
        # PRブランチではなく、mainブランチの履歴を見る必要がある
        result = subprocess.run(
            [
                "git", "log", 
                f"origin/{base_branch}",
                "--pretty=format:%an",
                "--follow",
                "--", file_path
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            # ファイルが存在しない（新規ファイル）場合もエラーになる
            return set()
        
        # コミット作成者名を取得（重複を除去）
        authors = set()
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                authors.add(line.strip())
        
        return authors
    
    except subprocess.TimeoutExpired:
        print("Warning: git log command timed out", file=sys.stderr)
        return set()
    except Exception as e:
        print(f"Warning: Failed to get file authors: {e}", file=sys.stderr)
        return set()


def is_file_new(file_path: str, base_branch: str = "main") -> bool:
    """
    ファイルがbase_branchに存在しない（新規作成）かどうかを確認
    """
    try:
        result = subprocess.run(
            ["git", "cat-file", "-e", f"origin/{base_branch}:{file_path}"],
            capture_output=True,
            timeout=10
        )
        # 戻り値が0ならファイルが存在する、それ以外なら存在しない
        return result.returncode != 0
    except Exception:
        # エラーの場合は新規ファイルとして扱う（安全側に倒す）
        return True


def check_permission(file_path: str, pr_author: str, base_branch: str = "main") -> dict:
    """
    ファイル編集権限をチェック
    
    ルール:
    - 新規ファイル: 誰でも作成可能
    - 既存ファイル: 過去にそのファイルにコミットしたことがあるユーザーのみ編集可能
    """
    result = {
        "file_path": file_path,
        "is_new_file": False,
        "is_permitted": False,
        "pr_author": pr_author,
        "file_authors": [],
        "reason": ""
    }
    
    # 新規ファイルかどうか確認
    if is_file_new(file_path, base_branch):
        result["is_new_file"] = True
        result["is_permitted"] = True
        result["reason"] = "新規ファイルの作成は誰でも可能です"
        return result
    
    # 既存ファイルの場合、過去のコミット者を取得
    file_authors = get_file_authors(file_path, base_branch)
    result["file_authors"] = sorted(list(file_authors))
    
    if not file_authors:
        # コミット履歴が取得できない場合は許可（初期状態やエラー）
        result["is_permitted"] = True
        result["reason"] = "コミット履歴が取得できませんでした（初期状態の可能性）"
        return result
    
    # PR作成者が過去のコミット者に含まれるか確認
    if pr_author in file_authors:
        result["is_permitted"] = True
        result["reason"] = f"PR作成者 '{pr_author}' はこの記事の過去の編集者です"
    else:
        result["is_permitted"] = False
        result["reason"] = (
            f"PR作成者 '{pr_author}' はこの記事を編集する権限がありません。"
            f"この記事は {', '.join(sorted(file_authors))} によって作成されました。"
        )
    
    return result


def main():
    """メイン処理"""
    import argparse
    
    parser = argparse.ArgumentParser(description="記事編集権限をチェック")
    parser.add_argument("file_path", help="チェック対象のファイルパス")
    parser.add_argument("pr_author", help="PRの作成者（GitHubユーザー名）")
    parser.add_argument("--base-branch", default="main", help="ベースブランチ名（デフォルト: main）")
    
    args = parser.parse_args()
    
    result = check_permission(args.file_path, args.pr_author, args.base_branch)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 終了コード: 許可されていれば0、そうでなければ1
    sys.exit(0 if result["is_permitted"] else 1)


if __name__ == "__main__":
    main()
