# Code Review Principles for Refactoring Opportunities

This document contains evidence-based principles for identifying refactoring opportunities, detecting unnecessary complexity, and maintaining code health. These principles are derived from Google's Engineering Practices, Martin Fowler's work, and scientific research on technical debt.

## Table of Contents

1. [Complexity and Code Health](#complexity-and-code-health)
2. [YAGNI: Avoiding Over-Engineering](#yagni-avoiding-over-engineering)
3. [Cognitive Complexity](#cognitive-complexity)
4. [Technical Debt Prioritization](#technical-debt-prioritization)
5. [When to Refactor](#when-to-refactor)

---

## Complexity and Code Health

### Google's Standard: "Too Complex"

**Definition**: "Too complex" usually means **"can't be understood quickly by code readers"** or **"developers are likely to introduce bugs when they try to call or modify this code."**

### Key Principles

1. **Continuous Improvement Over Perfection**
   - The primary purpose of code review is to ensure the overall code health is **improving over time**
   - A change that improves maintainability, readability, and understandability shouldn't be delayed for perfection
   - However, **never accept changes that degrade code health**

2. **System-Level Thinking**
   - Consider whether changes improve or degrade the **whole system**
   - Small incremental increases in complexity compound over time
   - Prevent complexity in early stages—it's harder to fix later

3. **What Makes Code Complex?**
   - Long functions (generally >50 lines is a warning sign)
   - Deeply nested conditionals (>3 levels)
   - Multiple responsibilities in one class/function
   - Unclear naming or logic flow
   - Excessive coupling between components

### Review Questions to Ask

- Can a new developer understand this code within 5 minutes?
- Would modifying this code likely introduce bugs?
- Does this change make the system easier or harder to test?
- Is the solution addressing actual requirements or anticipated future needs?

---

## YAGNI: Avoiding Over-Engineering

### Definition

**YAGNI** = "You Aren't Gonna Need It"

A principle from Extreme Programming: **don't add functionality until it's actually needed**, not when you just anticipate needing it.

### The Four Costs of Ignoring YAGNI

1. **Cost of Build**: Time spent analyzing, programming, and testing unnecessary features
2. **Cost of Delay**: Opportunity cost—features that could generate revenue sooner aren't built
3. **Cost of Carry**: Complexity the unused code adds, making the codebase harder to modify and debug
4. **Cost of Repair**: Technical debt when previously built features need refactoring based on new learnings

### When YAGNI Applies

YAGNI applies to **presumptive features**—code supporting functionality not yet available for use.

**Warning signs of YAGNI violations:**

- Generic interfaces with only one implementation
- Abstract base classes used by only one concrete class
- Configuration options for "future flexibility" that aren't used
- Parameterized logic where parameters are always the same value
- "Just in case" infrastructure

### When YAGNI Does NOT Apply

YAGNI **does not apply** to:

- **Refactoring**: Making code easier to modify is always valuable
- **Self-testing code**: Tests enable evolutionary design
- **Continuous delivery practices**: CI/CD infrastructure has immediate value
- **Architectural patterns needed now**: If multiple parts of the system benefit today, it's not premature

### Detection Strategy

Ask: "If we added this capability later, would it be significantly more expensive?"

- If NO → Current abstraction is likely premature (YAGNI violation)
- If YES → Abstraction may be justified

---

## Cognitive Complexity

### Definition

Cognitive complexity quantifies **the mental effort needed to understand code**, focusing on:

- Flow control structures
- Nesting levels
- Readability of code constructs

### Differences from Cyclomatic Complexity

| Metric | Measures | Purpose |
|--------|----------|---------|
| **Cyclomatic Complexity** | Number of linearly independent paths | Test coverage needs |
| **Cognitive Complexity** | Mental effort to understand code | Code readability |

**Key insight**: Cyclomatic complexity doesn't predict comprehension difficulty well.

### Calculation Method

Start with 1 point, then add points for:

- **Each decision point** (if, switch, while, for, catch, etc.)
- **Nesting level increment** (each additional nesting adds +1 per nested structure)
- **Flow-breaking actions** (break, continue, return in middle of function)
- **Recursion**
- **Use of logical operators** (&&, ||) in conditions

**Example:**

```javascript
// Cognitive Complexity = 7
function processItems(items) {  // +0 (base)
  if (items.length === 0) {     // +1 (decision)
    return;                     // +0 (early return doesn't add nesting)
  }

  for (let item of items) {     // +1 (loop)
    if (item.active) {          // +2 (decision +1, nested +1)
      if (item.priority > 5) {  // +3 (decision +1, nested +2)
        process(item);
      }
    }
  }
}
```

### Code Patterns That Increase Cognitive Load

- **Deeply nested conditional statements** (>3 levels)
- **Excessive logical operators** in single conditions
- **Long methods with multiple execution paths** (>50 lines)
- **Inconsistent coding practices** within same module
- **Lack of code clarity** (unclear variable names, magic numbers)

### Reducing Cognitive Complexity

**Effective strategies:**

1. **Extract nested logic into functions**
   ```javascript
   // Before: Cognitive Complexity = 5
   if (user) {
     if (user.active) {
       if (user.permissions.includes('admin')) {
         grantAccess();
       }
     }
   }

   // After: Cognitive Complexity = 1 (main) + 1 (helper) = 2 total
   if (isAdminUser(user)) {
     grantAccess();
   }

   function isAdminUser(user) {
     return user?.active && user.permissions.includes('admin');
   }
   ```

2. **Early returns to reduce nesting**
   ```javascript
   // Before: Cognitive Complexity = 3
   function process(data) {
     if (data) {
       if (data.valid) {
         return transform(data);
       }
     }
     return null;
   }

   // After: Cognitive Complexity = 2
   function process(data) {
     if (!data || !data.valid) return null;
     return transform(data);
   }
   ```

3. **Replace complex conditions with named booleans**
   ```javascript
   // Before
   if (user.age >= 18 && user.country === 'US' && !user.banned)

   // After
   const isEligibleUser = user.age >= 18 && user.country === 'US' && !user.banned;
   if (isEligibleUser)
   ```

### Threshold Guidelines

- **0-5**: Simple, easy to understand
- **6-10**: Moderate complexity, manageable
- **11-15**: Complex, consider refactoring
- **16+**: Very complex, high priority for refactoring

---

## Technical Debt Prioritization

### Scientific Findings

Research shows that **not all technical debt matters equally**.

### Most Critical Code Smells

**Prioritize detection and resolution of:**

1. **Blob Class / God Class**
   - Classes that are too long (>300-500 lines)
   - Classes serving multiple responsibilities
   - **Impact**: Substantially increases comprehension time and bug risk

2. **Spaghetti Code**
   - Long methods without clear structure (>50-100 lines)
   - Complex control flow with many branches
   - **Impact**: Makes changes error-prone

3. **Multiple Code Smells in Single Class**
   - Research finding: **Multiple smells in one class create serious problems**
   - Even if individual smells are minor, their combination compounds difficulty

### When Technical Debt Matters

**Context determines priority:**

- **High-change areas**: Code modified frequently needs to be clean
  - Example: "Long method in weekly-updated onboarding service" → HIGH PRIORITY

- **Legacy stable code**: Rarely touched code can often stay as-is
  - Example: "Long method in legacy report generator used once/year" → LOW PRIORITY

### Detection Timing

**Key insight**: Most code smells appear **in initial class design** and persist throughout lifecycle.

**Implication**: Prevention > Cure

- Focus on detecting problematic patterns early (during code review)
- Refactoring efforts rarely remove code smells after the fact
- About 89-98% of smells emerge in the month before major releases

### Refactoring Prioritization Matrix

| Smell Type | Change Frequency | Priority |
|------------|------------------|----------|
| Blob Class | High (weekly+) | 🔴 HIGH |
| Spaghetti Code | High (weekly+) | 🔴 HIGH |
| Blob Class | Medium (monthly) | 🟡 MEDIUM |
| Spaghetti Code | Medium (monthly) | 🟡 MEDIUM |
| Duplicated Code | High (weekly+) | 🟡 MEDIUM |
| Any smell | Low (yearly) | 🟢 LOW |
| Minor smells | Any frequency | 🟢 LOW |

---

## When to Refactor

### Martin Fowler's "Rule of Three"

1. **First time**: Just do it (implement straightforward solution)
2. **Second time**: Notice the duplication, but do it anyway
3. **Third time**: Now refactor (eliminate the duplication)

### Best Timing for Refactoring

**Don't schedule separate refactoring time.** Instead, refactor as part of:

1. **While adding features**
   - Look at existing code
   - Refactor it to make the new change straightforward
   - Then add the feature

2. **While fixing bugs**
   - Refactoring helps understand code
   - Often reveals why bug exists
   - Makes fix clearer

3. **During code review**
   - Fresh eyes spot complexity
   - Great opportunity to improve code health
   - Reviewer can suggest simplifications

### The Two Hats

Think of wearing **two hats while programming**:

- **Refactoring hat**: Restructure code, add no new functionality, don't change existing tests
- **Feature hat**: Add new functionality, don't restructure existing code

**Switch between them consciously**, but never wear both at once.

### Small Steps Philosophy

- Refactor in **small chunks** over time
- Each step should be low-risk
- Avoid having system broken during restructuring
- Small steps reduce error introduction

### Speed Benefits

**Counterintuitive insight**: Refactoring makes development **faster**, not slower.

- Code easier to understand
- Changes easier to make
- Bugs easier to find
- New features easier to add

**Technical debt compounds**: Small messes accumulate into large obstacles.

---

## Practical Review Checklist

When reviewing commits for refactoring opportunities, check:

### Complexity Signals

- [ ] Functions longer than 50 lines
- [ ] Nesting deeper than 3 levels
- [ ] Files longer than 500 lines
- [ ] Classes with >5 public methods doing unrelated things
- [ ] Complex boolean logic (>3 conditions combined)

### YAGNI Violations

- [ ] Abstract interfaces with single implementation
- [ ] Generic parameters always passed same value
- [ ] Configuration options never changed
- [ ] "Helper" or "Util" classes with unrelated methods
- [ ] Premature optimization

### Duplication

- [ ] Same code pattern repeated 3+ times
- [ ] Similar logic in different modules
- [ ] Copy-pasted blocks with minor variations

### Readability

- [ ] Unclear variable/function names
- [ ] Magic numbers without constants
- [ ] Comments explaining "what" instead of "why"
- [ ] Inconsistent formatting or patterns

### Test Coverage

- [ ] New code without tests
- [ ] Complex logic not exercised by tests
- [ ] Tests that don't fail when implementation breaks

---

## References

1. [Google Engineering Practices: What to Look For](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
2. [Martin Fowler: YAGNI](https://martinfowler.com/bliki/Yagni.html)
3. [Martin Fowler: Refactoring (2nd Edition)](https://martinfowler.com/books/refactoring.html)
4. [Understanding Cognitive Complexity](https://getdx.com/blog/cognitive-complexity/)
5. [On Technical Debt and Code Smells: Scientific Research](https://www.scrum.org/resources/blog/technical-debt-and-code-smells-surprising-insights-scientific-studies)
