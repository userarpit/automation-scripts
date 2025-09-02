import pyautogui
import time
import pytesseract
import asyncio


async def write(action, interval=0.5, type="k"):
    if type == "h":
        pyautogui.hotkey(action)
        time.sleep(1)
    else:
        pyautogui.write(action, interval=interval)
        time.sleep(0.5)
        pyautogui.hotkey("enter")


async def main():
    # send windows + r to open the run window
    await write(["win", "r"], type="h")
    # send 'cmd' to open the command prompt
    await write("cmd", interval=0.2)
    time.sleep(1)
    # send 'alt+space=x' to maximize the command prompt
    await write(["alt", "space", "x"], type="h")
    # navigate to automation folder
    await write(r"cd Documents\Arpit\automation-scripts", 0.05)
    # send 'git status' to check the status of repository
    await write("git status", 0.1)

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    # Take screenshot
    screenshot = pyautogui.screenshot()

    # Use OCR to extract text
    text = pytesseract.image_to_string(screenshot)
    time.sleep(0.5)

    if "nothing to commit" not in text:
        # if there is something to add and commit, then run git add, git commit,
        # and git push (to update remote repository)

        msg = "There is something to add and commit"
        pyautogui.write(msg, interval=0.05)
        time.sleep(1)
        pyautogui.press("backspace", presses=len(msg), interval=0.05)

        await write("git add .", 0.1)
        await write("git commit -m 'update'", 0.1)
        await write("git push origin main", 0.1)
        # sleep for 5 seconds
        # time.sleep(5)

        msg = "All the files are pushed to github!"
        pyautogui.write(msg, interval=0.05)
        time.sleep(1)
        pyautogui.press("backspace", presses=len(msg), interval=0.05)

    else:
        # if there is nothing to add and commit, then send the message
        msg = "There is nothing to add and commit"
        pyautogui.write(msg, interval=0.05)
        time.sleep(1)
        pyautogui.press("backspace", presses=len(msg), interval=0.1)

    # bye message
    msg = "bye"
    pyautogui.write(msg, interval=0.2)
    time.sleep(1)
    pyautogui.press("backspace", presses=len(msg), interval=0.1)

    # exit command prompt
    await write("exit", 0.3)


if __name__ == "__main__":
    asyncio.run(main())
