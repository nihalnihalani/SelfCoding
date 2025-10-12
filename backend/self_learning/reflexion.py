from typing import Dict, List, Any, Optional
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import json
import uuid


class ReflexionFramework:
    """Implements the Reflexion framework for self-correction.
    
    Components:
    - Actor: Generates solutions
    - Evaluator: Assesses quality
    - Self-Reflection: Learns from mistakes
    """
    
    def __init__(self, memory_system):
        self.memory = memory_system
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
    
    async def actor_generate(self, task: str, context: Optional[Dict] = None) -> Dict:
        """Actor: Generate initial solution."""
        
        # Retrieve relevant memories
        relevant_memories = self.memory.retrieve_relevant(task, top_k=3)
        
        # Build context from memories
        memory_context = ""
        if relevant_memories:
            memory_context = "\n\nRELEVANT PAST EXPERIENCES:\n"
            for i, mem in enumerate(relevant_memories, 1):
                memory_context += f"\n{i}. {mem['content'].get('description', 'N/A')}\n"
                if mem['content'].get('insight'):
                    memory_context += f"   Insight: {mem['content']['insight']}\n"
        
        actor_chat = LlmChat(
            api_key=self.api_key,
            session_id=f"actor_{uuid.uuid4()}",
            system_message="You are an expert code generator. Generate high-quality, complete code."
        ).with_model("gemini", "gemini-2.5-flash")
        
        prompt = f"""Generate a complete web application.

TASK: {task}

CONTEXT:
{json.dumps(context, indent=2) if context else 'None'}

{memory_context}

Return ONLY valid JSON:
{{
  "files": {{"index.html": "...", "styles.css": "...", "script.js": "..."}},
  "approach": "brief description of approach",
  "metadata": {{"tech_stack": [], "features": []}}
}}"""
        
        response = await actor_chat.send_message(UserMessage(text=prompt))
        
        # Parse response
        response_text = response.strip()
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0]
        
        result = json.loads(response_text.strip())
        
        # Store in short-term memory
        self.memory.add_short_term({
            'task': task,
            'solution': result,
            'stage': 'initial_generation'
        })
        
        return result
    
    async def evaluator_assess(self, task: str, solution: Dict) -> Dict:
        """Evaluator: Assess solution quality."""
        
        evaluator_chat = LlmChat(
            api_key=self.api_key,
            session_id=f"evaluator_{uuid.uuid4()}",
            system_message="You are an expert code reviewer. Provide detailed, constructive evaluation."
        ).with_model("gemini", "gemini-2.5-pro")
        
        files_summary = "\n".join([f"{name}: {len(content)} chars" for name, content in solution.get('files', {}).items()])
        
        prompt = f"""Evaluate this generated code.

TASK: {task}

APPROACH: {solution.get('approach', 'N/A')}

FILES:
{files_summary}

Evaluate:
1. Correctness (0-100)
2. Completeness (0-100) 
3. Code quality (0-100)
4. Best practices (0-100)
5. Potential issues
6. Strengths
7. Weaknesses

Return JSON:
{{
  "overall_score": 0-100,
  "correctness": 0-100,
  "completeness": 0-100,
  "quality": 0-100,
  "best_practices": 0-100,
  "issues": ["issue 1", "issue 2"],
  "strengths": ["strength 1"],
  "weaknesses": ["weakness 1"],
  "verdict": "pass/needs_improvement/fail",
  "feedback": "detailed feedback"
}}"""
        
        response = await evaluator_chat.send_message(UserMessage(text=prompt))
        
        # Parse response
        response_text = response.strip()
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0]
        
        evaluation = json.loads(response_text.strip())
        
        # Store evaluation
        self.memory.add_short_term({
            'task': task,
            'evaluation': evaluation,
            'stage': 'evaluation'
        })
        
        return evaluation
    
    async def self_reflect(self, task: str, solution: Dict, evaluation: Dict) -> Dict:
        """Self-Reflection: Learn from evaluation."""
        
        reflector_chat = LlmChat(
            api_key=self.api_key,
            session_id=f"reflector_{uuid.uuid4()}",
            system_message="You are a meta-learning system. Extract deep insights and lessons from experiences."
        ).with_model("gemini", "gemini-2.5-pro")
        
        prompt = f"""Reflect on this code generation experience.

TASK: {task}
APPROACH: {solution.get('approach')}
SCORE: {evaluation.get('overall_score')}/100
VERDICT: {evaluation.get('verdict')}

STRENGTHS:
{json.dumps(evaluation.get('strengths', []), indent=2)}

WEAKNESSES:
{json.dumps(evaluation.get('weaknesses', []), indent=2)}

ISSUES:
{json.dumps(evaluation.get('issues', []), indent=2)}

Reflect deeply:
1. What worked well and why?
2. What didn't work and why?
3. What should be done differently next time?
4. What general principles can be learned?
5. What patterns should be remembered?
6. How can this inform future generations?

Return JSON:
{{
  "key_learnings": ["learning 1", "learning 2"],
  "action_items": ["action 1", "action 2"],
  "patterns_to_remember": ["pattern 1"],
  "patterns_to_avoid": ["anti-pattern 1"],
  "improvement_strategy": "strategy description",
  "meta_insight": "deep insight about the learning process itself"
}}"""
        
        response = await reflector_chat.send_message(UserMessage(text=prompt))
        
        # Parse response
        response_text = response.strip()
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0]
        
        reflection = json.loads(response_text.strip())
        
        # Store reflection in reflective memory (high importance)
        self.memory.add_reflection({
            'task': task,
            'score': evaluation.get('overall_score'),
            'reflection': reflection,
            'timestamp': 'now'
        }, importance=0.95)
        
        return reflection
    
    async def improve_solution(self, task: str, solution: Dict, evaluation: Dict, reflection: Dict) -> Dict:
        """Generate improved solution based on reflection."""
        
        improver_chat = LlmChat(
            api_key=self.api_key,
            session_id=f"improver_{uuid.uuid4()}",
            system_message="You are a code improvement specialist. Apply learnings to create better code."
        ).with_model("gemini", "gemini-2.5-flash")
        
        prompt = f"""Improve this code based on reflection.

ORIGINAL TASK: {task}
ORIGINAL SCORE: {evaluation.get('overall_score')}/100

WEAKNESSES IDENTIFIED:
{json.dumps(evaluation.get('weaknesses', []), indent=2)}

ISSUES:
{json.dumps(evaluation.get('issues', []), indent=2)}

KEY LEARNINGS:
{json.dumps(reflection.get('key_learnings', []), indent=2)}

ACTION ITEMS:
{json.dumps(reflection.get('action_items', []), indent=2)}

IMPROVEMENT STRATEGY:
{reflection.get('improvement_strategy')}

Generate IMPROVED code that addresses all issues and applies learnings.

Return JSON:
{{
  "files": {{"index.html": "...", "styles.css": "...", "script.js": "..."}},
  "improvements_made": ["improvement 1", "improvement 2"],
  "approach": "updated approach description"
}}"""
        
        response = await improver_chat.send_message(UserMessage(text=prompt))
        
        # Parse response
        response_text = response.strip()
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0]
        
        improved = json.loads(response_text.strip())
        
        return improved
    
    async def reflexion_loop(self, task: str, context: Optional[Dict] = None, max_iterations: int = 3) -> Dict:
        """Complete reflexion loop: generate → evaluate → reflect → improve."""
        
        iteration_log = []
        best_solution = None
        best_score = 0
        
        for iteration in range(max_iterations):
            print(f"\n=== Reflexion Iteration {iteration + 1}/{max_iterations} ===")
            
            # Generate or improve
            if iteration == 0:
                solution = await self.actor_generate(task, context)
            else:
                solution = await self.improve_solution(task, prev_solution, prev_evaluation, prev_reflection)
            
            # Evaluate
            evaluation = await self.evaluator_assess(task, solution)
            score = evaluation.get('overall_score', 0)
            
            print(f"Score: {score}/100 - Verdict: {evaluation.get('verdict')}")
            
            # Track best solution
            if score > best_score:
                best_score = score
                best_solution = solution
            
            # Reflect
            reflection = await self.self_reflect(task, solution, evaluation)
            
            # Log iteration
            iteration_log.append({
                'iteration': iteration + 1,
                'score': score,
                'verdict': evaluation.get('verdict'),
                'key_learnings': reflection.get('key_learnings', [])
            })
            
            # Store episode
            self.memory.add_episode({
                'task': task,
                'iteration': iteration + 1,
                'solution': solution,
                'evaluation': evaluation,
                'reflection': reflection,
                'success': score >= 80
            }, importance=0.8 if score >= 80 else 0.6)
            
            # Break if excellent
            if score >= 95 or evaluation.get('verdict') == 'pass':
                print(f"✅ Excellent result achieved at iteration {iteration + 1}!")
                break
            
            # Prepare for next iteration
            prev_solution = solution
            prev_evaluation = evaluation
            prev_reflection = reflection
        
        # Record performance
        self.memory.add_performance_record({
            'task': task,
            'final_score': best_score,
            'iterations': len(iteration_log),
            'success': best_score >= 80
        })
        
        return {
            'solution': best_solution,
            'final_score': best_score,
            'iterations': iteration_log,
            'learning_summary': self.memory.get_consolidated_knowledge()
        }
