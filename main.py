from adb import AdbClient
from state_matcher import stateMatcherFactory
import time
import argparse
import state_constants as const

def main():
	parser = argparse.ArgumentParser(description='Arknights Auto')
	parser.add_argument('-s', '--serial', help='serial number or connection endpoint', nargs='?')
	parser.add_argument('-c', '--cycles', help='times to run, defaults to 0, 0 cycles means running 1000 times', nargs='?', type=int, default=0)
	parser.add_argument('--adb', help='path to adb executable', default='adb')
	args = parser.parse_args()

	adbClient = AdbClient(args.serial, args.adb)
	if adbClient.testAdb():
		print('successfully setup adb')
	else:
		print('failed to setup adb')
		return

	inputCycles = args.cycles
	if inputCycles < 0:
		print('invalid cycles, cycles must be >= 0')
		return

	if inputCycles == 0:
		print('cycles detected: 1000')
		inputCycles = 1000
	else:
		print('cycles detected: ' + str(inputCycles))

	cycle = 0
	while cycle < inputCycles:
		print('Checking inital screen')
		ss = adbClient.captureScreen()
		tester = stateMatcherFactory(const.STATE_INITIAL, ss.name)
		testResult = tester.test()
		if not testResult.matches:
			print('please go to inital screen')
			return

		adbClient.tap(*testResult.getCenter())
		time.sleep(2)

		print('Checking screen is at squad selection')
		ss = adbClient.captureScreen()
		tester = stateMatcherFactory(const.STATE_INITIAL_NO_STAMINA, ss.name)
		testResult = tester.test()
		if testResult.matches:
			print('out of stamina')
			return

		# print('imagePath' + ss.name)
		# input("Press Enter to continue...")
		tester = stateMatcherFactory(const.STATE_SQUAD_SELECTION, ss.name)
		testResult = tester.test()
		if not testResult.matches:
			print('not at squad selection screen')
			return

		print('starting battle')
		adbClient.tap(*testResult.getCenter())

		print('waiting for 90s for battle to end')
		time.sleep(90)

		timesExtended = 0
		# wait up to 30 mins
		while timesExtended < 60:
			print('checking battle ended')
			ss = adbClient.captureScreen()
			tester = stateMatcherFactory(const.STATE_END_BATTLE, ss.name)
			testResult = tester.test()
			if testResult.matches:
				adbClient.tap(*testResult.getCenter())
				print('finished a cycle')
				time.sleep(10)
				cycle += 1
				break

			print('battle not ended waiting for another 30s')
			time.sleep(30)
			timesExtended += 1

	print('ending auto')



if __name__ == '__main__':
	main()