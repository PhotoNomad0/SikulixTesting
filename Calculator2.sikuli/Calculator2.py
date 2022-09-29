click("WindowsStart.png")
wait("SearchPrompt.png")
type("calc"+Key.ENTER)
wait(Pattern("CalcKeyBd-1.png").similar(0.58))
click(Pattern("CalcKeyBd-1.png").similar(0.58).targetOffset(-122,23)) # click 1
click(Pattern("CalcKeyBd-1.png").similar(0.58).targetOffset(118,24)) # click +
click(Pattern("CalcKeyBd-1.png").similar(0.58).targetOffset(-122,23)) # click 1
click(Pattern("CalcKeyBd-1.png").similar(0.58).targetOffset(111,77)) # click =
