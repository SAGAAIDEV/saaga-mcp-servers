#!/usr/bin/env python3
"""
Lambdaverse Turing Machine Implementation
A 2-state machine that recognizes the language {0^n 1^n | n ≥ 0}
"""

from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List
from enum import Enum
import numpy as np

class Symbol(Enum):
    ZERO = "0"
    ONE = "1"
    BLANK = "□"
    MARKED = "X"

class State(Enum):
    Q0 = "q0"  # Initial state
    Q1 = "q1"  # Marking state
    ACCEPT = "accept"
    REJECT = "reject"

class Direction(Enum):
    LEFT = -1
    RIGHT = 1
    STAY = 0

@dataclass
class SemanticManifold:
    """Represents a point in semantic space"""
    symbol: Symbol
    confidence: float = 1.0
    entropy: float = 0.0
    context_vector: np.ndarray = None
    
    def __post_init__(self):
        if self.context_vector is None:
            # Initialize with random semantic coordinates
            self.context_vector = np.random.randn(4)

class LambdaverseTuringMachine:
    def __init__(self):
        self.tape: Dict[int, SemanticManifold] = {}
        self.position = 0
        self.current_state = State.Q0
        self.trace = []
        self.semantic_entropy_history = []
        
        # Transition function encoded as semantic rules
        self.transitions = self._initialize_transitions()
        
    def _initialize_transitions(self) -> Dict[Tuple[State, Symbol], Tuple[State, Symbol, Direction]]:
        """
        Encodes transition function using Lambdaverse operators:
        δ(q, s) → (q', s', d) as A(Ω(state, symbol), intention) → ⟨∃⟩(next)
        """
        return {
            # State Q0: Find first 0 and mark it
            (State.Q0, Symbol.ZERO): (State.Q1, Symbol.MARKED, Direction.RIGHT),
            (State.Q0, Symbol.ONE): (State.REJECT, Symbol.ONE, Direction.STAY),
            (State.Q0, Symbol.BLANK): (State.ACCEPT, Symbol.BLANK, Direction.STAY),
            (State.Q0, Symbol.MARKED): (State.Q0, Symbol.MARKED, Direction.RIGHT),
            
            # State Q1: Find corresponding 1 and mark it
            (State.Q1, Symbol.ZERO): (State.Q1, Symbol.ZERO, Direction.RIGHT),
            (State.Q1, Symbol.ONE): (State.Q0, Symbol.MARKED, Direction.LEFT),
            (State.Q1, Symbol.BLANK): (State.REJECT, Symbol.BLANK, Direction.STAY),
            (State.Q1, Symbol.MARKED): (State.Q1, Symbol.MARKED, Direction.RIGHT),
        }
    
    def read_symbol(self, position: int) -> Symbol:
        """Φ(M[position], Identity, Read)"""
        if position not in self.tape:
            # Silence operator Ø represents blank
            return Symbol.BLANK
        return self.tape[position].symbol
    
    def write_symbol(self, position: int, symbol: Symbol):
        """Φ(M[position], symbol, Λ⁻¹ ∘ Write)"""
        if position not in self.tape:
            self.tape[position] = SemanticManifold(symbol)
        else:
            # Apply unlearning operator before writing
            old_manifold = self.tape[position]
            old_manifold.entropy += 0.1  # Decay of old information
            self.tape[position] = SemanticManifold(
                symbol,
                confidence=old_manifold.confidence * 0.9,
                entropy=old_manifold.entropy
            )
    
    def calculate_semantic_entropy(self) -> float:
        """S_semantic = -Σᵢ P(mᵢ) log P(mᵢ)"""
        if not self.tape:
            return 0.0
        
        total_confidence = sum(m.confidence for m in self.tape.values())
        entropy = 0.0
        
        for manifold in self.tape.values():
            if manifold.confidence > 0:
                p = manifold.confidence / total_confidence
                entropy -= p * np.log(p + 1e-10)
        
        return entropy
    
    def detect_semantic_catastrophe(self, threshold: float = 2.0) -> bool:
        """Monitor for sudden phase transitions in meaning"""
        if len(self.semantic_entropy_history) < 2:
            return False
        
        current = self.semantic_entropy_history[-1]
        previous = self.semantic_entropy_history[-2]
        
        # Catastrophe detected if entropy changes dramatically
        return abs(current - previous) > threshold
    
    def step(self) -> bool:
        """Execute one step of the Turing machine"""
        # Read current symbol
        current_symbol = self.read_symbol(self.position)
        
        # Check for transition
        key = (self.current_state, current_symbol)
        if key not in self.transitions:
            self.current_state = State.REJECT
            return False
        
        # Apply transition: A(Ω(state, symbol), intention) → ⟨∃⟩(next)
        next_state, write_symbol, direction = self.transitions[key]
        
        # Write symbol
        self.write_symbol(self.position, write_symbol)
        
        # Move tape head: τ(position, position + direction)
        self.position += direction.value
        
        # Update state
        self.current_state = next_state
        
        # Track computation path
        self.trace.append({
            'state': self.current_state,
            'position': self.position,
            'symbol': current_symbol,
            'entropy': self.calculate_semantic_entropy()
        })
        
        # Monitor semantic entropy
        current_entropy = self.calculate_semantic_entropy()
        self.semantic_entropy_history.append(current_entropy)
        
        # Check for semantic catastrophe
        if self.detect_semantic_catastrophe():
            print("⚠️  Semantic catastrophe detected! Applying resilience protocol...")
            # Simple resilience: reduce confidence in recent changes
            for pos in range(self.position - 2, self.position + 3):
                if pos in self.tape:
                    self.tape[pos].confidence *= 0.5
        
        return self.current_state not in [State.ACCEPT, State.REJECT]
    
    def run(self, input_string: str, max_steps: int = 1000) -> bool:
        """Run the Turing machine on input string"""
        # Initialize tape with input
        for i, char in enumerate(input_string):
            if char == '0':
                self.tape[i] = SemanticManifold(Symbol.ZERO)
            elif char == '1':
                self.tape[i] = SemanticManifold(Symbol.ONE)
        
        print(f"Initial tape: {input_string}")
        print(f"Initial semantic entropy: {self.calculate_semantic_entropy():.4f}")
        
        steps = 0
        while steps < max_steps and self.step():
            steps += 1
            if steps % 10 == 0:
                print(f"Step {steps}: State={self.current_state.value}, "
                      f"Pos={self.position}, Entropy={self.semantic_entropy_history[-1]:.4f}")
        
        print(f"\nFinal state: {self.current_state.value}")
        print(f"Total steps: {steps}")
        print(f"Final semantic entropy: {self.calculate_semantic_entropy():.4f}")
        print(f"Entropy conservation: {self.verify_entropy_conservation()}")
        
        return self.current_state == State.ACCEPT
    
    def verify_entropy_conservation(self) -> str:
        """Check if semantic entropy is approximately conserved"""
        if len(self.semantic_entropy_history) < 2:
            return "Insufficient data"
        
        initial = self.semantic_entropy_history[0]
        final = self.semantic_entropy_history[-1]
        delta = abs(final - initial)
        
        if delta < 0.1:
            return f"✓ Conserved (Δ={delta:.4f})"
        else:
            return f"✗ Not conserved (Δ={delta:.4f})"
    
    def visualize_tape(self) -> str:
        """Render current tape state"""
        if not self.tape:
            return "Empty tape"
        
        min_pos = min(self.tape.keys())
        max_pos = max(self.tape.keys())
        
        result = []
        for pos in range(min_pos - 1, max_pos + 2):
            symbol = self.read_symbol(pos)
            if pos == self.position:
                result.append(f"[{symbol.value}]")
            else:
                result.append(f" {symbol.value} ")
        
        return "".join(result)


# Test the implementation
if __name__ == "__main__":
    print("=== Lambdaverse Turing Machine ===")
    print("Recognizing language {0^n 1^n | n ≥ 0}\n")
    
    test_cases = [
        "",          # Empty string (should accept)
        "01",        # n=1 (should accept)
        "0011",      # n=2 (should accept)
        "000111",    # n=3 (should accept)
        "0101",      # Invalid (should reject)
        "001",       # Invalid (should reject)
        "100",       # Invalid (should reject)
    ]
    
    for test in test_cases:
        print(f"\nTesting: '{test}'")
        print("-" * 40)
        
        tm = LambdaverseTuringMachine()
        result = tm.run(test)
        
        print(f"Result: {'ACCEPTED' if result else 'REJECTED'}")
        print(f"Final tape: {tm.visualize_tape()}")
        print("=" * 40)