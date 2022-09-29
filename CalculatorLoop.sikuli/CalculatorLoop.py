running = True

def runHotkey (event) :
	global running
	running = False

Env.addHotkey(Key.F12, KeyModifier.CTRL, runHotkey)

click("WinKey.png")
wait("WinMenuIcon.png")
type("calc"+Key.ENTER)
wait(Pattern("CalcKeyBd.png").similar(0.50))
click(Pattern("CalcKeyBd.png").similar(0.50).targetOffset(-126,27)) # click 1

while exists(Pattern("CalcKeyBd.png").similar(0.50)) and running:
    click(Pattern("CalcKeyBd.png").similar(0.50).targetOffset(115,25)) # click +
    click(Pattern("CalcKeyBd.png").similar(0.50).targetOffset(-126,27)) # click 1

click(Pattern("CalcKeyBd.png").similar(0.50).targetOffset(115,74)) # click =
