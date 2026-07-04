import collections
import collections.abc
collections.Mapping = collections.abc.Mapping  

from experta import *

# --- 1. EXPERT SYSTEM FACTS ---
class SprintMetrics(Fact):
    """Initial facts inputted by the manager"""
    pass

class TechnicalSkill(Fact):
    """Intermediate fact deduced by the engine"""
    pass

class TeamIntegration(Fact):
    """Intermediate fact deduced by the engine"""
    pass

# --- 2. ADVANCED INFERENCE ENGINE ---
class PerformanceEvaluator(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.feedback = []

    # --- TIER 1: DEDUCING TECHNICAL SKILLS ---
    @Rule(SprintMetrics(bugs=MATCH.b, modularity_score=MATCH.m), 
          TEST(lambda b, m: b <= 1 and m >= 8))
    def tech_expert(self):
        self.declare(TechnicalSkill(level="Expert"))
        self.feedback.append("🔧 Tech Assessment: Expert. Excellent job implementing modular, data-driven architectures.")

    @Rule(SprintMetrics(bugs=MATCH.b, modularity_score=MATCH.m), 
          TEST(lambda b, m: b >= 4 and m <= 5))
    def tech_needs_work(self):
        self.declare(TechnicalSkill(level="Needs_Improvement"))
        self.feedback.append("🔧 Tech Assessment: Needs Improvement. Code is tightly coupled; high defect rate.")

    @Rule(SprintMetrics(bugs=MATCH.b, modularity_score=MATCH.m), 
          TEST(lambda b, m: 1 < b < 4 and 5 < m < 8))
    def tech_average(self):
        self.declare(TechnicalSkill(level="Average"))
        self.feedback.append("🔧 Tech Assessment: Average. Code is functional but has room for architectural improvement.")

    # --- TIER 1: DEDUCING TEAM SKILLS ---
    @Rule(SprintMetrics(code_reviews=MATCH.cr, communication=MATCH.c), 
          TEST(lambda cr, c: cr >= 5 and c >= 8))
    def team_excellent(self):
        self.declare(TeamIntegration(level="Excellent"))
        self.feedback.append("🤝 Team Assessment: Excellent. Highly collaborative and proactive.")

    @Rule(SprintMetrics(code_reviews=MATCH.cr, communication=MATCH.c), 
          TEST(lambda cr, c: cr <= 2 and c <= 5))
    def team_isolated(self):
        self.declare(TeamIntegration(level="Isolated"))
        self.feedback.append("🤝 Team Assessment: Isolated. Working in a silo. Needs to participate more.")

    @Rule(SprintMetrics(code_reviews=MATCH.cr, communication=MATCH.c), 
          TEST(lambda cr, c: 2 < cr < 5 and 5 < c < 8))
    def team_average(self):
        self.declare(TeamIntegration(level="Average"))
        self.feedback.append("🤝 Team Assessment: Average. Meeting basic communication expectations.")

    # NEW TIER 1 RULE: Mixed Signals (High reviews, low communication)
    @Rule(SprintMetrics(code_reviews=MATCH.cr, communication=MATCH.c), 
          TEST(lambda cr, c: cr >= 5 and c <= 4))
    def team_inconsistent(self):
        self.declare(TeamIntegration(level="Inconsistent"))
        self.feedback.append("🤝 Team Assessment: Inconsistent. High volume of code reviews, but poor direct communication.")

    # --- TIER 2: FINAL DECISIONS (CHAINING FACTS) ---
    @Rule(TechnicalSkill(level="Expert"), TeamIntegration(level="Excellent"))
    def promote_to_lead(self):
        self.feedback.append("⭐ FINAL VERDICT: Ready for Promotion. Nominate for Lead Developer.")

    @Rule(TechnicalSkill(level="Expert"), TeamIntegration(level="Isolated"))
    def lone_wolf(self):
        self.feedback.append("⚠️ FINAL VERDICT: 'Lone Wolf' detected. Highly skilled but bottlenecking knowledge transfer.")

    # NEW TIER 2 RULE: Final verdict combining Expert + Inconsistent
    @Rule(TechnicalSkill(level="Expert"), TeamIntegration(level="Inconsistent"))
    def expert_inconsistent_verdict(self):
        self.feedback.append("⚠️ FINAL VERDICT: Technically brilliant, but poor communication is limiting their impact. Recommend soft-skills mentoring.")

    @Rule(TechnicalSkill(level="Needs_Improvement"))
    def PIP_warning(self):
        self.feedback.append("🛑 FINAL VERDICT: Put on Technical Improvement Plan. Pair with a senior engineer.")

    @Rule(TechnicalSkill(level="Average"), TeamIntegration(level="Average"))
    def standard_contributor(self):
        self.feedback.append("⚖️ FINAL VERDICT: Solid Contributor. Meeting expectations across the board.")


# --- 3. COMMAND LINE INTERFACE ---
def run_cli():
    print("\n=============================================")
    print("   Advanced Dev Evaluator (Expert System)    ")
    print("=============================================\n")
    
    try:
        f_points = int(input("1. Feature Points Completed (0-20): "))
        b_count = int(input("2. Critical Bugs Introduced (0-10): "))
        m_score = int(input("3. Code Modularity Score (1-10):    "))
        reviews = int(input("4. Code Reviews Completed (0-15):   "))
        comm = int(input("5. Team Communication Score (1-10): "))
    except ValueError:
        print("\n[Error] Invalid input. Please enter whole numbers only.")
        return

    print("\n[ Running Inference Engine... ]\n")

    # Initialize and run
    engine = PerformanceEvaluator()
    engine.reset()
    engine.declare(SprintMetrics(
        feature_points=f_points, 
        bugs=b_count, 
        modularity_score=m_score,
        code_reviews=reviews,
        communication=comm
    ))
    engine.run()

    # Output results
    if len(engine.feedback) == 0:
        print("🔍 System Notice: Metrics fall outside defined strict rule parameters.")
        print("   Developer is performing adequately in an unclassified middle-tier.")
    else:
        for item in engine.feedback:
            print(item)
            
    print("\n=============================================\n")

if __name__ == "__main__":
    run_cli()