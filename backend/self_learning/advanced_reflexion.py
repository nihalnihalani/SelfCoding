"""
Advanced Reflexion Framework with Research-Backed Improvements
Based on latest research in self-improving coding agents
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
import asyncio
from dataclasses import dataclass
from enum import Enum
import numpy as np
import google.generativeai as genai
import os


class ReflectionType(Enum):
    PERFORMANCE = "performance"
    ERROR_ANALYSIS = "error_analysis"
    PATTERN_DISCOVERY = "pattern_discovery"
    STRATEGY_OPTIMIZATION = "strategy_optimization"
    META_LEARNING = "meta_learning"


@dataclass
class ReflectionInsight:
    type: ReflectionType
    content: str
    confidence: float
    evidence: List[str]
    actionable_steps: List[str]
    timestamp: datetime
    impact_score: float = 0.0


class AdvancedReflexionFramework:
    """
    Enhanced Reflexion with:
    1. Multi-level reflection (tactical, strategic, meta)
    2. Confidence-weighted insights
    3. Causal reasoning
    4. Counterfactual analysis
    5. Transfer learning across domains
    """
    
    def __init__(self, memory_system):
        self.memory = memory_system
        self.reflection_history = []
        self.insight_confidence_threshold = 0.7
        self.meta_learning_cycles = 0
        
    async def deep_reflection_cycle(self, 
                                  task_context: Dict, 
                                  performance_data: Dict,
                                  external_feedback: Optional[Dict] = None) -> List[ReflectionInsight]:
        """
        Conduct multi-level reflection with causal analysis
        """
        insights = []
        
        # Level 1: Tactical Reflection (immediate performance)
        tactical_insights = await self._tactical_reflection(task_context, performance_data)
        insights.extend(tactical_insights)
        
        # Level 2: Strategic Reflection (pattern analysis)
        strategic_insights = await self._strategic_reflection(performance_data)
        insights.extend(strategic_insights)
        
        # Level 3: Meta-Learning Reflection (learning about learning)
        if self.meta_learning_cycles > 5:  # Only after sufficient experience
            meta_insights = await self._meta_learning_reflection()
            insights.extend(meta_insights)
        
        # Causal Analysis: Why did certain approaches work/fail?
        causal_insights = await self._causal_analysis(task_context, performance_data)
        insights.extend(causal_insights)
        
        # Counterfactual Reasoning: What if we had done X instead?
        counterfactual_insights = await self._counterfactual_analysis(task_context, performance_data)
        insights.extend(counterfactual_insights)
        
        # Filter by confidence and store high-quality insights
        high_confidence_insights = [i for i in insights if i.confidence >= self.insight_confidence_threshold]
        
        for insight in high_confidence_insights:
            self.memory.add_reflection({
                'type': insight.type.value,
                'content': insight.content,
                'confidence': insight.confidence,
                'evidence': insight.evidence,
                'actionable_steps': insight.actionable_steps,
                'impact_score': insight.impact_score
            }, importance=0.9)
        
        self.reflection_history.extend(high_confidence_insights)
        self.meta_learning_cycles += 1
        
        return high_confidence_insights
    
    async def _tactical_reflection(self, task_context: Dict, performance_data: Dict) -> List[ReflectionInsight]:
        """Immediate performance analysis"""
        insights = []
        
        # Analyze code quality trends
        quality_score = performance_data.get('quality_score', 0)
        time_taken = performance_data.get('time_taken', 0)
        success = performance_data.get('success', False)
        
        if quality_score < 70 and success:
            insight = ReflectionInsight(
                type=ReflectionType.PERFORMANCE,
                content=f"Code generated successfully but quality score ({quality_score}) below optimal threshold",
                confidence=0.8,
                evidence=[f"Quality score: {quality_score}/100", f"Success: {success}"],
                actionable_steps=[
                    "Increase code review rigor",
                    "Add more specific quality criteria to prompts",
                    "Implement iterative refinement"
                ],
                timestamp=datetime.now(),
                impact_score=0.7
            )
            insights.append(insight)
        
        if time_taken > 30:  # Slow generation
            insight = ReflectionInsight(
                type=ReflectionType.PERFORMANCE,
                content=f"Generation took {time_taken:.1f}s - investigating efficiency bottlenecks",
                confidence=0.9,
                evidence=[f"Time taken: {time_taken}s", "Expected: <20s"],
                actionable_steps=[
                    "Optimize prompt length",
                    "Use more efficient model routing",
                    "Implement response caching"
                ],
                timestamp=datetime.now(),
                impact_score=0.6
            )
            insights.append(insight)
        
        return insights
    
    async def _strategic_reflection(self, performance_data: Dict) -> List[ReflectionInsight]:
        """Pattern analysis across multiple generations"""
        insights = []
        
        # Analyze recent performance trends
        recent_history = self.memory.performance_history[-10:] if len(self.memory.performance_history) >= 10 else []
        
        if len(recent_history) >= 5:
            success_rates = [h.get('success', False) for h in recent_history]
            quality_scores = [h.get('quality_score', 0) for h in recent_history if h.get('quality_score')]
            
            # Trend analysis
            if len(quality_scores) >= 5:
                recent_avg = np.mean(quality_scores[-3:])
                older_avg = np.mean(quality_scores[:3])
                
                if recent_avg > older_avg + 5:  # Significant improvement
                    insight = ReflectionInsight(
                        type=ReflectionType.PATTERN_DISCOVERY,
                        content=f"Quality improving: {older_avg:.1f} → {recent_avg:.1f}. Learning is effective.",
                        confidence=0.85,
                        evidence=[f"Recent avg: {recent_avg:.1f}", f"Earlier avg: {older_avg:.1f}"],
                        actionable_steps=[
                            "Continue current learning strategy",
                            "Identify specific patterns driving improvement",
                            "Increase pattern reuse frequency"
                        ],
                        timestamp=datetime.now(),
                        impact_score=0.8
                    )
                    insights.append(insight)
                elif recent_avg < older_avg - 5:  # Declining performance
                    insight = ReflectionInsight(
                        type=ReflectionType.ERROR_ANALYSIS,
                        content=f"Quality declining: {older_avg:.1f} → {recent_avg:.1f}. Need strategy adjustment.",
                        confidence=0.9,
                        evidence=[f"Recent avg: {recent_avg:.1f}", f"Earlier avg: {older_avg:.1f}"],
                        actionable_steps=[
                            "Review recent changes in approach",
                            "Increase validation rigor",
                            "Revert to previously successful patterns"
                        ],
                        timestamp=datetime.now(),
                        impact_score=0.9
                    )
                    insights.append(insight)
        
        return insights
    
    async def _meta_learning_reflection(self) -> List[ReflectionInsight]:
        """Learning about the learning process itself"""
        insights = []
        
        # Analyze learning efficiency
        if len(self.reflection_history) >= 10:
            # How often do our insights lead to actual improvements?
            actionable_insights = [r for r in self.reflection_history if len(r.actionable_steps) > 0]
            high_impact_insights = [r for r in self.reflection_history if r.impact_score > 0.7]
            
            insight_effectiveness = len(high_impact_insights) / len(actionable_insights) if actionable_insights else 0
            
            if insight_effectiveness > 0.7:
                insight = ReflectionInsight(
                    type=ReflectionType.META_LEARNING,
                    content=f"Reflection process highly effective ({insight_effectiveness:.1%} high-impact insights)",
                    confidence=0.8,
                    evidence=[f"High-impact insights: {len(high_impact_insights)}", f"Total actionable: {len(actionable_insights)}"],
                    actionable_steps=[
                        "Maintain current reflection depth",
                        "Focus on similar insight types",
                        "Increase reflection frequency"
                    ],
                    timestamp=datetime.now(),
                    impact_score=0.8
                )
                insights.append(insight)
            elif insight_effectiveness < 0.3:
                insight = ReflectionInsight(
                    type=ReflectionType.META_LEARNING,
                    content=f"Reflection process needs improvement ({insight_effectiveness:.1%} effectiveness)",
                    confidence=0.9,
                    evidence=[f"Low effectiveness: {insight_effectiveness:.1%}"],
                    actionable_steps=[
                        "Increase insight confidence thresholds",
                        "Focus on more specific, actionable insights",
                        "Validate insights against actual outcomes"
                    ],
                    timestamp=datetime.now(),
                    impact_score=0.9
                )
                insights.append(insight)
        
        return insights
    
    async def _causal_analysis(self, task_context: Dict, performance_data: Dict) -> List[ReflectionInsight]:
        """Analyze causal relationships between actions and outcomes"""
        insights = []
        
        # Configure Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key in ['demo-key', 'YOUR_API_KEY_HERE']:
            return insights  # Skip if API key not configured
        
        genai.configure(api_key=api_key)
        causal_model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""Analyze the causal relationships in this coding agent performance:

TASK CONTEXT:
{json.dumps(task_context, indent=2)}

PERFORMANCE DATA:
{json.dumps(performance_data, indent=2)}

RECENT HISTORY:
{json.dumps(self.memory.performance_history[-5:], indent=2, default=str)}

Identify:
1. What specific factors likely CAUSED the current performance level?
2. Which actions had the strongest causal impact?
3. What are the key causal chains (A → B → C)?

Return JSON:
{{
  "primary_causes": ["cause 1", "cause 2"],
  "causal_chains": [["action", "intermediate_effect", "final_outcome"]],
  "confidence": 0.0-1.0,
  "evidence": ["evidence 1", "evidence 2"]
}}"""
        
        try:
            response = await asyncio.to_thread(causal_model.generate_content, prompt)
            
            # Parse response
            response_text = response.text.strip()
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            
            causal_data = json.loads(response_text.strip())
            
            if causal_data.get('confidence', 0) > 0.6:
                insight = ReflectionInsight(
                    type=ReflectionType.ERROR_ANALYSIS,
                    content=f"Causal analysis: {', '.join(causal_data.get('primary_causes', []))}",
                    confidence=causal_data.get('confidence', 0.6),
                    evidence=causal_data.get('evidence', []),
                    actionable_steps=[
                        f"Address primary cause: {causal_data.get('primary_causes', ['Unknown'])[0]}",
                        "Monitor causal chain effects",
                        "Test causal hypotheses in next generation"
                    ],
                    timestamp=datetime.now(),
                    impact_score=0.8
                )
                insights.append(insight)
        
        except Exception as e:
            print(f"Causal analysis failed: {e}")
        
        return insights
    
    async def _counterfactual_analysis(self, task_context: Dict, performance_data: Dict) -> List[ReflectionInsight]:
        """What if we had done things differently?"""
        insights = []
        
        # Identify alternative approaches that could have been taken
        current_approach = task_context.get('approach', 'standard')
        success = performance_data.get('success', False)
        
        if not success:
            # Configure Gemini
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key or api_key in ['demo-key', 'YOUR_API_KEY_HERE']:
                return insights  # Skip if API key not configured
            
            genai.configure(api_key=api_key)
            counterfactual_model = genai.GenerativeModel('gemini-flash-latest')
            
            prompt = f"""Analyze counterfactual scenarios for this failed coding task:

TASK: {task_context.get('description', 'Unknown')}
APPROACH USED: {current_approach}
FAILURE REASON: {performance_data.get('error', 'Unknown')}

What alternative approaches might have succeeded? Consider:
1. Different prompting strategies
2. Alternative model routing
3. Different validation approaches
4. Modified generation parameters

Return JSON:
{{
  "counterfactuals": [
    {{
      "alternative_approach": "description",
      "likely_outcome": "success/failure",
      "confidence": 0.0-1.0,
      "reasoning": "why this might work"
    }}
  ],
  "most_promising": "approach name"
}}"""
            
            try:
                response = await asyncio.to_thread(counterfactual_model.generate_content, prompt)
                
                response_text = response.text.strip()
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0]
                
                counterfactual_data = json.loads(response_text.strip())
                
                most_promising = counterfactual_data.get('most_promising')
                if most_promising:
                    insight = ReflectionInsight(
                        type=ReflectionType.STRATEGY_OPTIMIZATION,
                        content=f"Counterfactual analysis suggests trying: {most_promising}",
                        confidence=0.7,
                        evidence=[f"Current approach failed: {current_approach}", f"Alternative identified: {most_promising}"],
                        actionable_steps=[
                            f"Implement {most_promising} approach",
                            "A/B test against current approach",
                            "Monitor comparative performance"
                        ],
                        timestamp=datetime.now(),
                        impact_score=0.8
                    )
                    insights.append(insight)
            
            except Exception as e:
                print(f"Counterfactual analysis failed: {e}")
        
        return insights
    
    def get_reflection_summary(self) -> Dict:
        """Get comprehensive reflection summary"""
        if not self.reflection_history:
            return {"status": "no_reflections"}
        
        # Group insights by type
        insights_by_type = {}
        for insight in self.reflection_history:
            insight_type = insight.type.value
            if insight_type not in insights_by_type:
                insights_by_type[insight_type] = []
            insights_by_type[insight_type].append(insight)
        
        # Calculate average confidence and impact
        avg_confidence = np.mean([i.confidence for i in self.reflection_history])
        avg_impact = np.mean([i.impact_score for i in self.reflection_history])
        
        # Recent trends
        recent_insights = self.reflection_history[-5:] if len(self.reflection_history) >= 5 else self.reflection_history
        recent_confidence = np.mean([i.confidence for i in recent_insights]) if recent_insights else 0
        
        return {
            "total_reflections": len(self.reflection_history),
            "insights_by_type": {k: len(v) for k, v in insights_by_type.items()},
            "average_confidence": avg_confidence,
            "average_impact": avg_impact,
            "recent_confidence_trend": recent_confidence,
            "meta_learning_cycles": self.meta_learning_cycles,
            "most_recent_insights": [
                {
                    "type": i.type.value,
                    "content": i.content[:100] + "..." if len(i.content) > 100 else i.content,
                    "confidence": i.confidence,
                    "impact": i.impact_score
                }
                for i in recent_insights
            ]
        }