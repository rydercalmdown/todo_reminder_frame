import os
import time
import logging
from paper_controller import PaperController
from todoist import Todoist


class ToDoDisplay():
    """Class for running the to do display application"""

    def __init__(self):
        self.pc = PaperController()
        self.td = Todoist()
        self._set_defaults()

    def _set_defaults(self):
        """Set defaults for the application"""
        self.update_every_x_seconds = 60
        self.latest_task = {}

    def _get_latest_task(self):
        """Get the latest task from todoist"""
        logging.info('Getting latest task')
        return self.td.get_tasks(1)[0]

    def _update_display(self, task):
        """Updates the display with the latest task"""
        logging.info('Updating display with latest task')
        self.pc.display_title(task['content'], task['description'])

    def _tick(self):
        """Runs the code for updating the display"""
        logging.info('Checking for updates')
        latest_task = self._get_latest_task()
        logging.debug(latest_task)
        if latest_task == self.latest_task:
            logging.info('No changes for latest task')
            return
        logging.info('Latest task has changed')
        self.latest_task = latest_task
        self._update_display(latest_task)
        logging.info('Task updated on display')

    def run(self):
        """Run the display"""
        logging.info('Running display')
        while True:
            self._tick()
            time.sleep(self.update_every_x_seconds)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        logging.info('Starting display')
        tdd = ToDoDisplay()
        tdd.run()
    except KeyboardInterrupt:    
        logging.info('Exiting')
