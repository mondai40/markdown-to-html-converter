# マークダウンを HTML に変換するプログラムを作成
# シェルを通して python3 file-converter.py markdown inputfile outputfile というコマンドを実行させる。
# ここで、markdown は実行するコマンド、inputfile は .md ファイルへのパス、出力パスはプログラムを実行した後に作成される .html です。


import sys
import os
import markdown
from pymdownx import emoji

def validate_args(mode, args):
    # """コマンド別の引数数チェック"""
    required_args = {
        "markdown": 4    # mode, input, output  
    }
    
    if len(args) < required_args[mode]:
        raise ValueError(f"{mode}コマンドには{required_args[mode]-1}個の引数が必要です。")

def validate_output_path(output_path):
    # """出力ファイルのバリデーション"""
    if os.path.exists(output_path):
        try:
            response = input(f"ファイル '{output_path}' は既に存在します。上書きしますか？ (y/n): ")
            if response.lower() != 'y':
                raise ValueError("処理がキャンセルされました。")
        except (KeyboardInterrupt, EOFError):
            raise ValueError("処理がキャンセルされました。")

def markdown_to_html(input_path, args):
    # """ファイルをコピー"""
    validate_args("markdown", args)
    output_path = args[3]
    
    try:
        validate_output_path(output_path)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        html = markdown.markdown(
            content, 
            extensions=['tables', 'fenced_code','pymdownx.emoji'],
            extension_configs={
                'pymdownx.emoji': {
                    'emoji_index': emoji.gemoji,
                    'emoji_generator': emoji.to_svg
                }
            }
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
    except FileNotFoundError:
        raise ValueError(f"入力ファイルが見つかりません: {input_path}")
    except PermissionError:
        raise ValueError(f"ファイルの読み取り/書き込み権限がありません")
    except Exception as e:
        raise ValueError(f"ファイル処理エラー: {e}")


SUPPORTED_MODES = ["markdown"]
FUNCTIONS = {
    "markdown": markdown_to_html,
}

def show_usage():
    # """使用方法を表示"""
    print("使用方法:")
    print("  python3 markdown_to_html_converter.py markdown <inputpath> <outputpath>")

def validate_basic_args(args):
    # """基本的な引数チェック"""
    if len(args) < 2:
        raise ValueError("モードが指定されていません。")
    
    mode = args[1]
    if mode not in SUPPORTED_MODES:
        raise ValueError(f"指定されたモード '{mode}' は存在しません。\n対応モード: {', '.join(SUPPORTED_MODES)}")
    
    if len(args) < 3:
        raise ValueError("入力ファイルが指定されていません。")
    
    input_path = args[2]
    if not os.path.isfile(input_path):
        raise ValueError(f"指定されたファイル '{input_path}' は存在しません。")
    
    return mode, input_path

def main():
    try:
        args = sys.argv

        # ヘルプ表示
        if len(args) == 1 or (len(args) == 2 and args[1] in ['-h', '--help', 'help']):
            show_usage()
            return

        # 基本的な引数チェック
        mode, input_path = validate_basic_args(args)
        
        # 対応する関数を実行
        FUNCTIONS[mode](input_path, args)

        print("処理が完了しました。")

    except KeyboardInterrupt:
        print("\n処理が中断されました。")
    except ValueError as e:
        print(f"エラー: {e}")
        print()
        show_usage()
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
    finally:
        print("処理を終了します。")

if __name__ == "__main__":
    main()