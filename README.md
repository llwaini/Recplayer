# RecPlayer Docs

## Development Logs

### 20200623

完成最小功能，基于即定通讯协议，完成arduino控制的录音，终止，播放三项基本功能，支持指定文件播放

未完成事项：

1. 跨平台测试，当前脚本仅在MacOS上测试跑通
2. Arduino设备兼容，未测试uno，mega等主板，PySerialMonitor待完善
3. 暂不支持打断播放
4. 暂不支持录音，终止和播放等功能的Arduino信息反馈



## 简述

考虑到，项目已经跑了一半，所以在需求书中不做重复的信息补充了。

简单说，这是一个通过linux主机，实现录音，可选文件播放的软硬件结合项目。

功能描述：

1. 可通过USB通讯与Arduino，实时双向数据通讯
2. 可通过Arduino发送的指令，实现，录音，终止录音，和制定音频播放的功能
3. 为实现功能2，软件功能需要支持Arduino录音文件命名和制定文件名播放的功能
4. 播放状态反馈，完成录音播放指令后，告知Arduino，已完成任务，或播放失败

附加功能 —— 有更好，没无所谓：

1. Arduino指令控制加减音量

## 通讯协议

### 协议构成

| 框架   | 指令    | 内容           | 结尾符           |
| ---- | ----- | ------------ | ------------- |
| 描述   | 即命名名称 | 传递参数（如果需要的话） | “\r\n”用于做指令切包 |



### Example

#### Arduino发送

内容："record 1.mp3\r\n"

Arduino指令

```c++
Serial.println("record 1.mp3");
```

**NOTE:** println即带"\r\n"发送指令，用于换行或者指令接收端识别发送的结尾符

Python串口接收，返回格式String内容和Boolean状态

```python
def read_line(self):
    packet = ''
    state = False
    try:
        packet = self.serial.readline()
        packet = packet.decode()
        state = True
    except Exception as e:
        # self.is_connected = False
        # notebook.error('Serial reading error', exc_info=True)
        pass

    return packet, state
```

接收到：“record 1.mp3\r\n”

数据切割

```python
data = packet.strip('\r\n')
command = data.split(' ')
```

command类型为列表，command[0]即“record”，command[1]即“1.mp3”，通过strip移除结尾符。

可自行Google各种Python字符串处理指令 (Python split string...)，简单好用。



### 协议内容

#### 指令1 - 开始录音

```python
"record 1.mp3\r\n"
```

#### 返回

```python
"OK"
```

指令：开始录音

内容：存储的文件名称

返回：OK



#### 指令2 - 终止录音和播放

```python
"stop\r\n"
```

#### 返回

```python
"OK"
```

指令：终止录音和播放

内容：空

返回：OK



#### 指令3 - 指定文件播放

```python
"play 1.mp3\r\n"
```

#### 返回

```python
"OK"
"ERROR"
"Finished"
```

指令：终止录音和播放

内容：播放对象的文件名称

返回：

- OK - 开始播放
- ERROR - 播放失败
- Finished - 完成播放

### 更多内容

TBD...