@echo off

@rem 7-Zipがインストールされているパスを指定
set ZIP_PATH=C:\Program Files\7-Zip\7z.exe

@rem 学習済みモデルのパスを指定
set MODEL_PATH=E:\ReinVision\resources\pretrained\release\generic\craft.pth

@rem codeフォルダが存在するルートディレクトリを指定
set ROOT_DIR=E:\ReinVision\rein-vision-api\blog_craft

@rem 圧縮結果のファイル名
set OUTPUT_NAME=blog_craft

if exist %MODEL_PATH% (
    cd %ROOT_DIR%

    "%ZIP_PATH%" a %OUTPUT_NAME%.tar code %MODEL_PATH%
    "%ZIP_PATH%" a %OUTPUT_NAME%.tar.gz %OUTPUT_NAME%.tar

    del %OUTPUT_NAME%.tar
)
