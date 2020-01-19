import language_check
tool = language_check.LanguageTool('en-US')
text = u'The Birch looked stark. White and Lonesome, the boxes held by a bright red snapper.'
matches = tool.check(text)

print(language_check.correct(text, matches))
