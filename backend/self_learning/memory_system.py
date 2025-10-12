from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import deque
import json
import math


class MemoryEntry:
    """Represents a single memory entry with metadata."""
    
    def __init__(self, content: Dict, memory_type: str, importance: float = 0.5):
        self.content = content
        self.memory_type = memory_type
        self.importance = importance
        self.timestamp = datetime.now()
        self.access_count = 0
        self.last_accessed = datetime.now()
        self.retention_strength = 1.0
    
    def access(self):
        """Record memory access."""
        self.access_count += 1
        self.last_accessed = datetime.now()
        # Strengthen memory on access (spaced repetition)
        self.retention_strength = min(1.0, self.retention_strength + 0.1)
    
    def decay(self, hours_passed: float):
        """Apply Ebbinghaus forgetting curve."""
        # Forgetting curve: R(t) = e^(-t/S)
        # where S is retention strength
        decay_rate = 0.1 * (1.0 - self.importance)  # Important memories decay slower
        self.retention_strength *= math.exp(-hours_passed * decay_rate)
        return self.retention_strength


class HierarchicalMemory:
    """Multi-tier memory system inspired by human cognition."""
    
    def __init__(self):
        # Short-term memory (working memory) - holds immediate context
        self.short_term = deque(maxlen=10)
        
        # Mid-term memory (episodic) - stores recent experiences
        self.mid_term = deque(maxlen=50)
        
        # Long-term memory (semantic + procedural) - consolidated knowledge
        self.long_term = {
            'successful_patterns': [],
            'failed_patterns': [],
            'learned_rules': [],
            'procedural_knowledge': [],
            'performance_insights': []
        }
        
        # Reflective memory - meta-insights about agent's own performance
        self.reflective = []
        
        # Performance trajectory for learning
        self.performance_history = []
    
    def add_short_term(self, content: Dict, importance: float = 0.5):
        """Add to short-term memory."""
        entry = MemoryEntry(content, 'short_term', importance)
        self.short_term.append(entry)
        return entry
    
    def add_episode(self, episode: Dict, importance: float = 0.7):
        """Add an episode to mid-term memory."""
        entry = MemoryEntry(episode, 'episode', importance)
        self.mid_term.append(entry)
        
        # Consolidate to long-term if important enough
        if importance > 0.8:
            self._consolidate_to_long_term(entry)
        
        return entry
    
    def add_reflection(self, reflection: Dict, importance: float = 0.9):
        """Add reflective insight."""
        entry = MemoryEntry(reflection, 'reflection', importance)
        self.reflective.append(entry)
        return entry
    
    def add_performance_record(self, record: Dict):
        """Track performance over time."""
        record['timestamp'] = datetime.now().isoformat()
        self.performance_history.append(record)
        
        # Analyze trajectory for insights
        if len(self.performance_history) >= 5:
            insights = self._analyze_performance_trajectory()
            if insights:
                self.add_reflection({
                    'type': 'performance_analysis',
                    'insights': insights
                }, importance=0.95)
    
    def _consolidate_to_long_term(self, entry: MemoryEntry):
        """Move important memories to long-term storage."""
        content = entry.content
        
        if content.get('success'):
            # Extract patterns from successful generations
            pattern = {
                'description': content.get('description'),
                'approach': content.get('approach'),
                'quality_score': content.get('quality_score'),
                'timestamp': entry.timestamp.isoformat(),
                'access_count': 0
            }
            self.long_term['successful_patterns'].append(pattern)
        else:
            # Learn from failures
            failure = {
                'description': content.get('description'),
                'error': content.get('error'),
                'attempted_solution': content.get('attempted_solution'),
                'timestamp': entry.timestamp.isoformat()
            }
            self.long_term['failed_patterns'].append(failure)
    
    def _analyze_performance_trajectory(self) -> Optional[Dict]:
        """Analyze recent performance for learning insights."""
        recent = self.performance_history[-10:]
        
        if not recent:
            return None
        
        # Calculate trends
        scores = [r.get('quality_score', 0) for r in recent if r.get('quality_score')]
        
        if len(scores) < 3:
            return None
        
        avg_recent = sum(scores[-3:]) / 3
        avg_older = sum(scores[:3]) / 3
        
        insights = {
            'trend': 'improving' if avg_recent > avg_older else 'declining',
            'avg_recent_score': avg_recent,
            'avg_older_score': avg_older,
            'delta': avg_recent - avg_older
        }
        
        # Extract common patterns in successes vs failures
        successes = [r for r in recent if r.get('success')]
        failures = [r for r in recent if not r.get('success')]
        
        insights['success_rate'] = len(successes) / len(recent)
        
        return insights
    
    def retrieve_relevant(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant memories based on query."""
        relevant = []
        
        # Search all memory tiers
        for entry in list(self.short_term) + list(self.mid_term) + self.reflective:
            # Simple keyword matching (can be enhanced with embeddings)
            content_str = json.dumps(entry.content).lower()
            if any(word in content_str for word in query.lower().split()):
                entry.access()  # Mark as accessed
                relevant.append({
                    'content': entry.content,
                    'importance': entry.importance,
                    'retention': entry.retention_strength,
                    'type': entry.memory_type
                })
        
        # Sort by importance and retention
        relevant.sort(key=lambda x: x['importance'] * x['retention'], reverse=True)
        return relevant[:top_k]
    
    def get_consolidated_knowledge(self) -> Dict:
        """Get consolidated long-term knowledge."""
        return {
            'successful_patterns_count': len(self.long_term['successful_patterns']),
            'failed_patterns_count': len(self.long_term['failed_patterns']),
            'learned_rules': self.long_term['learned_rules'],
            'recent_insights': self.reflective[-5:] if self.reflective else [],
            'performance_trend': self._analyze_performance_trajectory()
        }
    
    def apply_forgetting_curve(self):
        """Apply memory decay based on Ebbinghaus forgetting curve."""
        now = datetime.now()
        
        # Decay mid-term memories
        for entry in self.mid_term:
            hours_passed = (now - entry.last_accessed).total_seconds() / 3600
            retention = entry.decay(hours_passed)
            
            # If retention drops too low, remove from mid-term
            if retention < 0.1 and entry.importance < 0.5:
                self.mid_term.remove(entry)
    
    def get_statistics(self) -> Dict:
        """Get memory system statistics."""
        return {
            'short_term_count': len(self.short_term),
            'mid_term_count': len(self.mid_term),
            'long_term_patterns': len(self.long_term['successful_patterns']),
            'reflective_insights': len(self.reflective),
            'performance_records': len(self.performance_history),
            'success_rate': len([r for r in self.performance_history if r.get('success')]) / len(self.performance_history) if self.performance_history else 0
        }
