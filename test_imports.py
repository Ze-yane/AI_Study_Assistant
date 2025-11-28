import sys
import traceback

print("=" * 60)
print("TESTING MODULE IMPORTS")
print("=" * 60)

# Test 1: StudyAssistant
print("\n[1/3] Testing StudyAssistant...")
try:
    from study import StudyAssistant
    print("✓ StudyAssistant imported successfully")
except SyntaxError as e:
    print(f"✗ SYNTAX ERROR in study.py:")
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"✗ ERROR in study.py:")
    traceback.print_exc()
    sys.exit(1)

# Test 2: BudgetTracker
print("\n[2/3] Testing BudgetTracker...")
try:
    from budget import BudgetTracker
    print("✓ BudgetTracker imported successfully")
except Exception as e:
    print(f"✗ ERROR in budget.py:")
    traceback.print_exc()
    sys.exit(1)

# Test 3: CVBuilder
print("\n[3/3] Testing CVBuilder...")
try:
    from cv_builder import CVBuilder
    print("✓ CVBuilder imported successfully")
except Exception as e:
    print(f"✗ ERROR in cv_builder.py:")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL MODULES IMPORTED SUCCESSFULLY!")
print("=" * 60)
