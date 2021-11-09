import os
import logging
import requests
from datetime import datetime


class Todoist():
    """Module for getting active tasks from todoist"""

    def __init__(self):
        pass

    def _get_api_host(self):
        """Returns the API host"""
        return 'api.todoist.com'

    def _build_tasks_url(self):
        """Builds and returns the tasks URL"""
        return f"https://{self._get_api_host()}/rest/v1/tasks"

    def _get_bearer_token(self):
        """Returns the bearer token for API requests"""
        return os.environ['TODOIST_PERSONAL_TOKEN']

    def _get_all_active_tasks(self):
        """Retrieves all active tasks from the api"""
        req_headers = {
            'Authorization': "Bearer " + self._get_bearer_token(),
        }
        url = self._build_tasks_url()
        response = requests.get(url, headers=req_headers)
        if response.status_code != 200:
            logging.error('Error retrieving tasks from API')
            return None
        return response.json()

    def _sort_tasks_by_highest_priority(self, tasks):
        """Sorts tasks by highest priority (4, 3, 2, 1)"""
        return sorted(tasks, key=lambda t: t['priority'], reverse=True)

    def _get_todoist_date_format(self):
        """Returns the todoist date format"""
        return '%Y-%m-%d'

    def _filter_tasks_due_today_or_before(self, tasks):
        """Returns only tasks that are due today or before today"""
        due_today = []
        for task in tasks:
            if not task.get('due'):
                continue
            due_date = datetime.strptime(task['due']['date'], self._get_todoist_date_format())
            if due_date <= datetime.today():
                due_today.append(task)
        return due_today

    def get_tasks(self, num_tasks=3):
        """Returns the number of tasks by highest priority and date"""
        all_tasks = self._get_all_active_tasks()
        due_today = self._filter_tasks_due_today_or_before(all_tasks)
        if not due_today:
            return None
        due_today = self._sort_tasks_by_highest_priority(due_today)
        return due_today[0:num_tasks]
