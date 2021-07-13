import win32gui
import win32process
import psutil

hwnd_title = dict()


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)

for h, t in hwnd_title.items():
    if t is not "":
        thread_id, process_id = win32process.GetWindowThreadProcessId(h)
        process = psutil.Process(process_id)
        print("--------------------")
        print(process.exe())
        print(process.name())
        # print(h, t)
