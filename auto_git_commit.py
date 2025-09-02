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
    await write(["win", "r"], type="h")
    await write("cmd", 0.3)
    time.sleep(2)
    await write(["alt", "space", "x"], type="h")
    # time.sleep(2)
    await write("cd Documents", 0.1)
    await write("cd Arpit", 0.1)
    await write("cd automation-scripts", 0.1)
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
        msg = "There is something to add and commit"
        pyautogui.write(msg, interval=0.1)
        time.sleep(1)
        pyautogui.press("backspace", presses=len(msg), interval=0.1)

        await write("git add .", 0.1)
        await write("git commit -m 'update'", 0.1)
        await write("git push origin main", 0.1)
        time.sleep(5)
        msg = "Everything is pushed to github!"
        pyautogui.write(msg, interval=0.1)
        time.sleep(1)
        pyautogui.press("backspace", presses=len(msg), interval=0.1)

        msg = "bye"
        pyautogui.write(msg, interval=0.2)
        time.sleep(2)
        pyautogui.press("backspace", presses=len(msg), interval=0.1)

        await write("exit", 0.3)


if __name__ == "__main__":
    asyncio.run(main())
