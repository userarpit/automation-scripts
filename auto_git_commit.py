import pyautogui
import time
import pytesseract
import asyncio


async def main():
    # await do_action("git add .", 0.1)
    pyautogui.hotkey("win", "r")
    time.sleep(0.8)
    await do_action("cmd", 0.3)
    # pyautogui.write("cmd", interval=0.3)
    # pyautogui.hotkey("enter")
    # time.sleep(1.5)
    pyautogui.hotkey("alt", "space", "x")
    time.sleep(1.2)
    
    pyautogui.write("cd Documents", interval=0.1)
    time.sleep(0.5)
    pyautogui.hotkey("enter")
    pyautogui.write("cd Arpit", interval=0.1)
    time.sleep(0.5)
    pyautogui.hotkey("enter")
    pyautogui.write("cd automation-scripts", interval=0.1)
    time.sleep(0.5)
    pyautogui.hotkey("enter")
    pyautogui.write("git status", interval=0.1)
    time.sleep(1)
    pyautogui.hotkey("enter")

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    # Take screenshot
    screenshot = pyautogui.screenshot()

    # Use OCR to extract text
    text = pytesseract.image_to_string(screenshot)
    time.sleep(1)
    print("Extracted Text:", text)
    if not ("nothing to commit" in text):
        msg = "There is something to add and commit"
        pyautogui.write("There is something to add and commit", interval=0.1)
        time.sleep(1)
        pyautogui.press("backspace", presses=len(msg), interval=0.1)

        await do_action("git add .", 0.1)
        await do_action("git commit -m 'update'", 0.1)
        await do_action("git push origin main", 0.1)


async def do_action(action, interval=0.5):
    pyautogui.write(action, interval=interval)
    time.sleep(1.5)
    pyautogui.hotkey("enter")


if __name__ == "__main__":
    asyncio.run(main())
