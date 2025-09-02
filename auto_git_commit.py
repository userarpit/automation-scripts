import pyautogui
import time
import pytesseract
import asyncio


async def main():
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    await do_action("cmd", 0.3)
    time.sleep(1)
    pyautogui.hotkey("alt", "space", "x")
    time.sleep(1)
    await do_action("cd Documents", 0.1)
    await do_action("cd Arpit", 0.1)
    await do_action("cd automation-scripts", 0.1)
    await do_action("git status", 0.1)

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    # Take screenshot
    screenshot = pyautogui.screenshot()

    # Use OCR to extract text
    text = pytesseract.image_to_string(screenshot)
    time.sleep(1)

    if "nothing to commit" not in text:
        msg = "There is something to add and commit"
        pyautogui.write("There is something to add and commit", interval=0.1)
        time.sleep(1)
        pyautogui.press("backspace", presses=len(msg), interval=0.1)

        await do_action("git add .", 0.1)
        await do_action("git commit -m 'update'", 0.1)
        await do_action("git push origin main", 0.1)
        await do_action("bye", 0.1)
        await do_action("exit",0.1)

async def do_action(action, interval=0.5):
    pyautogui.write(action, interval=interval)
    time.sleep(0.5)
    pyautogui.hotkey("enter")


if __name__ == "__main__":
    asyncio.run(main())
