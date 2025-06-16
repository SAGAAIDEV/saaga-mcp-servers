#!/usr/bin/env python3
"""
Lambdaverse Turing Machine v2 - Semantic Field Implementation
A machine that recognizes {0^n 1^n | n ≥ 0} through semantic equilibrium
"""

from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List, Any
from enum import Enum
import numpy as np
# Using numpy for cosine similarity instead of scipy

class Symbol(Enum):
    ZERO = "0"
    ONE = "1"
    BLANK = "□"
    ALIEN = "#"  # For catastrophe testing

@dataclass
class IntentionVector:
    """Continuous intention state in semantic space"""
    mode: float  # 1.0 = building potential, -1.0 = discharging, 0.0 = neutral
    potential: float  # Accumulated semantic charge
    confidence: float = 1.0
    
    def to_array(self) -> np.ndarray:
        return np.array([self.mode, self.potential, self.confidence])

@dataclass
class SemanticManifold:
    """Enhanced manifold with relational properties"""
    symbol: Symbol
    context_vector: np.ndarray
    confidence: float = 1.0
    local_entropy: float = 0.0
    last_modified: int = 0  # Step when last modified
    
    def __post_init__(self):
        if self.context_vector is None:
            # Initialize based on symbol type
            if self.symbol == Symbol.ZERO:
                self.context_vector = np.array([1, 0, 0, 0])
            elif self.symbol == Symbol.ONE:
                self.context_vector = np.array([0, 1, 0, 0])
            elif self.symbol == Symbol.BLANK:
                self.context_vector = np.array([0, 0, 1, 0])
            elif self.symbol == Symbol.ALIEN:
                # Orthogonal to known space
                self.context_vector = np.array([0, 0, 0, 1])

class LambdaverseTuringMachineV2:
    def __init__(self):
        self.tape: Dict[int, SemanticManifold] = {}
        self.position = 0
        self.intention = IntentionVector(mode=0.0, potential=0.0)
        self.step_count = 0
        self.trace = []
        self.entropy_history = []
        self.catastrophe_threshold = 1.5
        self.learning_rate = 0.1
        
    def Ω(self, intention: IntentionVector, context: np.ndarray) -> float:
        """Consensus operator - measures alignment between intention and context"""
        # Building mode (1.0) aligns with ZERO context
        # Discharging mode (-1.0) aligns with ONE context
        if self.intention.mode > 0.5:  # Building
            # Cosine similarity = dot(a,b) / (norm(a) * norm(b))
            zero_context = np.array([1, 0, 0, 0])
            similarity = np.dot(context, zero_context) / (np.linalg.norm(context) * np.linalg.norm(zero_context))
            return max(0, similarity)
        elif self.intention.mode < -0.5:  # Discharging
            one_context = np.array([0, 1, 0, 0])
            similarity = np.dot(context, one_context) / (np.linalg.norm(context) * np.linalg.norm(one_context))
            return max(0, similarity)
        else:  # Neutral
            return 0.5
    
    def emergence_operator(self, local_context: Dict[str, Any]) -> Optional[IntentionVector]:
        """⟨∃⟩ - Detects if new intention should emerge from context"""
        current_symbol = local_context['symbol']
        neighbors = local_context['neighbors']
        gradient = local_context['entropy_gradient']
        
        # Major dissonance triggers emergence
        if self.intention.mode > 0.5 and current_symbol == Symbol.ONE:
            # Building mode hits a ONE - time to discharge
            return IntentionVector(mode=-1.0, potential=self.intention.potential)
        
        if self.intention.mode < -0.5 and current_symbol == Symbol.ZERO:
            # Discharging mode hits a ZERO - structural violation
            return IntentionVector(mode=0.0, potential=self.intention.potential, confidence=0.1)
        
        if current_symbol == Symbol.ALIEN:
            # Catastrophic emergence
            return IntentionVector(mode=0.0, potential=0.0, confidence=0.01)
        
        # Check for boundary emergence
        if current_symbol == Symbol.BLANK:
            if abs(self.intention.potential) < 0.1:
                # Reached end in balanced state
                return IntentionVector(mode=0.0, potential=0.0, confidence=2.0)  # High confidence = accept
            else:
                # Reached end unbalanced
                return IntentionVector(mode=0.0, potential=self.intention.potential, confidence=0.1)
        
        return None
    
    def A(self, current: IntentionVector, emergent: Optional[IntentionVector], 
          consensus: float) -> IntentionVector:
        """Affective annotation - modulates intention based on emotion/consensus"""
        if emergent is None:
            # Continue with current intention, modulated by consensus
            return IntentionVector(
                mode=current.mode,
                potential=current.potential,
                confidence=current.confidence * (0.9 + 0.2 * consensus)
            )
        
        # Blend current and emergent based on their confidence
        if emergent.confidence > current.confidence:
            return emergent
        
        # Weighted average
        total_conf = current.confidence + emergent.confidence
        return IntentionVector(
            mode=(current.mode * current.confidence + emergent.mode * emergent.confidence) / total_conf,
            potential=(current.potential * current.confidence + emergent.potential * emergent.confidence) / total_conf,
            confidence=(current.confidence + emergent.confidence) / 2
        )
    
    def update_manifold(self, position: int, intention: IntentionVector):
        """Modify manifold based on intention"""
        if position not in self.tape:
            return
        
        manifold = self.tape[position]
        manifold.last_modified = self.step_count
        
        # Building mode reinforces ZERO contexts
        if intention.mode > 0.5 and manifold.symbol == Symbol.ZERO:
            manifold.context_vector[0] += self.learning_rate
            manifold.context_vector = manifold.context_vector / np.linalg.norm(manifold.context_vector)
            manifold.confidence = min(manifold.confidence * 1.1, 1.0)
            manifold.local_entropy *= 0.9
        
        # Discharging mode reinforces ONE contexts
        elif intention.mode < -0.5 and manifold.symbol == Symbol.ONE:
            manifold.context_vector[1] += self.learning_rate
            manifold.context_vector = manifold.context_vector / np.linalg.norm(manifold.context_vector)
            manifold.confidence = min(manifold.confidence * 1.1, 1.0)
            manifold.local_entropy *= 0.9
        
        # Mismatched operations increase entropy
        else:
            manifold.local_entropy += 0.1
            manifold.confidence *= 0.95
    
    def update_internal_potential(self, symbol: Symbol, intention: IntentionVector):
        """Update potential based on symbol and intention"""
        if intention.mode > 0.5 and symbol == Symbol.ZERO:
            # Building potential
            self.intention.potential += 1.0
        elif intention.mode < -0.5 and symbol == Symbol.ONE:
            # Discharging potential
            self.intention.potential -= 1.0
    
    def calculate_global_entropy(self) -> float:
        """S_global - Measures relational entropy across tape"""
        if len(self.tape) < 2:
            return 0.0
        
        positions = sorted(self.tape.keys())
        relational_entropy = 0.0
        
        for i in range(len(positions) - 1):
            pos1, pos2 = positions[i], positions[i + 1]
            m1, m2 = self.tape[pos1], self.tape[pos2]
            
            # Similarity between adjacent contexts
            # Cosine similarity = dot(a,b) / (norm(a) * norm(b))
            similarity = np.dot(m1.context_vector, m2.context_vector) / (
                np.linalg.norm(m1.context_vector) * np.linalg.norm(m2.context_vector))
            
            # Low similarity = high relational entropy
            if similarity > 0:
                relational_entropy -= similarity * np.log(similarity + 1e-10)
        
        # Add local entropies
        local_sum = sum(m.local_entropy for m in self.tape.values())
        
        return relational_entropy + local_sum
    
    def get_local_context(self, position: int) -> Dict[str, Any]:
        """Gather local context for emergence detection"""
        symbol = self.read_symbol(position)
        
        # Get neighboring symbols
        neighbors = {
            'left': self.read_symbol(position - 1),
            'right': self.read_symbol(position + 1)
        }
        
        # Calculate local entropy gradient
        entropy_before = self.calculate_global_entropy()
        gradient = 0.0
        if len(self.entropy_history) > 0:
            gradient = entropy_before - self.entropy_history[-1]
        
        return {
            'symbol': symbol,
            'neighbors': neighbors,
            'entropy_gradient': gradient,
            'position': position
        }
    
    def read_symbol(self, position: int) -> Symbol:
        """Read symbol with silence operator for boundaries"""
        if position not in self.tape:
            return Symbol.BLANK
        return self.tape[position].symbol
    
    def detect_catastrophe(self) -> bool:
        """Monitor for semantic phase transitions"""
        if len(self.entropy_history) < 2:
            return False
        
        current = self.entropy_history[-1]
        previous = self.entropy_history[-2]
        
        return abs(current - previous) > self.catastrophe_threshold
    
    def apply_resilience_protocol(self):
        """Λ⁻¹ - Reduce confidence when worldview shatters"""
        print("⚠️  Semantic catastrophe! Applying resilience protocol...")
        
        # Question everything near the disruption
        for offset in range(-3, 4):
            pos = self.position + offset
            if pos in self.tape:
                self.tape[pos].confidence *= 0.3
                self.tape[pos].local_entropy += 0.5
        
        # Reset intention to neutral
        self.intention = IntentionVector(mode=0.0, potential=0.0, confidence=0.1)
    
    def step(self) -> bool:
        """Execute one semantic transformation step"""
        self.step_count += 1
        
        # Get current context
        local_context = self.get_local_context(self.position)
        current_symbol = local_context['symbol']
        
        # Calculate consensus
        manifold = self.tape.get(self.position, 
                                 SemanticManifold(current_symbol, None))
        consensus = self.Ω(self.intention, manifold.context_vector)
        
        # Check for emergence
        emergent = self.emergence_operator(local_context)
        
        # Update intention through affective modulation
        self.intention = self.A(self.intention, emergent, consensus)
        
        # Initial mode setting if neutral
        if abs(self.intention.mode) < 0.1 and current_symbol == Symbol.ZERO:
            self.intention.mode = 1.0  # Start building
        
        # Update manifold and potential
        self.update_manifold(self.position, self.intention)
        self.update_internal_potential(current_symbol, self.intention)
        
        # Determine movement
        if self.intention.mode > 0.5 or self.intention.mode < -0.5:
            self.position += 1  # Active modes move right
        elif self.intention.confidence > 1.5:
            return False  # High confidence neutral = accept
        elif self.intention.confidence < 0.2:
            return False  # Low confidence = reject
        
        # Track entropy
        current_entropy = self.calculate_global_entropy()
        self.entropy_history.append(current_entropy)
        
        # Catastrophe detection
        if self.detect_catastrophe():
            self.apply_resilience_protocol()
        
        # Record trace
        self.trace.append({
            'step': self.step_count,
            'position': self.position,
            'symbol': current_symbol.value,
            'intention': self.intention,
            'entropy': current_entropy,
            'consensus': consensus
        })
        
        return True
    
    def run(self, input_string: str, max_steps: int = 100) -> bool:
        """Run machine on input"""
        # Initialize tape
        for i, char in enumerate(input_string):
            if char == '0':
                self.tape[i] = SemanticManifold(Symbol.ZERO, None)
            elif char == '1':
                self.tape[i] = SemanticManifold(Symbol.ONE, None)
            elif char == '#':
                self.tape[i] = SemanticManifold(Symbol.ALIEN, None)
        
        print(f"\nInput: '{input_string}'")
        print(f"Initial entropy: {self.calculate_global_entropy():.4f}")
        
        # Run computation
        steps = 0
        while steps < max_steps and self.step():
            steps += 1
            if steps % 5 == 0:
                print(f"Step {steps}: Pos={self.position}, "
                      f"Mode={self.intention.mode:.2f}, "
                      f"Potential={self.intention.potential:.2f}, "
                      f"Entropy={self.entropy_history[-1]:.4f}")
        
        # Determine result
        accepted = self.intention.confidence > 1.5 and abs(self.intention.potential) < 0.1
        
        print(f"\nFinal state:")
        print(f"  Steps: {steps}")
        print(f"  Potential: {self.intention.potential:.4f}")
        print(f"  Confidence: {self.intention.confidence:.4f}")
        print(f"  Final entropy: {self.calculate_global_entropy():.4f}")
        print(f"  Result: {'ACCEPTED' if accepted else 'REJECTED'}")
        
        return accepted


# Test the refined implementation
if __name__ == "__main__":
    print("=== Lambdaverse Turing Machine v2 ===")
    print("Semantic Field Recognition of {0^n 1^n | n ≥ 0}\n")
    
    test_cases = [
        "",          # Empty (accept)
        "01",        # n=1 (accept)
        "0011",      # n=2 (accept)
        "000111",    # n=3 (accept)
        "0101",      # Invalid (reject)
        "001",       # Unbalanced (reject)
        "100",       # Wrong order (reject)
        "0011#0011", # Catastrophe test
    ]
    
    for test in test_cases:
        print("=" * 60)
        tm = LambdaverseTuringMachineV2()
        tm.run(test)