"""This modules provides classes for watering."""

import logging
import queue
import threading
import time
from collections import namedtuple

import plant

__author__ = 'pgradot'


WateringDemand = namedtuple('WateringDemand', ['timestamp', 'uid'])
'''Represent a watering demand.'''


def create_watering_demand(uid: str):
    """A factory method to create a watering demand with the current time
    as the timestamp of the demand.
    """
    return WateringDemand(time.time(), uid)

# TODO create watering planner for planned-watering plants


class Sprinkler:
    """A Sprinkler is responsible for watering plants."""
    def __init__(self, plants):
        self.listeners = list()
        self._queue = queue.Queue()
        self._plants = plants

    def post(self, demand: WateringDemand):
        """Post a demand that the sprinkler will then consume."""
        self._queue.put(demand)

    def process_event(self, event):
        """Process a monitoring event and decide if a plant needs to be watered.

        This method is meant to turn Sprinkler into a listener for
        MonitoringAggregator.

        :param event: a event
        :type event: monitoring.MonitoringEvent
        """
        # Find the plant in the list
        plant_ = None
        for plant_ in self._plants:
            if plant_.uid == event.uid and plant_.watering == plant.WateringMethod.conditional:
                plant_ = plant_
                break

        # Process event if the plant has conditional watering method
        if plant_ is not None:
            if event.temperature is not None and event.temperature >= 25:
                # It's hot out there, the plant needs more water!
                if event.humidity <= 60:
                    demand = create_watering_demand(plant_.uid)
                    self.post(demand)

            else:
                if event.humidity <= 50:
                    demand = create_watering_demand(plant_.uid)
                    self.post(demand)

    def start(self):
        """Start the sprinkler's thread and start processing demands."""
        aggregator_thread = threading.Thread(target=self._process_demands, name=self.__class__.__name__ + 'thread')
        aggregator_thread.start()

    def _process_demands(self):
        """Get demands from the queue and process them.

        For the moment, the sprinkler just broadcasts to its listeners.
        """
        while True:
            # Retrieve demand
            demand = self._queue.get()
            logging.info('%s: demand %s', self.__class__.__name__, demand)

            for listener in self.listeners:
                listener.process_demand(demand)

            # TODO water plants

            # Release queue
            self._queue.task_done()
