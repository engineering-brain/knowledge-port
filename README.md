# Knowledge-port
モノづくりに関する発話に対して、関連するモノづくり知識をWebブラウザに表示する「ナレッジ・ポート」。この「ナレッジ・ポート」を利用するためのサンプルプログラムを共有するリポジトリです。
## 音声認識＆文章送信コード assist_speech_recog.py
### プログラム概要
マイク音声を文章として認識し、その文章をHTTPリクエストとしてナレッジ・ポートの稼働するサーバーに送信するPythonコードです。
### 使い方など
["assist_speech_recog"フォルダ](https://github.com/engineering-brain/knowledge-port/tree/development/assist_speech_recog)からpythonコード"assist_speech_recog.py"が入手できます。

使用方法は"assist_speech_recog"フォルダの[README.md](https://github.com/engineering-brain/knowledge-port/tree/development/assist_speech_recog/README.md)に記載していますので、ご参照ください。

## スクリーンショット＆文章送信コード assist_screenshot.py
### プログラム概要
PC画面のアクティブなウィンドウのスクリーンショットを取得し、それから日本語の文章を抽出します。さらに、その文章をHTTPリクエストとしてナレッジ・ポートの稼働するサーバーに送信するPythonコードです。
### 使い方など
["assist_screenshot"フォルダ](https://github.com/engineering-brain/knowledge-port/tree/development/assist_screenshot)からpythonコード"assist_screenshot.py"が入手できます。

使用方法は"assist_speech_recog"フォルダの[README.md](https://github.com/engineering-brain/knowledge-port/tree/development/assist_screenshot/README.md)に記載していますので、ご参照ください。

## 備考
できるだけ広く知識を表示するアルゴリズムを採用しているため、モノづくりとは関連の無い発言に対しても、何らかのモノづくり知識が表示される場合があります。この点については、徐々に改善を図りますのでご了承ください。

SSL(Secure Sockets Layer)による発話や知識の送受信を採用し、エンジニアリング・ブレインのプライバシーポリシーに沿って適切な情報管理を行っていますが、本プログラムで「ナレッジ・ポート」に送信される情報の漏洩が気になる方は、"setting.txt"に送信したくない単語や文章を記載してください。"setting.txt"に記載いただいた単語や文章を含む発話は、「ナレッジ・ポート」には送信されません。

Windows環境での動作のみ確認済みです。MacやLinux環境での動作は確認しておりません。
## Author
* P. Q.
* Engineering Brain
* https://engineering-brain.com
