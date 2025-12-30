from detectSensDataLeakage import detectPersonalPrivacy,SimplePatternRecognizer

recognizer, recognizer2 = detectPersonalPrivacy(),SimplePatternRecognizer("hello")
text = "zhang ming"
print(recognizer.find_pattern(text))