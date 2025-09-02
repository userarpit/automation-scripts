import pyautogui
import time
import pytesseract
import asyncio

async def main():
    pyautogui.hotkey("win", "r")
    time.sleep(0.8)
    pyautogui.write("cmd", interval=0.3)
    pyautogui.hotkey("enter")
    time.sleep(1.5)
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

    # print("Extracted Text:", text)
    if "Untracked files" in text:
        msg = "There is something to add and commit"
        pyautogui.write("There is something to add and commit", interval=0.1)
        time.sleep(1)
        pyautogui.press("backspace", presses=len(msg), interval=0.1)

        await git_action("git add .")
        await git_action("git commit -m 'update'")
        await git_action("git push origin main")


async def git_action(action):
    pyautogui.write(action)
    time.sleep(1)
    pyautogui.hotkey("enter")


if __name__ == "__main__":
    asyncio.run(main())
