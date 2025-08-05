"""
Task Coordinator - Manages task distribution and workflow
Orchestrates complex multi-agent workflows
"""

from datetime import datetime
import json
from os import name


class TaskCoordinator:
    def get_next_tasks(self, project_id):
        """Alias for get_next_task to match expected interface (returns next tasks for a project)"""
        return self.get_next_task(project_id)
    def __init__(self, message_hub):
        self.message_hub = message_hub
        self.active_projects = {}  # Store all active projects
        self.task_templates = {
            'content_creation': [
                {'agent': 'researcher', 'task': 'research_topic', 'dependencies': []},
                {'agent': 'writer', 'task': 'create_content', 'dependencies': ['research_topic']},
                {'agent': 'critic', 'task': 'review_content', 'dependencies': ['create_content']},
                {'agent': 'writer', 'task': 'revise_content', 'dependencies': ['review_content']}
            ],
            'market_analysis': [
                {'agent': 'researcher', 'task': 'gather_market_data', 'dependencies': []},
                {'agent': 'analyst', 'task': 'analyze_data', 'dependencies': ['gather_market_data']},
                {'agent': 'writer', 'task': 'create_report', 'dependencies': ['analyze_data']},
                {'agent': 'critic', 'task': 'review_report', 'dependencies': ['create_report']}
            ],
            'competitive_research': [
                {'agent': 'researcher', 'task': 'competitor_analysis', 'dependencies': []},
                {'agent': 'analyst', 'task': 'competitive_insights', 'dependencies': ['competitor_analysis']},
                {'agent': 'writer', 'task': 'strategy_document', 'dependencies': ['competitive_insights']},
                {'agent': 'critic', 'task': 'final_review', 'dependencies': ['strategy_document']}
            ]
        }

    def create_project(self, project_name, project_type, requirements):
        """Create a new multi-agent project"""
        project_id = f"proj_{len(self.active_projects) + 1}"
        if project_type not in self.task_templates:
            return None, f"Unknown project type: {project_type}"
        
        tasks = self.task_templates[project_type].copy()


        for task in tasks:
            task['status'] = 'pending'
            task['assigned_at'] = None
            task['completed_at'] = None
            task['result'] = None
            task['requirements'] = requirements
        
        project = {
            'id': project_id,
            'name': project_name,
            'type': project_type,
            'requirements': requirements,
            'tasks': tasks,
            'status': 'created',
            'created_at': datetime.now().isoformat(),
            'thread_id': None
        }

        self.active_projects[project_id] = project


        # Create conversation thread for project
        participants = list(set([task['agent'] for task in tasks] + ['manager']))
        thread_id = self.message_hub.create_conversation_thread(project_name, participants)
        project['thread_id'] = thread_id

        return project_id, 'Project created successfully'
    
    def get_next_task(self, project_id):
        """Get the next task to be executed in the project"""
        if project_id not in self.active_projects:
            return []
        project = self.active_projects[project_id]
        next_tasks = []

        for task in project['tasks']:
            if task['status'] == 'pending':
                dependencies_met = True
                for dep_task_name in task['dependencies']:
                    dep_task = next((t for t in project['tasks'] if t['task'] == dep_task_name), None)
                    if not dep_task or dep_task['status'] != 'completed':
                        dependencies_met = False
                        break
                if dependencies_met:
                    next_tasks.append(task)

        return next_tasks

    def assign_task(self, project_id, task_name, agent_name):
        """Assign a task to an agent"""
        if project_id not in self.active_projects:
            return False, 'Project not found'
        
        project = self.active_projects[project_id]
        task = next((t for t in project['tasks'] if t['task'] == task_name), None)

        if not task:
            return False, 'Task not found'
        
        if task['status'] != 'pending':
            return False, f"Task status is {task['status']}, cannot assign"
        
        # Check dependencies
        for dep_task_name in task['dependencies']:
            dep_task = next((t for t in project['tasks'] if t['task'] == dep_task_name), None)
            if not dep_task or dep_task['status'] != 'completed':
                return False, f"Dependencies not met for task {task_name}"
            
        
        # Assign task
        task['status'] = 'assigned'
        task['agent'] = agent_name
        task['assigned_at'] = datetime.now().isoformat()
        
        # Send message to agent
        message_content = {
            'project_id': project_id,
            'task_name': task_name,
            'requirements': task['requirements'],
            'dependencies_data': self._get_dependency_results(project, task['dependencies'])
        }

        self.message_hub.send_message('coordinator',agent_name,'task_assignment',message_content)
        return True, "Task assigned successfully"
    

    def complete_task(self, project_id, task_name, result):
        """Mark a task as completed and store the result"""
        if project_id not in self.active_projects:
            return False, 'Project not found'
        
        project = self.active_projects[project_id]
        task = next((t for t in project['tasks'] if t['task'] == task_name), None)

        if not task:
            return False, 'Task not found'
        if task['status'] != 'assigned':
            return False, f"Task status is {task['status']}, cannot complete"
        
        # Mark task as completed
        task['status'] = 'completed'
        task['completed_at'] = datetime.now().isoformat()
        task['result'] = result

        # Post to project thread
        self.message_hub.post_to_thread(
            project['thread_id'],
            task['agent'],
            f'Completed task: {task_name}\nResult: {result[:200]}...'
        )

        # Check if project is complete
        all_completed = all(task['status'] == 'completed' for task in project['tasks'])
        if all_completed:
            project['status'] = 'completed'
            project['completed_at'] = datetime.now().isoformat()

        return True, "Task completed successfully"
    
    def _get_dependency_results(self, project, dependencies):
        """Get results from completed dependency tasks"""
        results = {}
        for dep_task_name in dependencies:
            dep_task_name = next((t for t in project['tasks'] if t['task'] == dep_task_name), None)
            if dep_task_name and dep_task_name['status'] == 'completed':
                results[dep_task_name['task']] = dep_task_name['result']
        return results
    
    def get_project_status(self, project_id):
        """Get the status of a project"""
        if project_id not in self.active_projects:
            return None, 'Project not found'

        project = self.active_projects[project_id]

        # Calculate progress
        total_tasks = len(project['tasks'])
        completed_tasks = len([t for t in project['tasks'] if t['status'] == 'completed'])
        progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        return {
            'project_id': project_id,
            'name': project['name'],
            'type': project['type'],
            'status': project['status'],
            'progress': f"{progress:.1f}%",
            'tasks_completed': f"{completed_tasks}/{total_tasks}",
            'next_tasks': [t['task'] for t in self.get_next_tasks(project_id)]
        }
    
    def get_all_projects_status(self):
        """Get status of all active projects"""
        return [self.get_project_status(pid) for pid in self.active_projects.keys()]