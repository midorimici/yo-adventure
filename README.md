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

効果音素材は[On-Jin ～音人～](https://on-jin.com)の[効果音 かわいく跳ねる・ジャンプ03](https://on-jin.com/sound/listshow.php?pagename=ta&title=%E3%81%8B%E3%82%8F%E3%81%84%E3%81%8F%E8%B7%B3%E3%81%AD%E3%82%8B%E3%83%BB%E3%82%B8%E3%83%A3%E3%83%B3%E3%83%9703&janl=%E3%81%9D%E3%81%AE%E4%BB%96%E9%9F%B3&bunr=%E8%B7%B3%E3%81%AD%E3%82%8B&kate=%E6%93%AC%E9%9F%B3%E3%83%BB%E3%82%AA%E3%83%8E%E3%83%9E%E3%83%88%E3%83%9A)と、[効果音 星・キラーン05](https://on-jin.com/sound/listshow.php?pagename=ta&title=%E6%98%9F%E3%83%BB%E3%82%AD%E3%83%A9%E3%83%BC%E3%83%B305&janl=%E3%81%9D%E3%81%AE%E4%BB%96%E9%9F%B3&bunr=%E6%98%9F&kate=%E6%93%AC%E9%9F%B3%E3%83%BB%E3%82%AA%E3%83%8E%E3%83%9E%E3%83%88%E3%83%9A)より。
