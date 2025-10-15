from typing import Dict, List, Any, Optional
from datetime import datetime
from .memory_system import HierarchicalMemory
from .reflexion import ReflexionFramework
from .advanced_reflexion import AdvancedReflexionFramework
from .curriculum_learning import CurriculumLearningSystem
from .meta_learning_engine import MetaLearningEngine, LearningStrategy
import asyncio


class SelfImprovementEngine:
    """
    Enhanced self-improvement engine with advanced research-backed techniques:
    - Advanced Reflexion with multi-level analysis
    - Curriculum Learning for progressive skill development
    - Meta-Learning for strategy optimization
    """
    
    def __init__(self):
        self.memory = HierarchicalMemory()
        self.reflexion = ReflexionFramework(self.memory)
        self.advanced_reflexion = AdvancedReflexionFramework(self.memory)
        self.curriculum = CurriculumLearningSystem()
        self.meta_learner = MetaLearningEngine()
        self.improvement_cycle_count = 0
    
    async def learn_from_generation(self, task: str, result: Dict, external_feedback: Dict = None):
        """Enhanced learning from code generation with advanced techniques."""
        
        # Store as episode
        episode = {
            'task': task,
            'result': result,
            'external_feedback': external_feedback,
            'cycle': self.improvement_cycle_count
        }
        
        importance = 0.8 if result.get('success') else 0.6
        self.memory.add_episode(episode, importance)
        
        # Advanced multi-level reflection
        performance_data = {
            'success': result.get('success', False),
            'quality_score': result.get('metadata', {}).get('quality_score', 0),
            'time_taken': result.get('time_taken', 0),
            'error': result.get('error')
        }
        
        insights = await self.advanced_reflexion.deep_reflection_cycle(
            task_context={'description': task, 'approach': 'standard'},
            performance_data=performance_data,
            external_feedback=external_feedback
        )
        
        # Update curriculum learning
        task_category = self._categorize_task(task)
        complexity = self._estimate_task_complexity(task)
        
        self.curriculum.record_task_attempt(
            task_id=f"{task_category}_{hash(task) % 1000}",
            success=result.get('success', False),
            quality_score=performance_data['quality_score']
        )
        
        # Record meta-learning experience
        strategy_used = self._infer_strategy_used(result)
        self.meta_learner.record_learning_outcome(
            strategy=strategy_used,
            domain=task_category,
            complexity=complexity,
            approach=result.get('approach', 'unknown'),
            quality=performance_data['quality_score'],
            time_taken=performance_data['time_taken'],
            success=result.get('success', False),
            context={'insights_generated': len(insights)}
        )
        
        # If feedback indicates failure, conduct deeper analysis
        if external_feedback and not external_feedback.get('success'):
            await self._deep_reflection_on_failure(task, result, external_feedback)
    
    async def _deep_reflection_on_failure(self, task: str, result: Dict, feedback: Dict):
        """Conduct deep reflection when generation fails."""
        
        reflection = {
            'type': 'failure_analysis',
            'task': task,
            'error': feedback.get('error'),
            'hypothesis': self._hypothesize_cause(feedback),
            'proposed_solution': self._propose_solution(feedback)
        }
        
        self.memory.add_reflection(reflection, importance=0.9)
    
    def _hypothesize_cause(self, feedback: Dict) -> str:
        """Hypothesize why generation failed."""
        error = feedback.get('error', '')
        
        if 'syntax' in error.lower():
            return "Syntax error suggests incomplete code generation or malformed output"
        elif 'undefined' in error.lower():
            return "Undefined variable suggests missing declarations or scope issues"
        elif 'timeout' in error.lower():
            return "Timeout suggests infinite loops or inefficient algorithms"
        else:
            return "Unknown error pattern - requires deeper analysis"
    
    def _propose_solution(self, feedback: Dict) -> List[str]:
        """Propose solutions based on failure analysis."""
        error = feedback.get('error', '')
        solutions = []
        
        if 'syntax' in error.lower():
            solutions.append("Add explicit validation of generated code structure")
            solutions.append("Use more structured prompts with clear formatting requirements")
        
        if 'undefined' in error.lower():
            solutions.append("Ensure all variables are declared before use")
            solutions.append("Add explicit scope checking in code generation")
        
        solutions.append("Increase code review scrutiny")
        
        return solutions
    
    async def recursive_self_improvement(self, task: str, context: Dict = None) -> Dict:
        """Enhanced recursive self-improvement with advanced techniques."""
        
        print("\n" + "="*70)
        print("🧠 ADVANCED SELF-IMPROVEMENT CYCLE")
        print("="*70)
        
        self.improvement_cycle_count += 1
        
        # Get optimal learning strategy from meta-learner
        task_domain = self._categorize_task(task)
        task_complexity = self._estimate_task_complexity(task)
        available_examples = len(self._get_similar_patterns(task))
        
        strategy, strategy_params = await self.meta_learner.recommend_learning_strategy(
            task_domain=task_domain,
            task_complexity=task_complexity,
            available_examples=available_examples,
            time_budget=context.get('time_budget', 60) if context else 60
        )
        
        print(f"📋 Recommended Strategy: {strategy.value}")
        print(f"🎯 Strategy Parameters: {strategy_params}")
        
        # Apply curriculum-guided task selection if needed
        if context and context.get('adaptive_curriculum', False):
            recommended_tasks = self.curriculum.get_next_recommended_tasks(3)
            if recommended_tasks:
                print(f"📚 Curriculum Recommendations: {[t.description for t in recommended_tasks]}")
        
        # Run enhanced reflexion loop with strategy guidance
        enhanced_context = {
            **(context or {}),
            'learning_strategy': strategy.value,
            'strategy_params': strategy_params,
            'curriculum_level': self.curriculum._get_current_difficulty_level().name
        }
        
        result = await self.reflexion.reflexion_loop(task, enhanced_context, max_iterations=3)
        
        # Apply forgetting curve to memories
        self.memory.apply_forgetting_curve()
        
        # Get consolidated knowledge
        knowledge = self.memory.get_consolidated_knowledge()
        
        # Generate meta-insights
        meta_insights = await self.meta_learner.generate_meta_insights()
        
        # Get curriculum analytics
        curriculum_analytics = self.curriculum.get_learning_analytics()
        
        # Get advanced reflection summary
        reflection_summary = self.advanced_reflexion.get_reflection_summary()
        
        return {
            **result,
            'improvement_cycle': self.improvement_cycle_count,
            'memory_stats': self.memory.get_statistics(),
            'consolidated_knowledge': knowledge,
            'learning_strategy_used': strategy.value,
            'strategy_params': strategy_params,
            'meta_insights': meta_insights,
            'curriculum_analytics': curriculum_analytics,
            'reflection_summary': reflection_summary,
            'learning_efficiency': self.meta_learner.get_learning_efficiency_report()
        }
    
    def get_learning_report(self) -> Dict:
        """Generate comprehensive learning report."""
        stats = self.memory.get_statistics()
        knowledge = self.memory.get_consolidated_knowledge()
        
        return {
            'improvement_cycles_completed': self.improvement_cycle_count,
            'memory_statistics': stats,
            'consolidated_knowledge': knowledge,
            'learning_efficiency': self._calculate_learning_efficiency(),
            'recommendations': self._generate_recommendations()
        }
    
    def _calculate_learning_efficiency(self) -> Dict:
        """Calculate how efficiently the agent is learning."""
        history = self.memory.performance_history
        
        if len(history) < 5:
            return {'status': 'insufficient_data'}
        
        # Compare first 5 vs last 5
        early_scores = [h.get('quality_score', 0) for h in history[:5] if h.get('quality_score')]
        recent_scores = [h.get('quality_score', 0) for h in history[-5:] if h.get('quality_score')]
        
        if not early_scores or not recent_scores:
            return {'status': 'insufficient_data'}
        
        early_avg = sum(early_scores) / len(early_scores)
        recent_avg = sum(recent_scores) / len(recent_scores)
        improvement = recent_avg - early_avg
        
        return {
            'early_average': early_avg,
            'recent_average': recent_avg,
            'improvement': improvement,
            'learning_rate': improvement / len(history),
            'status': 'improving' if improvement > 0 else 'needs_attention'
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for improvement."""
        recommendations = []
        efficiency = self._calculate_learning_efficiency()
        
        if efficiency.get('status') == 'needs_attention':
            recommendations.append("Consider adjusting learning parameters")
            recommendations.append("Review recent reflections for recurring issues")
        
        stats = self.memory.get_statistics()
        if stats['success_rate'] < 0.7:
            recommendations.append("Success rate below 70% - increase validation rigor")
        
        if len(self.memory.reflective) < 5:
            recommendations.append("Insufficient reflective insights - increase reflection depth")
        
        return recommendations if recommendations else ["System performing well - continue current strategy"]
    def _categorize_task(self, task: str) -> str:
        """Categorize task into domain for curriculum and meta-learning."""
        task_lower = task.lower()
        
        if any(word in task_lower for word in ['button', 'form', 'input', 'ui', 'component']):
            return 'ui_components'
        elif any(word in task_lower for word in ['chart', 'graph', 'data', 'visualization', 'dashboard']):
            return 'data_visualization'
        elif any(word in task_lower for word in ['todo', 'app', 'interactive', 'game', 'calculator']):
            return 'interactive_apps'
        elif any(word in task_lower for word in ['algorithm', 'sort', 'search', 'optimization']):
            return 'algorithms'
        elif any(word in task_lower for word in ['api', 'backend', 'database', 'server']):
            return 'full_stack'
        else:
            return 'general'
    
    def _estimate_task_complexity(self, task: str) -> float:
        """Estimate task complexity (0.0-1.0) based on description."""
        complexity_indicators = {
            'simple': 0.2, 'basic': 0.3, 'standard': 0.5, 'advanced': 0.7, 'complex': 0.8,
            'real-time': 0.8, 'interactive': 0.6, 'responsive': 0.6, 'animated': 0.7,
            'dashboard': 0.7, 'full-stack': 0.9, 'ai': 0.9, 'machine learning': 1.0
        }
        
        task_lower = task.lower()
        max_complexity = 0.3  # Base complexity
        
        for indicator, complexity in complexity_indicators.items():
            if indicator in task_lower:
                max_complexity = max(max_complexity, complexity)
        
        # Adjust based on task length (longer descriptions often indicate complexity)
        length_factor = min(0.3, len(task.split()) / 50)
        
        return min(1.0, max_complexity + length_factor)
    
    def _infer_strategy_used(self, result: Dict) -> LearningStrategy:
        """Infer which learning strategy was likely used based on result characteristics."""
        
        # Check if patterns were reused (imitation)
        if result.get('patterns_used', 0) > 0:
            return LearningStrategy.IMITATION
        
        # Check if it was a refinement of existing approach
        if result.get('metadata', {}).get('approach') == 'refinement':
            return LearningStrategy.REFINEMENT
        
        # Check if transfer learning was used
        if result.get('metadata', {}).get('transfer_learning', False):
            return LearningStrategy.TRANSFER
        
        # Check if multiple patterns were combined
        if result.get('metadata', {}).get('patterns_combined', 0) > 1:
            return LearningStrategy.COMPOSITION
        
        # Default to exploration for novel approaches
        return LearningStrategy.EXPLORATION
    
    def _get_similar_patterns(self, task: str) -> List[Dict]:
        """Get similar patterns from memory for the task."""
        # This would integrate with the existing pattern retrieval system
        # For now, return empty list as placeholder
        return []
    
    async def get_adaptive_task_suggestion(self) -> Optional[str]:
        """Get an adaptive task suggestion based on curriculum and performance."""
        
        # Get recent performance for meta-learning context
        recent_performance = self.memory.performance_history[-10:] if self.memory.performance_history else []
        
        # Get curriculum-based suggestion
        curriculum_suggestion = self.curriculum.get_adaptive_task_suggestion(recent_performance)
        
        if curriculum_suggestion:
            return curriculum_suggestion
        
        # Fallback to meta-learning suggestion
        if recent_performance:
            # Analyze what domains need work
            domain_performance = {}
            for perf in recent_performance:
                domain = self._categorize_task(perf.get('description', ''))
                if domain not in domain_performance:
                    domain_performance[domain] = []
                domain_performance[domain].append(perf.get('quality_score', 0))
            
            # Find domain with lowest average performance
            worst_domain = min(domain_performance.items(), 
                             key=lambda x: sum(x[1]) / len(x[1]) if x[1] else 0)
            
            # Suggest a task in that domain
            domain_tasks = {
                'ui_components': "Create a modern card component with animations",
                'data_visualization': "Build an interactive bar chart with tooltips",
                'interactive_apps': "Create a memory game with scoring",
                'algorithms': "Implement a sorting visualizer",
                'full_stack': "Build a simple REST API with database",
                'general': "Create a responsive landing page"
            }
            
            return domain_tasks.get(worst_domain[0], "Create a simple interactive web application")
        
        return None
    
    async def generate_comprehensive_learning_report(self) -> Dict:
        """Generate a comprehensive report on learning progress and insights."""
        
        # Get all component reports
        memory_stats = self.memory.get_statistics()
        curriculum_analytics = self.curriculum.get_learning_analytics()
        meta_insights = await self.meta_learner.generate_meta_insights()
        reflection_summary = self.advanced_reflexion.get_reflection_summary()
        efficiency_report = self.meta_learner.get_learning_efficiency_report()
        
        # Calculate overall learning score
        overall_score = 0
        score_components = []
        
        if curriculum_analytics.get('mastery_rate'):
            mastery_component = curriculum_analytics['mastery_rate'] * 30
            overall_score += mastery_component
            score_components.append(f"Curriculum Mastery: {mastery_component:.1f}/30")
        
        if memory_stats.get('success_rate'):
            memory_component = memory_stats['success_rate'] * 25
            overall_score += memory_component
            score_components.append(f"Memory Performance: {memory_component:.1f}/25")
        
        if reflection_summary.get('average_confidence'):
            reflection_component = reflection_summary['average_confidence'] * 20
            overall_score += reflection_component
            score_components.append(f"Reflection Quality: {reflection_component:.1f}/20")
        
        if efficiency_report.get('learning_velocity_per_hour', 0) > 0:
            velocity_component = min(25, efficiency_report['learning_velocity_per_hour'] * 5)
            overall_score += velocity_component
            score_components.append(f"Learning Velocity: {velocity_component:.1f}/25")
        
        # Generate recommendations
        recommendations = []
        
        if overall_score < 50:
            recommendations.append("Focus on completing more curriculum tasks to build foundational skills")
        
        if curriculum_analytics.get('mastery_rate', 0) < 0.3:
            recommendations.append("Spend more time on each task to achieve mastery before moving on")
        
        if reflection_summary.get('average_confidence', 0) < 0.7:
            recommendations.append("Increase reflection depth and evidence gathering")
        
        if efficiency_report.get('time_efficiency', 0) < 0.6:
            recommendations.append("Focus on time management and efficient learning strategies")
        
        # Get next suggested task
        next_task = await self.get_adaptive_task_suggestion()
        
        return {
            "overall_learning_score": overall_score,
            "score_breakdown": score_components,
            "improvement_cycles_completed": self.improvement_cycle_count,
            "memory_statistics": memory_stats,
            "curriculum_progress": curriculum_analytics,
            "meta_learning_insights": meta_insights,
            "reflection_quality": reflection_summary,
            "learning_efficiency": efficiency_report,
            "recommendations": recommendations,
            "next_suggested_task": next_task,
            "learning_trajectory": "improving" if overall_score > 60 else "developing",
            "generated_at": datetime.now().isoformat()
        }