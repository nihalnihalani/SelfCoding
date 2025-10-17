"""
Curriculum Learning for Coding Agents
Progressively increase task complexity based on agent capabilities
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import numpy as np
from datetime import datetime, timedelta


class DifficultyLevel(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4
    RESEARCH = 5


class TaskCategory(Enum):
    UI_COMPONENTS = "ui_components"
    DATA_VISUALIZATION = "data_visualization"
    INTERACTIVE_APPS = "interactive_apps"
    ALGORITHMS = "algorithms"
    FULL_STACK = "full_stack"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    RESEARCH = "research"


@dataclass
class CurriculumTask:
    id: str
    description: str
    category: TaskCategory
    difficulty: DifficultyLevel
    prerequisites: List[str]  # Task IDs that should be mastered first
    success_criteria: Dict[str, float]  # quality_score, time_limit, etc.
    learning_objectives: List[str]
    estimated_time: int  # minutes
    
    
@dataclass
class MasteryLevel:
    task_id: str
    attempts: int
    successes: int
    best_score: float
    average_score: float
    mastery_achieved: bool
    last_attempt: datetime


class CurriculumLearningSystem:
    """
    Implements curriculum learning for progressive skill development
    """
    
    def __init__(self):
        self.curriculum = self._initialize_curriculum()
        self.mastery_levels = {}  # task_id -> MasteryLevel
        self.current_focus_areas = []
        self.mastery_threshold = 0.8  # 80% success rate with quality > 75
        
    def _initialize_curriculum(self) -> Dict[str, CurriculumTask]:
        """Initialize the learning curriculum"""
        tasks = {}
        
        # Beginner Level Tasks
        tasks["simple_button"] = CurriculumTask(
            id="simple_button",
            description="Create a simple button with hover effects",
            category=TaskCategory.UI_COMPONENTS,
            difficulty=DifficultyLevel.BEGINNER,
            prerequisites=[],
            success_criteria={"quality_score": 70, "time_limit": 30},
            learning_objectives=["Basic HTML structure", "CSS styling", "Hover effects"],
            estimated_time=5
        )
        
        tasks["basic_form"] = CurriculumTask(
            id="basic_form",
            description="Create a contact form with validation",
            category=TaskCategory.UI_COMPONENTS,
            difficulty=DifficultyLevel.BEGINNER,
            prerequisites=["simple_button"],
            success_criteria={"quality_score": 75, "time_limit": 45},
            learning_objectives=["Form elements", "Input validation", "Event handling"],
            estimated_time=10
        )
        
        tasks["todo_list"] = CurriculumTask(
            id="todo_list",
            description="Build a todo list with add/remove functionality",
            category=TaskCategory.INTERACTIVE_APPS,
            difficulty=DifficultyLevel.INTERMEDIATE,
            prerequisites=["basic_form"],
            success_criteria={"quality_score": 80, "time_limit": 60},
            learning_objectives=["DOM manipulation", "Local storage", "Array operations"],
            estimated_time=15
        )
        
        # Intermediate Level Tasks
        tasks["data_table"] = CurriculumTask(
            id="data_table",
            description="Create a sortable, filterable data table",
            category=TaskCategory.DATA_VISUALIZATION,
            difficulty=DifficultyLevel.INTERMEDIATE,
            prerequisites=["todo_list"],
            success_criteria={"quality_score": 80, "time_limit": 90},
            learning_objectives=["Table manipulation", "Sorting algorithms", "Filtering"],
            estimated_time=20
        )
        
        tasks["chart_dashboard"] = CurriculumTask(
            id="chart_dashboard",
            description="Build a dashboard with interactive charts",
            category=TaskCategory.DATA_VISUALIZATION,
            difficulty=DifficultyLevel.ADVANCED,
            prerequisites=["data_table"],
            success_criteria={"quality_score": 85, "time_limit": 120},
            learning_objectives=["Chart libraries", "Data processing", "Responsive design"],
            estimated_time=30
        )
        
        # Advanced Level Tasks
        tasks["real_time_chat"] = CurriculumTask(
            id="real_time_chat",
            description="Create a real-time chat application",
            category=TaskCategory.FULL_STACK,
            difficulty=DifficultyLevel.ADVANCED,
            prerequisites=["chart_dashboard"],
            success_criteria={"quality_score": 85, "time_limit": 180},
            learning_objectives=["WebSockets", "Real-time updates", "Message handling"],
            estimated_time=45
        )
        
        tasks["game_engine"] = CurriculumTask(
            id="game_engine",
            description="Build a simple 2D game engine with physics",
            category=TaskCategory.ALGORITHMS,
            difficulty=DifficultyLevel.EXPERT,
            prerequisites=["real_time_chat"],
            success_criteria={"quality_score": 90, "time_limit": 240},
            learning_objectives=["Game loops", "Physics simulation", "Performance optimization"],
            estimated_time=60
        )
        
        # Expert Level Tasks
        tasks["ai_code_assistant"] = CurriculumTask(
            id="ai_code_assistant",
            description="Create an AI-powered code completion tool",
            category=TaskCategory.RESEARCH,
            difficulty=DifficultyLevel.RESEARCH,
            prerequisites=["game_engine"],
            success_criteria={"quality_score": 95, "time_limit": 300},
            learning_objectives=["AI integration", "Code analysis", "Advanced algorithms"],
            estimated_time=90
        )
        
        return tasks
    
    def get_next_recommended_tasks(self, max_tasks: int = 3) -> List[CurriculumTask]:
        """Get the next recommended tasks based on current mastery"""
        available_tasks = []
        
        for task_id, task in self.curriculum.items():
            # Check if prerequisites are met
            prerequisites_met = all(
                self.is_task_mastered(prereq_id) 
                for prereq_id in task.prerequisites
            )
            
            # Check if not already mastered
            not_mastered = not self.is_task_mastered(task_id)
            
            if prerequisites_met and not_mastered:
                available_tasks.append(task)
        
        # Sort by difficulty and estimated time
        available_tasks.sort(key=lambda t: (t.difficulty.value, t.estimated_time))
        
        return available_tasks[:max_tasks]
    
    def is_task_mastered(self, task_id: str) -> bool:
        """Check if a task has been mastered"""
        if task_id not in self.mastery_levels:
            return False
        
        mastery = self.mastery_levels[task_id]
        
        # Mastery criteria: 80% success rate with average quality > 75
        success_rate = mastery.successes / mastery.attempts if mastery.attempts > 0 else 0
        
        return (success_rate >= self.mastery_threshold and 
                mastery.average_score >= 75 and 
                mastery.attempts >= 3)  # Minimum attempts for statistical significance
    
    def record_task_attempt(self, task_id: str, success: bool, quality_score: float):
        """Record the result of a task attempt"""
        if task_id not in self.mastery_levels:
            self.mastery_levels[task_id] = MasteryLevel(
                task_id=task_id,
                attempts=0,
                successes=0,
                best_score=0,
                average_score=0,
                mastery_achieved=False,
                last_attempt=datetime.now()
            )
        
        mastery = self.mastery_levels[task_id]
        mastery.attempts += 1
        
        if success:
            mastery.successes += 1
        
        mastery.best_score = max(mastery.best_score, quality_score)
        
        # Update average score
        if mastery.attempts == 1:
            mastery.average_score = quality_score
        else:
            # Exponential moving average for recent performance
            alpha = 0.3
            mastery.average_score = alpha * quality_score + (1 - alpha) * mastery.average_score
        
        mastery.last_attempt = datetime.now()
        mastery.mastery_achieved = self.is_task_mastered(task_id)
        
        # Update focus areas based on performance
        self._update_focus_areas()
    
    def _update_focus_areas(self):
        """Update current focus areas based on performance patterns"""
        self.current_focus_areas = []
        
        # Identify struggling areas
        for task_id, mastery in self.mastery_levels.items():
            if mastery.attempts >= 3 and not mastery.mastery_achieved:
                task = self.curriculum[task_id]
                if task.category not in self.current_focus_areas:
                    self.current_focus_areas.append(task.category)
        
        # If no struggling areas, focus on next difficulty level
        if not self.current_focus_areas:
            mastered_difficulties = set()
            for task_id, mastery in self.mastery_levels.items():
                if mastery.mastery_achieved:
                    task = self.curriculum[task_id]
                    mastered_difficulties.add(task.difficulty)
            
            if mastered_difficulties:
                next_difficulty = max(mastered_difficulties).value + 1
                if next_difficulty <= DifficultyLevel.RESEARCH.value:
                    # Focus on categories at the next difficulty level
                    for task in self.curriculum.values():
                        if task.difficulty.value == next_difficulty:
                            if task.category not in self.current_focus_areas:
                                self.current_focus_areas.append(task.category)
    
    def get_adaptive_task_suggestion(self, recent_performance: List[Dict]) -> Optional[str]:
        """
        Suggest a task based on recent performance and learning theory
        """
        if not recent_performance:
            # Start with beginner tasks
            beginner_tasks = [t for t in self.curriculum.values() 
                            if t.difficulty == DifficultyLevel.BEGINNER and not t.prerequisites]
            return beginner_tasks[0].description if beginner_tasks else None
        
        # Analyze recent performance
        recent_success_rate = sum(1 for p in recent_performance[-5:] if p.get('success', False)) / min(5, len(recent_performance))
        recent_avg_quality = np.mean([p.get('quality_score', 0) for p in recent_performance[-5:]])
        
        # Adaptive difficulty adjustment
        if recent_success_rate > 0.8 and recent_avg_quality > 80:
            # Performing well - increase difficulty
            recommended_tasks = self.get_next_recommended_tasks(1)
            if recommended_tasks:
                return recommended_tasks[0].description
        elif recent_success_rate < 0.4 or recent_avg_quality < 60:
            # Struggling - suggest easier tasks or review
            current_level = self._get_current_difficulty_level()
            if current_level.value > 1:
                easier_tasks = [t for t in self.curriculum.values() 
                              if t.difficulty.value == current_level.value - 1 
                              and not self.is_task_mastered(t.id)]
                if easier_tasks:
                    return f"Review: {easier_tasks[0].description}"
        
        # Normal progression
        recommended_tasks = self.get_next_recommended_tasks(1)
        return recommended_tasks[0].description if recommended_tasks else None
    
    def _get_current_difficulty_level(self) -> DifficultyLevel:
        """Determine current difficulty level based on mastered tasks"""
        mastered_levels = []
        for task_id, mastery in self.mastery_levels.items():
            if mastery.mastery_achieved:
                task = self.curriculum[task_id]
                mastered_levels.append(task.difficulty.value)
        
        if not mastered_levels:
            return DifficultyLevel.BEGINNER
        
        max_mastered = max(mastered_levels)
        return DifficultyLevel(max_mastered)
    
    def generate_personalized_curriculum(self, time_budget_minutes: int = 60) -> List[CurriculumTask]:
        """Generate a personalized curriculum for the given time budget"""
        recommended_tasks = self.get_next_recommended_tasks(10)
        
        # Select tasks that fit within time budget
        selected_tasks = []
        total_time = 0
        
        for task in recommended_tasks:
            if total_time + task.estimated_time <= time_budget_minutes:
                selected_tasks.append(task)
                total_time += task.estimated_time
            
            if total_time >= time_budget_minutes * 0.8:  # Use 80% of budget
                break
        
        return selected_tasks
    
    def get_learning_analytics(self) -> Dict:
        """Get comprehensive learning analytics"""
        if not self.mastery_levels:
            return {"status": "no_data"}
        
        # Overall statistics
        total_tasks_attempted = len(self.mastery_levels)
        mastered_tasks = sum(1 for m in self.mastery_levels.values() if m.mastery_achieved)
        total_attempts = sum(m.attempts for m in self.mastery_levels.values())
        total_successes = sum(m.successes for m in self.mastery_levels.values())
        
        # Performance by category
        category_performance = {}
        for task_id, mastery in self.mastery_levels.items():
            task = self.curriculum[task_id]
            category = task.category.value
            
            if category not in category_performance:
                category_performance[category] = {
                    'attempts': 0,
                    'successes': 0,
                    'avg_quality': 0,
                    'mastered_tasks': 0,
                    'total_tasks': 0
                }
            
            category_performance[category]['attempts'] += mastery.attempts
            category_performance[category]['successes'] += mastery.successes
            category_performance[category]['avg_quality'] += mastery.average_score
            category_performance[category]['total_tasks'] += 1
            
            if mastery.mastery_achieved:
                category_performance[category]['mastered_tasks'] += 1
        
        # Calculate averages
        for category in category_performance:
            perf = category_performance[category]
            perf['success_rate'] = perf['successes'] / perf['attempts'] if perf['attempts'] > 0 else 0
            perf['avg_quality'] = perf['avg_quality'] / perf['total_tasks'] if perf['total_tasks'] > 0 else 0
            perf['mastery_rate'] = perf['mastered_tasks'] / perf['total_tasks'] if perf['total_tasks'] > 0 else 0
        
        # Learning velocity (tasks mastered per week)
        if self.mastery_levels:
            earliest_attempt = min(m.last_attempt for m in self.mastery_levels.values())
            weeks_learning = max(1, (datetime.now() - earliest_attempt).days / 7)
            learning_velocity = mastered_tasks / weeks_learning
        else:
            learning_velocity = 0
        
        return {
            "total_tasks_attempted": total_tasks_attempted,
            "mastered_tasks": mastered_tasks,
            "mastery_rate": mastered_tasks / total_tasks_attempted if total_tasks_attempted > 0 else 0,
            "overall_success_rate": total_successes / total_attempts if total_attempts > 0 else 0,
            "current_difficulty_level": self._get_current_difficulty_level().name,
            "focus_areas": [area.value for area in self.current_focus_areas],
            "learning_velocity_per_week": learning_velocity,
            "category_performance": category_performance,
            "next_recommended_tasks": [
                {
                    "id": task.id,
                    "description": task.description,
                    "difficulty": task.difficulty.name,
                    "estimated_time": task.estimated_time
                }
                for task in self.get_next_recommended_tasks(3)
            ]
        }