#! /usr/bin/env python
#---------------------------------------------------------------------
# Copyright (C) Oliver 'kfsone' Smith 2014 <oliver@kfs.org>:
#  You are free to use, redistribute, or even print and eat a copy of
#  this software so long as you include this copyright notice.
#  I guarantee there is at least one bug neither of us knew about.
#---------------------------------------------------------------------
# Elite Market Data Net :: Modules :: Main Module

"""
	"Elite Market Data Net" (EMDN) is a ZeroMQ based service that
	provides a near-realtime feed of market scrapes from the Elite
	Dangerous universe. This feed is called the "firehose".

	emdn.ItemRecord class encapsulates a record as described by
	the EMDN network.

	emdn.Firehose class encapsulates a connection to retrieve
	ItemRecords in an iterative fashion.

	Example:

	  from emdn.firehose import Firehose
	  firehose = Firehose()
	  # use firehose = Firehose(ctx=ctx) if you have your own zmq.Context

	  # wait upto 10 seconds and retrieve upto 2 records:
	  for itemRec in firehose.drink(records=2, timeout=10.0)
	  	pass

	  # print everything else we receive
	  for itemRec in firehose.drink():
	  	print(itemRec)
"""

try:
    import zmq
except ImportError:
    raise ImportError("This module requires the ZeroMQ library to be installed. The easiest way to obtain this is to type: pip install pyzmq")

import time

try: from itemrecord import ItemRecord
except ImportError: from . itemrecord import ItemRecord

class Firehose(object):
	"""
		Encapsulates a connection to the Elite Market Data Network (EMDN)
		live feed of price updates.
	"""

	defaultURI = 'tcp://firehose.elite-market-data.net:9050'

	def __init__(self, uri=None, ctx=None):
		self.__uri = uri or Firehose.defaultURI

		# All ZMQ operations are done through a Context,
		# so use one we're given or create one for ourselves.
		self.__ctx = ctx or zmq.Context()

		# EMDN is using the pub/sub model, a bit overzealously,
		# so we need a subscriber socket subscribed to nothing.
		self.__socket = self.__ctx.socket(zmq.SUB)
		self.__socket.setsockopt(zmq.SUBSCRIBE, ''.encode())
		self.__socket.connect(self.__uri)


	def drink(self, records=None, timeout=None, burst=False):
		"""
			Drink from the firehose, yielding the data we retrieve as ItemRecords.

			Keyword arguments:
			records -- maximum number of records to yield before exiting. Default, 0, is unlimited.
			timeout -- maximum total time to wait for data.
			burst   -- set True to stop after the first set of records are retrieved.

			e.g.
			  drink(records=50, timeout=300)
			    Reads until we have received 50 seconds or 300 seconds have passed.

			  drink(records=50, timeout=10.5, burst=True)
			    Reads until the first of:
			      50 records have been received,
			      10.5 seconds has elapsed,
			      the first burst of data has been drained.
		"""

		if self.__socket.closed:
			raise BrokenPipeError("Firehose socket is closed")

		socket = self.__socket
		maxPollDuration = timeout
		recordsRemaining = records or 1
		recordCost = 1 if records else 0

		if timeout:
			cutoffTime = time.clock() + timeout

		while recordsRemaining:
			if timeout:
				maxPollDuration = (cutoffTime - time.clock()) * 1000
				if maxPollDuration <= 0:
					return
			if socket.poll(timeout=maxPollDuration):
				while recordsRemaining:
					try:
						csv = socket.recv_string(zmq.NOBLOCK)
					except zmq.error.Again:
						break
					yield ItemRecord(*(csv.split(',')))
					recordsRemaining -= recordCost
				if burst:
					return

