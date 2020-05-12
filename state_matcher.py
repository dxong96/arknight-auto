import cv2
import os
import numpy as np
import state_constants as const

def stateMatcherFactory(state, imagePath):
	ret = None
	if state == const.STATE_INITIAL:
		ret = InitialMatcher()
	elif state == const.STATE_INITIAL_NO_STAMINA:
		ret = InitialNoStamina()
	elif state == const.STATE_SQUAD_SELECTION:
		ret = SquadSelection()
	elif state == const.STATE_END_BATTLE:
		ret = EndBattle()
	elif state == const.STATE_END_BATTLE_LEVELUP:
		ret = EndBattleLevelUp()
	else:
		raise 'invalid state'

	ret.imagePath = imagePath
	return ret

TEMPLATE_WIDTH = 1080
def scaleFactor(image):
	w, h = image.shape[::-1]
	return h / TEMPLATE_WIDTH

def downscale(image, template):
	w, h = template.shape[::-1]
	if h == TEMPLATE_WIDTH:
		return template
	sf = scaleFactor(image)
	print('downscale by factor ' + str(sf))
	return cv2.resize(template, (0,0), fx=sf, fy=sf) 


def getTemplatePath(templateName):
	return os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'test-images', templateName))


def genericMatch(imagePath, templateName):
	img = cv2.imread(imagePath, 0)
	templatePath = getTemplatePath(templateName)

	# print('templatePath ' + templatePath)
	template = cv2.imread(templatePath, 0)
	template = downscale(img, template)
	w, h = template.shape[::-1]

	res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	top_left = min_loc
	print('min_val: ' + str(min_val) + ', min_loc: %d,%d' % top_left)
	return MatchResult(min_val <= 0.2, (min_loc[0], min_loc[1], w, h))

class MatchResult:
	def __init__(self, matches, location):
		self.matches = matches
		self.location = location

	def getCenter(self):
		w = self.location[2]
		h = self.location[3]
		return (self.location[0] + w/2, self.location[1] + h/2)


class InitialMatcher:
	START_BUTTON_RATIO = 3.44
	START_BUTTON_HEIGHT = 94 / 1080
	START_BUTTON_BOTTOM_PADDING = 1/24
	MATCH_PERCENT = 0.01

	def test(self):
		img = cv2.imread(self.imagePath, 0)
		iW, iH = img.shape[::-1]

		templatePath = getTemplatePath('initial-test2.png')
		# print('templatePath ' + templatePath)
		template = cv2.imread(templatePath, 0)
		template = downscale(img, template)
		w, h = template.shape[::-1]


		buttonHeight = self.START_BUTTON_HEIGHT * iH
		bottom = iH * (1 - self.START_BUTTON_BOTTOM_PADDING)
		bottom = int(bottom)

		top = bottom - buttonHeight * 2
		top = int(top)
		
		right = iW * (1 - 0.023)
		right = int(right)
		
		buttonWidth = self.START_BUTTON_RATIO * buttonHeight
		left = right - buttonWidth
		left = int(left)

		# print(str(top))
		# print(str(bottom))
		# print(str(left))
		# print(str(right))

		img = img[top:bottom, left:right]

		res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		top_left = (min_loc[0] + left, min_loc[1] + top)
		print('min_val: ' + str(min_val) + ', min_loc: %d,%d' % top_left)
		# bottom_right = (top_left[0] + w, top_left[1] + h)

		# cv2.rectangle(img,top_left, bottom_right, 255, 2)
		# cv2.imshow('start button block', img)
		# cv2.waitKey(0)

		if min_val <= self.MATCH_PERCENT:
			return MatchResult(True, (top_left[0], top_left[1] + h, w, h))

		templatePath = getTemplatePath('initial-test1.png')
		template = cv2.imread(templatePath, 0)
		template = downscale(img, template)
		w, h = template.shape[::-1]

		res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		top_left = (min_loc[0] + left, min_loc[1] + top)
		print('min_val: ' + str(min_val) + ', min_loc: %d,%d' % top_left)
		return MatchResult(min_val <= self.MATCH_PERCENT, top_left + (w, h))

class InitialNoStamina:
	def test(self):
		result1 = genericMatch(self.imagePath, 'no-stamina-test1.jpg')
		result2 = genericMatch(self.imagePath, 'no-stamina-test2.jpg')
		return MatchResult(result1.matches and result2.matches, None)

MEMBERS_SECTION_RATIO = 1.9
class SquadSelection:
	def test(self):
		img = cv2.imread(self.imagePath, 0)
		iW, iH = img.shape[::-1]
		
		templatePath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'test-images', 'squad-selection-test.png'))
		# print('templatePath ' + templatePath)
		template = cv2.imread(templatePath, 0)
		template = downscale(img, template)
		w, h = template.shape[::-1]

		membersSectionTop = 0.11 * iH
		membersSectionBottom = iH - membersSectionTop
		membersSectionHeight = membersSectionBottom - membersSectionTop
		membersSectionWidth = membersSectionHeight * MEMBERS_SECTION_RATIO
		
		horizontalPartSize = int(membersSectionWidth / 7)
		verticalPartSize = int(membersSectionHeight / 2)
		paddingSize = int((iW - membersSectionWidth) / 2)

		startButtonLeft = paddingSize + 6 * horizontalPartSize
		startButtonTop = int(membersSectionTop + verticalPartSize)
		startButtonBlock = img[startButtonTop:startButtonTop+verticalPartSize, startButtonLeft:iW]
		img = startButtonBlock


		res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		# top_left = min_loc
		# bottom_right = (top_left[0] + w, top_left[1] + h)

		# cv2.rectangle(img,top_left, bottom_right, 255, 2)
		# cv2.imshow('start button block', img)
		# cv2.waitKey(0)
		# print(min_val)

		top_left = (startButtonLeft + min_loc[0], startButtonTop + min_loc[1])
		# print('min_val: ' + str(min_val) + ', min_loc: %d,%d' % top_left)
		return MatchResult(min_val <= 0.2, (top_left[0], top_left[1], w, h))

class EndBattle:
	def test(self):
		result = genericMatch(self.imagePath, 'end-battle-levelup-test.png')
		if result.matches:
			return result

		result = genericMatch(self.imagePath, 'end-battle-test1.png')
		result.matches = result.matches and \
			genericMatch(self.imagePath, 'end-battle-test2.png').matches
		
		return result

class EndBattleLevelUp:
	def test(self):
		return genericMatch(self.imagePath, 'end-battle-levelup-test.png')