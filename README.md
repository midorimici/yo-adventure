## Yo Adventure

おばけの「よーちゃん」がゴール（オレンジ色のマーク）を目指すゲームです。:ghost:

## 起動

Python 3.8.3 / Windows 64 bit で動作を確認しています。

Python が使える環境で、`python main.py`とコマンド入力すれば起動します。

## 操作方法

- `J` : 左←へ移動
- `L` : 右→へ移動
- `K` : ジャンプ↑
- `shift + R` : ステージをリセット
- `shift + N` : 次のステージへ

途中から始めたい場合は、`main.py`の冒頭にある記述を変更します。

例えば Stage 10 から始めたい場合は次のようにします。

```
from stages import Stage1   # -> ... import Stage10

# ステージ
stage = Stage1()            # -> ... = Stage10()
```

## その他

イラスト素材は[いらすとや](https://www.irasutoya.com/)の[いろいろなハロウィンのマーク](https://www.irasutoya.com/2018/10/blog-post_804.html)より。
