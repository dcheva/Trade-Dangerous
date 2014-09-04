#! /usr/bin/env python
#---------------------------------------------------------------------
# Copyright (C) Oliver 'kfsone' Smith 2014 <oliver@kfs.org>:
#  You are free to use, redistribute, or even print and eat a copy of
#  this software so long as you include this copyright notice.
#  I guarantee there is at least one bug neither of us knew about.
#---------------------------------------------------------------------
# Elite Market Data Net :: Modules :: ItemRecord
#  EMDN record description.

import re

class ItemRecord(object):
	"""
		Describes a record pulled from the Firehose.
	"""
	systemStationRe = re.compile(r'^(.*?)\s*\((.*?)\)$')

	def __init__(self, askingCr, payingCr, demand, demandLevel, stock, stockLevel, category, item, location, timestamp):
		self.askingCr, self.payingCr = int(askingCr or 0), int(payingCr or 0)
		self.demand, self.demandLevel = int(demand or 0), int(demandLevel or 0)
		self.stock, self.stockLevel = int(stock or 0), int(stockLevel or 0)
		self.category, self.item = category, item
		self.system, self.station = ItemRecord.systemStationRe.match(location).group(1, 2)
		self.timestamp = timestamp

	def str(self):
		return "{},{},{},{},{},{},{},{},{} ({}),{}".format(
		        self.askingCr, self.payingCr, self.demand, self.demandLevel, self.stock, self.stockLevel, self.category, self.item, self.system, self.station, self.timestamp
		)

	def __repr__(self):
		return "ItemRecord(askingCr={}, payingCr={}, demand={}, demandLevel={}, stock={}, stockLevel={}, category=\"{}\", item=\"{}\", location=\"{} ({})\", timestamp='{}')".format(
		        self.askingCr, self.payingCr, self.demand, self.demandLevel, self.stock, self.stockLevel, re.escape(self.category), re.escape(self.item), re.escape(self.system), re.escape(self.station), self.timestamp
		)
