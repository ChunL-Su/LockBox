from PyQt6.QtCore import QProcess


def launch_chrome(url):
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"  # 修改为你的 Chrome 路径
    process = QProcess()

    # Windows
    process.startDetached(chrome_path, [url])

    # 对于 macOS 和 Linux，可能需要不同的参数格式
    # macOS: process.startDetached("open", ["-a", "Google Chrome", url])
    # Linux: process.startDetached("google-chrome", [url])


if __name__ == '__main__':
    # 使用示例
    launch_chrome("https://www.baidu.com")