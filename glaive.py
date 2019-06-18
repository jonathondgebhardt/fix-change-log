import sublime
import sublime_plugin
import re


class ExampleCommand(sublime_plugin.TextCommand):

	# commitPattern = 'some-regex'

	def run(self, edit):
		# https://stackoverflow.com/questions/20182008/sublime-text-3-api-get-all-text-from-a-file
		region = sublime.Region(0, self.view.size())
		contents = self.view.substr(region)
		lines = contents.split('\n')

		formattedContents = ''
		for line in lines:
			formattedContents += self.fixFormatting(line) + '\n'

		self.view.replace(edit, region, formattedContents)


	def fixFormatting(self, x):
		if re.match(self.commitPattern, x) is None:
			print('matched', x)
			return self.addPeriod(x)

		return x

	def addPeriod(self, x):
		if x.endswith('.') is False:
			return x + '.'

		return x


