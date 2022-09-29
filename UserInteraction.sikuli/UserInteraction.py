name = input ("Enter your name")
popup ("Hello "+name, "Hello!")

someText = inputText ("Enter some text!")
popError ("Ah! "+someText)

myOptions = ('1', '2', '3', '4', '5')

result = select ("Pick a number!", options = myOptions)
choice = popAsk ("Did you select "+result+"?")

                                