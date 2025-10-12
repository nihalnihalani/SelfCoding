from typing import Dict, List, Any
from .memory_system import HierarchicalMemory
from .reflexion import ReflexionFramework
import asyncio


class SelfImprovementEngine:
    """Core self-improvement engine combining memory and reflexion."""
    
    def __init__(self):
        self.memory = HierarchicalMemory()
        self.reflexion = ReflexionFramework(self.memory)
        self.improvement_cycle_count = 0
    
    async def learn_from_generation(self, task: str, result: Dict, external_feedback: Dict = None):
        """Learn from a code generation experience."""
        
        # Store as episode
        episode = {
            'task': task,
            'result': result,
            'external_feedback': external_feedback,
            'cycle': self.improvement_cycle_count
        }
        
        importance = 0.8 if result.get('success') else 0.6
        self.memory.add_episode(episode, importance)
        
        # If feedback indicates failure, reflect deeply
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
        """Execute recursive self-improvement loop with Reflexion."""
        
        print("\n" + "="*70)
        print("🔄 RECURSIVE SELF-IMPROVEMENT CYCLE")
        print("="*70)
        
        self.improvement_cycle_count += 1
        
        # Run reflexion loop
        result = await self.reflexion.reflexion_loop(task, context, max_iterations=3)
        
        # Apply forgetting curve to memories
        self.memory.apply_forgetting_curve()
        
        # Get consolidated knowledge
        knowledge = self.memory.get_consolidated_knowledge()
        
        return {
            **result,
            'improvement_cycle': self.improvement_cycle_count,
            'memory_stats': self.memory.get_statistics(),
            'consolidated_knowledge': knowledge
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
