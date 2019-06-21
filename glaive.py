import sublime
import sublime_plugin
import re


class ExampleCommand(sublime_plugin.TextCommand):

	commitPattern = ''
	issueNumberPattern = ''
	hotFixIssueNumber = ''

	def run(self, edit):

		region = self.getScreenRegion()
		contents = self.getRegionContents(region)

		contents = self.removeMerges(contents)

		formattedContents = ''
		for line in contents:
			formattedContents += self.fixFormatting(line) + '\n'

		self.view.replace(edit, region, formattedContents)

	def getScreenRegion(self):
		return sublime.Region(0, self.view.size())

	def getRegionContents(self, x):
		# https://stackoverflow.com/questions/20182008/sublime-text-3-api-get-all-text-from-a-file
		contents = self.view.substr(x)
		lines = contents.split('\n')

		return lines

	def removeMerges(self, x):
		merges = ["merge pull", "merge branch", "merge remote"]
		contents = []

		for line in x:
			clean = True

			for m in merges:
				if line.lower().find(m) is not -1:
					clean = False
					break

			if clean is True:
				contents.append(line)
			
		return contents


	def fixFormatting(self, x):
		if re.match(self.commitPattern, x) is None and len(x) > 0:
			# print('matched', x)
			x = self.prependIssueNumber(x)
			x = self.addPeriod(x)
			x = self.capitalizeFirstLetter(x)

		return x

	def addPeriod(self, x):
		if x.endswith('.') is False:
			return x + '.'

		return x

	def prependIssueNumber(self, x):
		if re.search(self.issueNumberPattern, x) is None:
			return self.hotFixIssueNumber + ' ' + x

		return x

	def capitalizeFirstLetter(self, x):
		commit = self.splitCommit(x)
		issueNum = self.splitIssueNumber(x)

		return issueNum + ' ' + commit[:1].upper() + commit[1:]

	def splitCommit(self, x):
		if re.search(self.issueNumberPattern, x) is not None:
			return x[10:]

		return x
		
	def splitIssueNumber(self, x):
		if re.search(self.issueNumberPattern, x) is not None:
			return x[:9]

		return ''
