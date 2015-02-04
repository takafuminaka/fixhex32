armgcc付属のobjcopyが生成するhexファイルをI32HEXに準拠に変換するスクリプトです。
nrf51822のmbed環境でDrag&Dropで書き込みできるようにするために作成しました。

This is the script which convert objcopy created hex file to I32HEX compliant.
I created it to write HEX file by drag and drop on nrf51822 base mbed platform.

Usage 1: Just convert.
fixhex32.py < input.hex > output.hex

Usage 2: mergehex like 
cat softdevice.hex program.hex > merged.hex

Any kind of commnets are welcome.

T.Naka

