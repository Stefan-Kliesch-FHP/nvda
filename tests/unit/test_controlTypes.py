# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2021 NV Access Limited, Babbage B.V.

"""Unit tests for the controlTypes module.
"""

import unittest
import controlTypes
import versionInfo
from . import PlaceholderNVDAObject
from controlTypes.processAndLabelStates import _processNegativeStates, _processPositiveStates


class TestLabels(unittest.TestCase):
	@unittest.skipIf(versionInfo.version_year >= 2022, "Deprecated code")
	def test_legacy_roleLabels(self):
		"""Test to check whether every role has its own label in controlTypes.roleLabels"""
		for name, const in vars(controlTypes).items():
			if name.startswith("ROLE_"):
				self.assertIsNotNone(controlTypes.roleLabels.get(const),msg="{name} has no label".format(name=name))

	def test_role_displayString(self):
		"""Test to check whether every role has its own display string"""
		for role in controlTypes.Role:
			role.displayString

	@unittest.skipIf(versionInfo.version_year >= 2022, "Deprecated code")
	def test_legacy_positiveStateLabels(self):
		"""Test to check whether every state has its own label in controlTypes.stateLabels"""
		for name, const in vars(controlTypes).items():
			if name.startswith("STATE_"):
				self.assertIsNotNone(controlTypes.stateLabels.get(const),msg="{name} has no label".format(name=name))

	def test_state_displayString(self):
		"""Test to check whether every state has its own display string and negative display string"""
		for state in controlTypes.State:
			state.displayString
			state.negativeDisplayString


class TestProcessStates(unittest.TestCase):

	def setUp(self):
		self.obj = PlaceholderNVDAObject()
		self.obj.role = controlTypes.Role.CHECKBOX
		self.obj.states = {
			controlTypes.State.FOCUSABLE,
			controlTypes.State.INVALID_ENTRY,
			controlTypes.State.FOCUSED,
			controlTypes.State.REQUIRED
		}

	def test_positiveStates(self):
		self.assertSetEqual(
			_processPositiveStates(
				self.obj.role,
				self.obj.states,
				controlTypes.OutputReason.FOCUS,
				self.obj.states
			),
			{controlTypes.State.INVALID_ENTRY, controlTypes.State.REQUIRED}
		)

	def test_negativeStates(self):
		self.assertSetEqual(
			_processNegativeStates(
				self.obj.role,
				self.obj.states,
				controlTypes.OutputReason.FOCUS,
				None
			),
			{controlTypes.State.CHECKED}
		)

class TestStateOrder(unittest.TestCase):

	def test_positiveMergedStatesOutput(self):
		obj = PlaceholderNVDAObject()
		obj.role = controlTypes.Role.CHECKBOX
		obj.states = {
			controlTypes.State.CHECKED,
			controlTypes.State.FOCUSABLE,
			controlTypes.State.FOCUSED,
			controlTypes.State.SELECTED,
			controlTypes.State.SELECTABLE
		}
		self.assertEqual(
			controlTypes.processAndLabelStates(
				obj.role,
				obj.states,
				controlTypes.OutputReason.FOCUS,
				obj.states,
				None
			),
			[controlTypes.State.CHECKED.displayString]
		)

	def test_negativeMergedStatesOutput(self):
		obj = PlaceholderNVDAObject()
		obj.role = controlTypes.Role.CHECKBOX
		obj.states = {
			controlTypes.State.FOCUSABLE,
			controlTypes.State.FOCUSED,
			controlTypes.State.SELECTED,
			controlTypes.State.SELECTABLE
		}
		self.assertEqual(
			controlTypes.processAndLabelStates(
				obj.role,
				obj.states,
				controlTypes.OutputReason.FOCUS,
				obj.states,
				None
			),
			[controlTypes.State.CHECKED.negativeDisplayString]
		)
