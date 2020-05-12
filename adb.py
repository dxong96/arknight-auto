import subprocess
import tempfile
import os
import argparse
import re

class ScreenCapResult:
	def __init__(self, name):
		self.name = name

	def __del__(self):
		print("ScreenCapResult destructing")
		os.remove(self.name)


DIMENSION_PATTERN = re.compile('(\\d+)x(\\d+)')

class AdbClient:
	def __init__(self, serial, adbPath='adb'):
		self.serial = serial
		self.adbPath = adbPath

	def __subprocessArgs(self, args):
		adbCmd = [self.adbPath]
		if self.serial != None:
			adbCmd.extend(['-s', self.serial])
		adbCmd.extend(args)

		return adbCmd

	def captureScreen(self):
		with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
			# print(subprocess.list2cmdline(["adb", "exec-out", "screencap", "-p"]))
			subprocess.run(self.__subprocessArgs(["exec-out", "screencap", "-p"]), stdout=tf)
			ret = ScreenCapResult(tf.name)
			return ret

	def tap(self, x, y):
		print('tap ' + str(x) + ' ' + str(y))
		subprocess.run(self.__subprocessArgs(["shell", "input", 'tap', str(x), str(y)]))

	def testAdb(self):
		completed = subprocess.run(self.__subprocessArgs(["shell", "echo", "1"]), capture_output=True, text=True)
		# check stdout == 1
		output = completed.stdout
		connected = len(output) > 0 and output[0] == '1'
		if connected:
			return True

		output = completed.stderr

		if output.find('more than one') != -1:
			print('Please configure the device to connect')
			listDevices = subprocess.run(["adb", "devices"], capture_output=True, text=True)
			print(listDevices.stdout)
			return False

		if output.find('unauthorized') != -1:
			print('Please allow computer when it pops up in your device')
			return False

		print(output)
		return False

	def getDimensions(self):
		subprocess.run(self.__subprocessArgs(["shell", "wm", "size"]))
		output = completed.stdout
		match = DIMENSION_PATTERN.match(output)
		if match == None:
			return None

		return (match.group(1), match.group(2))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Arknights Auto')
	parser.add_argument('--serial', help='serial number or connection endpoint', nargs=1)
	args = parser.parse_args()
	print('got serial = ' + str(args.serial))

	adbOk = testAdb()
	if adbOk:
		capResult = captureScreen()
		print(capResult.name)
		# subprocess.run(["start", capResult.name])
		input("Press Enter to continue...")
		print("closing")