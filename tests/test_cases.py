import unittest
import os
from state_matcher import stateMatcherFactory
import state_constants as const

def testImageAbsPath(name):
	return os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'test-images', name))

class TestInitialMatcher(unittest.TestCase):
	def test_againstEndBattle(self):
		matcher = stateMatcherFactory(const.STATE_INITIAL, testImageAbsPath('end-battle-sample.jpg'))
		result = matcher.test()
		
		self.assertFalse(result.matches, msg=('not suppose to match but found at %d, %d' % result.location[:2]))

	def test_againstSquadSelection(self):
		matcher = stateMatcherFactory(const.STATE_INITIAL, testImageAbsPath('squad-selection-sample.png'))
		result = matcher.test()
		
		self.assertFalse(result.matches, msg=('not suppose to match but found at %d, %d' % result.location[:2]))

	def test_againstInitial(self):
		samples = ['initial-sample.png', 'initial-sample2.jpg', 'initial-sample3.png']
		for sample in samples:
			matcher = stateMatcherFactory(const.STATE_INITIAL, testImageAbsPath(sample))
			result = matcher.test()
		
			formatArgs = result.location[:2] + (sample,)
			self.assertTrue(result.matches, msg=('supposed to match but found at %d, %d for sample %s' % formatArgs))


class TestSquadSelection(unittest.TestCase):
	def test_againstInitial(self):
		samples = ['initial-sample.png', 'initial-sample2.jpg', 'initial-sample3.png']
		for sample in samples:
			matcher = stateMatcherFactory(const.STATE_SQUAD_SELECTION, testImageAbsPath(sample))
			result = matcher.test()
		
			formatArgs = result.location[:2] + (sample,)
			self.assertFalse(result.matches, msg=('not supposed to match but found at %d, %d for sample %s' % formatArgs))

		def test_againstSquadSelection(self):
			matcher = stateMatcherFactory(const.STATE_SQUAD_SELECTION, testImageAbsPath('squad-selection-sample.png'))
			result = matcher.test()
		
			self.assertTrue(result.matches, msg=('suppose to match but found at %d, %d' % result.location[:2]))


class TestEndBattle(unittest.TestCase):
	def test_againstSquadSelection(self):
		matcher = stateMatcherFactory(const.STATE_END_BATTLE, testImageAbsPath('end-battle-sample.jpg'))
		result = matcher.test()
		
		self.assertTrue(result.matches, msg=('suppose to match but found at %d, %d' % result.location[:2]))

	def test_againstInitial(self):
		samples = ['initial-sample.png', 'initial-sample2.jpg', 'initial-sample3.png']
		for sample in samples:
			matcher = stateMatcherFactory(const.STATE_END_BATTLE, testImageAbsPath(sample))
			result = matcher.test()
		
			formatArgs = result.location[:2] + (sample,)
			self.assertFalse(result.matches, msg=('not supposed to match but found at %d, %d for sample %s' % formatArgs))