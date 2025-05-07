# -*- coding: utf-8 -*-

# 動体検知アプリの作成_0J02011_加納陽太

# import文
#=========================================================
import cv2
# cv2はOpenCVのライブラリで、画像処理やコンピュータビジョンのための関数を提供するライブラリ
import flet as ft
# fletは、PythonでGUIアプリケーションを作成するためのライブラリで、Webアプリケーションやデスクトップアプリケーションを簡単に作成できる
import threading
# threadingは、Pythonのスレッドを扱うためのライブラリで、マルチスレッドプログラミングを可能にする
#========================================================


# カメラ起動変数capを共有するための変数（グローバル）
cap = None

# 動体検知アプリのメイン処理・関数
#========================================================
def main(page: ft.Page):
    page.title = "動体検知アプリ"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # MainAxisAlignment.CENTERは、ページの垂直方向の配置を中央に設定するためのもの
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # CrossAxisAlignment.CENTERは、ページの水平方向の配置を中央に設定するためのもの
    page.window_width = 700 # ウィンドウの幅を600pxに設定
    page.window_height = 700 # ウィンドウの高さを700pxに設定

    # 動体検出を開始・終了ボタンを押したときの処理
    #========================================================    
    def start_detection(e):
        threading.Thread(target=Motion_detection, daemon=True).start()
        # threading.Threadは、スレッドを作成するためのクラス
        # targetは、スレッドが実行する関数を指定するためのもの

    def end_detection(e):
        global cap
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
    #========================================================

    # 動体検知アプリのメイン関数を呼び出す
    title_label = ft.Text("動体検出         アプリの作成",font_family= "GN_Kill", size = 80, weight = "bold", color = "blue")
    strat_button = ft.ElevatedButton("動体検出開始", on_click = start_detection,style = ft.ButtonStyle(color = ft.colors.WHITE,bgcolor=ft.colors.BLUE_GREY_500), elevation = 30)
    end_button = ft.ElevatedButton("動体検出終了", on_click = end_detection,style = ft.ButtonStyle(color = ft.colors.WHITE,bgcolor = ft.colors.RED), elevation = 30)


    title_stack = ft.Stack(
        # Stackは、子要素を重ねて配置するためのコンテナで、子要素を重ねて表示することができる
        controls = [          
 
            # container 一つ一つに範囲を与えその範囲内で配置させる　詳細必要
            ft.Container(
                content = title_label,
                
                left = 80,  # X座標
                top = 130,  # Y座標
                width = 500, # 幅  
                height = 500, # 高さ 
            ),
            ft.Container (
                content = strat_button,
                left = 230,  # X座標
                top = 520,   # Y座標 
                width = 200, # 幅  
                height = 50, # 高さ 
               
            ),
            ft.Container (
                content = end_button,
                left = 230,  # X座標
                top = 580,   # Y座標
                width = 200, # 幅   
                height = 50, # 高さ 
               
            ),
        ],
 
        # ボタンの配置範囲の指定　範囲外だと見切れる
        # 範囲を画面全体に広げる
        expand=True 
        # expand=Trueは、Stackが親コンテナのサイズに合わせて拡張されることを指定するためのもの
        # これにより、Stackが親コンテナのサイズに合わせて拡張されます。
    )
 
    page.add(title_stack)
    # page.addは、ページにコンテナを追加するための関数
    # ここでは、title_stackをページに追加しています。
#========================================================


# 動体検出アプリ内部処理・関数
#========================================================
def Motion_detection():
    # 動体検知アプリのメイン関数
    #========================================================
    global cap # capをグローバル変数として宣言
    cap = cv2.VideoCapture(0) # Webカメラを起動する。
    # cap = cv2.VideoCapture(0)は、Webカメラを起動するためのOpenCVの関数

    avg = None  # avg変数を初期化
    threshold = 3 # 閾値の設定
    

    while True:
        # 1フレームずつ取得する。
        ret, frame = cap.read() # Webカメラからfream(フレーム)を取得(retは成功したかどうかのフラグ)

        # フレームが取得できなかった場合は終了
        if not ret:
            break

        # グレースケールに変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # cv2.BGRからフレームをグレースケールに変換
        # cv2.cvtColorはOpenCVの関数で、画像の色空間を変換するために使用される。
        # cv2.COLOR_BGR2GRAYは、BGR（青、緑、赤）からグレースケールへの変換を指定する定数。

        # 比較用のフレームを取得する
        if avg is None:
            avg = gray.copy().astype("float") # 最初のフレームを取得してavgに格納
            # ここでのastype("float")は、フレームを浮動小数点数型に変換するためのもの
            # これは、後で加重平均を計算するために必要です。
            # gray.copy()は、元のフレームを変更しないようにコピーを作成するためのもの
            # これにより、元のフレームはそのまま残ります。
            continue

        # 動体検知
        #================================================
        # フレームの平均を計算する
        
        # 現在のフレームと移動平均との差を計算
        cv2.accumulateWeighted(gray, avg, 0.9) # フレームの平均を計算する
        # cv2.accumulateWeightedは、指定した重みでフレームを加重平均する関数
        # ここでは、0.9の重みでフレームを加重平均しています。
        # これは、過去のフレームの影響を90%残し、新しいフレームの影響を10%加えることを意味します。
        # これにより、動体検知の精度が向上します。

        # フレームの平均を整数に変換する
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg)) # フレームの平均と現在のフレームの差分を計算する
        # cv2.absdiffは、2つの画像の絶対差を計算する関数
        # cv2.convertScaleAbsは、画像をスケール変換して絶対値を計算する関数
        
        # 二値化処理（閾値3を超えた画素を255にする）
        #================================================
        # デルタ画像に閾値処理を行う
        thresh = cv2.threshold(frameDelta, threshold, 255, cv2.THRESH_BINARY)[1] # フレームの平均と現在のフレームの差分を閾値処理する
        # [1]は、閾値処理の結果を取得するためのもの。[1]は、[0]が真偽値、[1]が閾値処理の結果を返すため、[1]を指定することで、閾値処理の結果を取得することができます。
        # cv2.thresholdは、画像を二値化するための関数で、指定した閾値を超えた画素を255に、それ以外を0に変換する。
        # cv2.THRESH_BINARYは、二値化の方法を指定する定数で、閾値を超えた画素を255に、それ以外を0にする。
        #================================================
        
        # 画像の閾値に輪郭線を入れる
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.findContoursは、画像から輪郭を検出するための関数
        # contoursは、検出された輪郭のリストで、hierarchyは、輪郭の階層情報を持つ配列
        # thresh.copy()は、元の画像を変更しないようにコピーを作成するためのもの(grayのコピーと同様)
        # cv2.RETR_EXTERNALは、外部輪郭のみを検出するための定数
        # cv2.CHAIN_APPROX_SIMPLEは、輪郭を簡略化するための定数

        frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        # cv2.drawContoursは、画像に輪郭を描画するための関数
        # frameは、描画する画像で、contoursは、描画する輪郭のリスト
        # -1は、すべての輪郭を描画することを指定するためのもの
        # (0, 255, 0)は、描画する色を指定するためのBGR形式のタプル
        # ここでは、緑色を指定しています。
        # 3は、描画する輪郭の太さを指定するためのもの
        # ここでは、3ピクセルの太さを指定しています。
        #================================================

        # 結果を出力
        cv2.imshow("Frame", frame)  # 動体検知画面を表示する
        key = cv2.waitKey(30) # 30ps(キー入力用)
        
    # 動作終了のためのキー入力
    #==========================================
        # qキーが押されたら動作終了
        if key == ord("q"):
            break

    # while文をブレイクした際、
    # Webカメラを解除する
    cap.release()
    # cap.release()は、Webカメラを解除するための関数
    # これにより、Webカメラを解放することができます。
    cv2.destroyAllWindows()
    # cv2.destroyAllWindows()は、OpenCVで作成したウィンドウをすべて閉じるための関数
    # これにより、Webカメラを解除することができます。
    #==========================================
    #========================================================


#========================================================




# fletのメイン関数を呼び出す
ft.app(target=main)