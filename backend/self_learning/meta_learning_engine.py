"""
Meta-Learning Engine for Coding Agents
Learn how to learn more effectively across different coding domains
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict, deque
import asyncio
# Legacy import removed - LlmChat not used in current implementation
import os


class LearningStrategy(Enum):
    IMITATION = "imitation"  # Learn from examples
    EXPLORATION = "exploration"  # Try new approaches
    REFINEMENT = "refinement"  # Improve existing solutions
    TRANSFER = "transfer"  # Apply knowledge from other domains
    COMPOSITION = "composition"  # Combine multiple patterns


@dataclass
class LearningExperience:
    strategy_used: LearningStrategy
    task_domain: str
    task_complexity: float
    approach_taken: str
    outcome_quality: float
    time_taken: float
    success: bool
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StrategyEffectiveness:
    strategy: LearningStrategy
    domain: str
    success_rate: float
    avg_quality: float
    avg_time: float
    sample_size: int
    confidence: float
    last_updated: datetime


class MetaLearningEngine:
    """
    Implements meta-learning to optimize learning strategies across domains
    """
    
    def __init__(self):
        self.learning_experiences = deque(maxlen=1000)  # Bounded memory
        self.strategy_effectiveness = {}  # (strategy, domain) -> StrategyEffectiveness
        self.domain_similarities = {}  # domain1 -> {domain2: similarity_score}
        self.adaptive_parameters = {
            'exploration_rate': 0.3,
            'transfer_threshold': 0.7,
            'confidence_threshold': 0.8,
            'min_samples_for_confidence': 5
        }
        self.meta_learning_cycles = 0
        
    async def recommend_learning_strategy(self, 
                                        task_domain: str, 
                                        task_complexity: float,
                                        available_examples: int = 0,
                                        time_budget: float = 60.0) -> Tuple[LearningStrategy, Dict[str, Any]]:
        """
        Recommend the best learning strategy for a given task
        """
        
        # Get strategy effectiveness for this domain
        domain_strategies = self._get_domain_strategy_effectiveness(task_domain)
        
        # Consider task characteristics
        strategy_scores = {}
        
        for strategy in LearningStrategy:
            base_score = domain_strategies.get(strategy, 0.5)  # Default neutral score
            
            # Adjust based on task characteristics
            if strategy == LearningStrategy.IMITATION:
                # Better when examples are available and task is complex
                score = base_score * (1 + 0.3 * min(available_examples / 5, 1)) * (1 + 0.2 * task_complexity)
            
            elif strategy == LearningStrategy.EXPLORATION:
                # Better for simpler tasks or when we have time
                score = base_score * (1 + 0.3 * (1 - task_complexity)) * (1 + 0.2 * min(time_budget / 120, 1))
            
            elif strategy == LearningStrategy.REFINEMENT:
                # Better when we have some experience in the domain
                domain_experience = len([exp for exp in self.learning_experiences 
                                       if exp.task_domain == task_domain])
                score = base_score * (1 + 0.4 * min(domain_experience / 10, 1))
            
            elif strategy == LearningStrategy.TRANSFER:
                # Better when we have experience in similar domains
                similar_domains = self._find_similar_domains(task_domain)
                transfer_potential = sum(self.domain_similarities.get(task_domain, {}).get(d, 0) 
                                       for d in similar_domains[:3])
                score = base_score * (1 + 0.5 * min(transfer_potential, 1))
            
            elif strategy == LearningStrategy.COMPOSITION:
                # Better for complex tasks when we have diverse experience
                diversity_score = len(set(exp.task_domain for exp in self.learning_experiences)) / 10
                score = base_score * (1 + 0.3 * task_complexity) * (1 + 0.3 * min(diversity_score, 1))
            
            strategy_scores[strategy] = score
        
        # Add exploration bonus (epsilon-greedy)
        if np.random.random() < self.adaptive_parameters['exploration_rate']:
            # Randomly select a strategy for exploration
            selected_strategy = np.random.choice(list(LearningStrategy))
        else:
            # Select best strategy
            selected_strategy = max(strategy_scores, key=strategy_scores.get)
        
        # Generate strategy-specific parameters
        strategy_params = await self._generate_strategy_parameters(
            selected_strategy, task_domain, task_complexity, time_budget
        )
        
        return selected_strategy, strategy_params
    
    def _get_domain_strategy_effectiveness(self, domain: str) -> Dict[LearningStrategy, float]:
        """Get effectiveness scores for each strategy in a domain"""
        effectiveness = {}
        
        for strategy in LearningStrategy:
            key = (strategy, domain)
            if key in self.strategy_effectiveness:
                eff = self.strategy_effectiveness[key]
                # Combine success rate and quality, weighted by confidence
                score = (eff.success_rate * 0.6 + eff.avg_quality / 100 * 0.4) * eff.confidence
                effectiveness[strategy] = score
            else:
                effectiveness[strategy] = 0.5  # Neutral default
        
        return effectiveness
    
    def _find_similar_domains(self, target_domain: str, top_k: int = 3) -> List[str]:
        """Find domains similar to the target domain"""
        if target_domain not in self.domain_similarities:
            return []
        
        similarities = self.domain_similarities[target_domain]
        sorted_domains = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        
        return [domain for domain, similarity in sorted_domains[:top_k] 
                if similarity > self.adaptive_parameters['transfer_threshold']]
    
    async def _generate_strategy_parameters(self, 
                                          strategy: LearningStrategy,
                                          domain: str,
                                          complexity: float,
                                          time_budget: float) -> Dict[str, Any]:
        """Generate parameters specific to the chosen strategy"""
        
        params = {"strategy": strategy.value}
        
        if strategy == LearningStrategy.IMITATION:
            params.update({
                "focus_on_patterns": True,
                "example_analysis_depth": "high" if complexity > 0.7 else "medium",
                "pattern_extraction_enabled": True
            })
        
        elif strategy == LearningStrategy.EXPLORATION:
            params.update({
                "creativity_boost": True,
                "alternative_approaches": max(2, int(time_budget / 30)),
                "risk_tolerance": "high" if time_budget > 90 else "medium"
            })
        
        elif strategy == LearningStrategy.REFINEMENT:
            # Find best previous approach in this domain
            domain_experiences = [exp for exp in self.learning_experiences 
                                if exp.task_domain == domain and exp.success]
            
            if domain_experiences:
                best_exp = max(domain_experiences, key=lambda x: x.outcome_quality)
                params.update({
                    "base_approach": best_exp.approach_taken,
                    "refinement_focus": "quality" if complexity > 0.6 else "speed",
                    "incremental_improvements": True
                })
        
        elif strategy == LearningStrategy.TRANSFER:
            similar_domains = self._find_similar_domains(domain)
            if similar_domains:
                # Get successful patterns from similar domains
                transfer_patterns = []
                for sim_domain in similar_domains[:2]:
                    domain_exps = [exp for exp in self.learning_experiences 
                                 if exp.task_domain == sim_domain and exp.success]
                    if domain_exps:
                        best_exp = max(domain_exps, key=lambda x: x.outcome_quality)
                        transfer_patterns.append({
                            "source_domain": sim_domain,
                            "approach": best_exp.approach_taken,
                            "quality": best_exp.outcome_quality
                        })
                
                params.update({
                    "transfer_patterns": transfer_patterns,
                    "adaptation_required": True,
                    "cross_domain_mapping": True
                })
        
        elif strategy == LearningStrategy.COMPOSITION:
            # Find diverse successful approaches to combine
            successful_approaches = []
            seen_domains = set()
            
            for exp in sorted(self.learning_experiences, key=lambda x: x.outcome_quality, reverse=True):
                if exp.success and exp.task_domain not in seen_domains and len(successful_approaches) < 3:
                    successful_approaches.append({
                        "domain": exp.task_domain,
                        "approach": exp.approach_taken,
                        "quality": exp.outcome_quality
                    })
                    seen_domains.add(exp.task_domain)
            
            params.update({
                "composition_sources": successful_approaches,
                "synthesis_required": True,
                "novelty_emphasis": True
            })
        
        return params
    
    def record_learning_outcome(self, 
                              strategy: LearningStrategy,
                              domain: str,
                              complexity: float,
                              approach: str,
                              quality: float,
                              time_taken: float,
                              success: bool,
                              context: Dict[str, Any] = None):
        """Record the outcome of a learning attempt"""
        
        experience = LearningExperience(
            strategy_used=strategy,
            task_domain=domain,
            task_complexity=complexity,
            approach_taken=approach,
            outcome_quality=quality,
            time_taken=time_taken,
            success=success,
            timestamp=datetime.now(),
            context=context or {}
        )
        
        self.learning_experiences.append(experience)
        
        # Update strategy effectiveness
        self._update_strategy_effectiveness(strategy, domain)
        
        # Update domain similarities
        asyncio.create_task(self._update_domain_similarities())
        
        # Adapt parameters based on recent performance
        self._adapt_parameters()
    
    def _update_strategy_effectiveness(self, strategy: LearningStrategy, domain: str):
        """Update effectiveness metrics for a strategy-domain combination"""
        
        key = (strategy, domain)
        
        # Get recent experiences for this strategy-domain combination
        relevant_experiences = [
            exp for exp in self.learning_experiences
            if exp.strategy_used == strategy and exp.task_domain == domain
        ]
        
        if not relevant_experiences:
            return
        
        # Calculate metrics
        success_rate = sum(1 for exp in relevant_experiences if exp.success) / len(relevant_experiences)
        avg_quality = np.mean([exp.outcome_quality for exp in relevant_experiences if exp.success])
        avg_time = np.mean([exp.time_taken for exp in relevant_experiences])
        sample_size = len(relevant_experiences)
        
        # Calculate confidence based on sample size and consistency
        confidence = min(1.0, sample_size / self.adaptive_parameters['min_samples_for_confidence'])
        if sample_size > 1:
            quality_std = np.std([exp.outcome_quality for exp in relevant_experiences if exp.success])
            consistency_factor = max(0.1, 1 - quality_std / 100)  # Lower std = higher confidence
            confidence *= consistency_factor
        
        self.strategy_effectiveness[key] = StrategyEffectiveness(
            strategy=strategy,
            domain=domain,
            success_rate=success_rate,
            avg_quality=avg_quality if not np.isnan(avg_quality) else 0,
            avg_time=avg_time,
            sample_size=sample_size,
            confidence=confidence,
            last_updated=datetime.now()
        )
    
    async def _update_domain_similarities(self):
        """Update similarities between domains based on transfer success"""
        
        # Group experiences by domain
        domain_experiences = defaultdict(list)
        for exp in self.learning_experiences:
            domain_experiences[exp.task_domain].append(exp)
        
        domains = list(domain_experiences.keys())
        
        # Calculate similarities using LLM analysis (currently disabled - using heuristic approach)
        if len(domains) >= 2:
            try:
                # Legacy LlmChat code removed - using direct similarity calculation
                similarity_chat = None
                
                # Analyze domain characteristics
                domain_characteristics = {}
                for domain in domains:
                    successful_approaches = [
                        exp.approach_taken for exp in domain_experiences[domain] 
                        if exp.success
                    ][:3]  # Top 3 successful approaches
                    
                    domain_characteristics[domain] = {
                        "successful_approaches": successful_approaches,
                        "avg_complexity": np.mean([exp.task_complexity for exp in domain_experiences[domain]]),
                        "success_rate": sum(1 for exp in domain_experiences[domain] if exp.success) / len(domain_experiences[domain])
                    }
                
                prompt = f"""Analyze similarity between these coding domains:

DOMAINS AND CHARACTERISTICS:
{json.dumps(domain_characteristics, indent=2)}

For each pair of domains, assess similarity (0.0-1.0) based on:
1. Technical approaches used
2. Problem complexity patterns
3. Success patterns
4. Transferable skills

Return JSON:
{{
  "similarities": {{
    "domain1": {{"domain2": 0.8, "domain3": 0.3}},
    "domain2": {{"domain1": 0.8, "domain3": 0.5}}
  }}
}}"""
                
                response = await similarity_chat.send_message(UserMessage(text=prompt))
                
                response_text = response.strip()
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0]
                
                similarity_data = json.loads(response_text.strip())
                self.domain_similarities = similarity_data.get('similarities', {})
                
            except Exception as e:
                print(f"Domain similarity analysis failed: {e}")
    
    def _adapt_parameters(self):
        """Adapt meta-learning parameters based on recent performance"""
        
        if len(self.learning_experiences) < 10:
            return
        
        recent_experiences = list(self.learning_experiences)[-20:]  # Last 20 experiences
        
        # Analyze exploration vs exploitation balance
        exploration_experiences = [exp for exp in recent_experiences 
                                 if exp.strategy_used == LearningStrategy.EXPLORATION]
        
        if exploration_experiences:
            exploration_success_rate = sum(1 for exp in exploration_experiences if exp.success) / len(exploration_experiences)
            
            # Adjust exploration rate based on success
            if exploration_success_rate > 0.7:
                # Exploration is working well, maintain or increase
                self.adaptive_parameters['exploration_rate'] = min(0.5, self.adaptive_parameters['exploration_rate'] * 1.1)
            elif exploration_success_rate < 0.3:
                # Exploration not working, reduce
                self.adaptive_parameters['exploration_rate'] = max(0.1, self.adaptive_parameters['exploration_rate'] * 0.9)
        
        # Analyze transfer learning effectiveness
        transfer_experiences = [exp for exp in recent_experiences 
                              if exp.strategy_used == LearningStrategy.TRANSFER]
        
        if transfer_experiences:
            transfer_success_rate = sum(1 for exp in transfer_experiences if exp.success) / len(transfer_experiences)
            
            # Adjust transfer threshold
            if transfer_success_rate > 0.8:
                # Transfer working well, can be more aggressive
                self.adaptive_parameters['transfer_threshold'] = max(0.5, self.adaptive_parameters['transfer_threshold'] * 0.95)
            elif transfer_success_rate < 0.4:
                # Transfer not working, be more conservative
                self.adaptive_parameters['transfer_threshold'] = min(0.9, self.adaptive_parameters['transfer_threshold'] * 1.05)
    
    async def generate_meta_insights(self) -> Dict[str, Any]:
        """Generate insights about the learning process itself"""
        
        if len(self.learning_experiences) < 10:
            return {"status": "insufficient_data"}
        
        insights = {}
        
        # Strategy effectiveness analysis
        strategy_performance = {}
        for strategy in LearningStrategy:
            strategy_exps = [exp for exp in self.learning_experiences if exp.strategy_used == strategy]
            if strategy_exps:
                success_rate = sum(1 for exp in strategy_exps if exp.success) / len(strategy_exps)
                avg_quality = np.mean([exp.outcome_quality for exp in strategy_exps if exp.success])
                strategy_performance[strategy.value] = {
                    "success_rate": success_rate,
                    "avg_quality": avg_quality if not np.isnan(avg_quality) else 0,
                    "usage_count": len(strategy_exps)
                }
        
        insights["strategy_performance"] = strategy_performance
        
        # Learning trajectory analysis
        recent_quality = np.mean([exp.outcome_quality for exp in list(self.learning_experiences)[-10:] if exp.success])
        early_quality = np.mean([exp.outcome_quality for exp in list(self.learning_experiences)[:10] if exp.success])
        
        insights["learning_trajectory"] = {
            "recent_avg_quality": recent_quality if not np.isnan(recent_quality) else 0,
            "early_avg_quality": early_quality if not np.isnan(early_quality) else 0,
            "improvement": recent_quality - early_quality if not (np.isnan(recent_quality) or np.isnan(early_quality)) else 0
        }
        
        # Domain mastery analysis
        domain_mastery = {}
        for domain in set(exp.task_domain for exp in self.learning_experiences):
            domain_exps = [exp for exp in self.learning_experiences if exp.task_domain == domain]
            success_rate = sum(1 for exp in domain_exps if exp.success) / len(domain_exps)
            avg_quality = np.mean([exp.outcome_quality for exp in domain_exps if exp.success])
            
            domain_mastery[domain] = {
                "success_rate": success_rate,
                "avg_quality": avg_quality if not np.isnan(avg_quality) else 0,
                "experience_count": len(domain_exps),
                "mastery_level": "expert" if success_rate > 0.8 and avg_quality > 85 else
                               "proficient" if success_rate > 0.6 and avg_quality > 70 else
                               "learning"
            }
        
        insights["domain_mastery"] = domain_mastery
        
        # Adaptive parameter status
        insights["adaptive_parameters"] = self.adaptive_parameters.copy()
        
        # Recommendations for improvement
        recommendations = []
        
        # Check if any strategy is underperforming
        for strategy, perf in strategy_performance.items():
            if perf["success_rate"] < 0.4 and perf["usage_count"] > 5:
                recommendations.append(f"Strategy '{strategy}' showing low success rate - consider parameter tuning")
        
        # Check learning trajectory
        if insights["learning_trajectory"]["improvement"] < 0:
            recommendations.append("Learning trajectory declining - consider curriculum adjustment or strategy review")
        
        # Check domain balance
        domain_counts = [perf["experience_count"] for perf in domain_mastery.values()]
        if len(domain_counts) > 1 and max(domain_counts) > 3 * min(domain_counts):
            recommendations.append("Unbalanced domain experience - consider more diverse task selection")
        
        insights["recommendations"] = recommendations
        
        return insights
    
    def get_learning_efficiency_report(self) -> Dict[str, Any]:
        """Generate a comprehensive learning efficiency report"""
        
        if not self.learning_experiences:
            return {"status": "no_data"}
        
        # Time-based analysis
        total_time = sum(exp.time_taken for exp in self.learning_experiences)
        successful_time = sum(exp.time_taken for exp in self.learning_experiences if exp.success)
        
        # Quality progression
        experiences_by_time = sorted(self.learning_experiences, key=lambda x: x.timestamp)
        quality_progression = [exp.outcome_quality for exp in experiences_by_time if exp.success]
        
        # Learning velocity (improvement per hour)
        if len(quality_progression) > 1 and total_time > 0:
            quality_improvement = quality_progression[-1] - quality_progression[0]
            learning_velocity = quality_improvement / (total_time / 60)  # per hour
        else:
            learning_velocity = 0
        
        # Strategy efficiency
        strategy_efficiency = {}
        for strategy in LearningStrategy:
            strategy_exps = [exp for exp in self.learning_experiences if exp.strategy_used == strategy]
            if strategy_exps:
                avg_time = np.mean([exp.time_taken for exp in strategy_exps])
                avg_quality = np.mean([exp.outcome_quality for exp in strategy_exps if exp.success])
                efficiency = avg_quality / avg_time if avg_time > 0 and not np.isnan(avg_quality) else 0
                strategy_efficiency[strategy.value] = efficiency
        
        return {
            "total_learning_time_minutes": total_time,
            "successful_time_minutes": successful_time,
            "time_efficiency": successful_time / total_time if total_time > 0 else 0,
            "learning_velocity_per_hour": learning_velocity,
            "quality_progression": quality_progression[-10:],  # Last 10 for visualization
            "strategy_efficiency": strategy_efficiency,
            "current_parameters": self.adaptive_parameters,
            "meta_learning_cycles": self.meta_learning_cycles
        }