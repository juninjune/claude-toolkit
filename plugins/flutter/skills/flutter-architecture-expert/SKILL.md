---
name: flutter-architecture-expert
description: Expert guidance for Flutter app architecture based on Andrea Bizzotto's best practices. Use when designing Flutter app architecture, implementing Riverpod patterns, structuring projects, creating repositories, managing state, or answering architecture questions. Covers 4-layer Riverpod architecture, feature-first structure, repository pattern, state management, error handling, and testing strategies.
---

# Flutter Architecture Expert

Provide expert guidance on Flutter app architecture based on Andrea Bizzotto's proven best practices from Code with Andrea. This skill enables implementation of modern, scalable Flutter applications using the 4-layer Riverpod architecture pattern.

## When to Use This Skill

Invoke this skill when:
- Designing Flutter app architecture from scratch
- Implementing Riverpod-based state management
- Structuring Flutter project directories (feature-first vs layer-first)
- Creating repositories following best practices
- Managing data fetching and mutations
- Handling errors and side effects
- Making architectural decisions (Clean Architecture vs Riverpod, BLoC vs Riverpod)
- Setting up proper layer separation
- Optimizing provider lifecycle and caching
- Testing Flutter architecture components

## Core Architecture Philosophy

Follow these principles when providing architectural guidance:

1. **Clear contracts over specific patterns** - Well-defined component interfaces matter more than which pattern is chosen
2. **Pragmatism over theoretical purity** - Prioritize developer productivity and maintainability over architectural perfection
3. **Progressive complexity** - Start simple, add layers only when needed
4. **Testability as validation** - If testing is difficult, the architecture needs improvement

## The 4-Layer Riverpod Architecture

When designing Flutter apps, recommend this layered structure:

### Layer Overview

```
Presentation Layer (Widgets + Controllers)
    ↓ ref.watch / ref.read
Application Layer (Services) [Optional]
    ↓
Domain Layer (Models)
    ↓
Data Layer (Repositories + APIs)
```

### Layer Responsibilities

**Presentation Layer:**
- UI rendering with ConsumerWidget
- User interaction handling
- Controllers (AsyncNotifier) for UI state and mutations
- Never include business logic

**Application Layer (Optional):**
- Coordinate multiple repositories
- Complex business logic requiring multiple data sources
- Only add when Repository alone is insufficient

**Domain Layer:**
- Immutable business entities
- Serialization (fromJson/toJson with freezed)
- Business logic as extensions
- Zero infrastructure dependencies

**Data Layer:**
- Repository pattern as gateway
- API communication and data source access
- DTO to Entity conversion
- Optional caching

### Implementation Workflow

When implementing a feature:

1. **Start with Domain** - Define entities and business logic
   - Create immutable model classes with freezed
   - Add business logic as extensions
   - Reference: See `assets/feature_template/domain/model_template.dart.txt`

2. **Implement Data Layer** - Create repository
   - Define Repository class with data operations
   - Convert DTOs to domain entities
   - Throw domain-specific exceptions
   - Reference: See `assets/feature_template/data/repository_template.dart.txt`
   - Detailed guidance: Read `references/repository_pattern.md`

3. **Add Providers** - Set up Riverpod providers
   - FutureProvider for read-only data
   - AsyncNotifier for mutations
   - Reference: Read `references/state_management.md`

4. **Build Presentation** - Create UI components
   - ConsumerWidget for reactive UI
   - AsyncValue.when() for state handling
   - Controllers for user actions
   - Reference: See `assets/feature_template/presentation/controller_template.dart.txt`

## Project Structure: Feature-First (Strongly Recommended)

Always recommend feature-first structure over layer-first:

```
lib/src/
  ├── features/
  │   ├── authentication/
  │   │   ├── data/
  │   │   ├── domain/
  │   │   ├── application/ (optional)
  │   │   └── presentation/
  │   ├── product_catalog/
  │   └── shopping_cart/
  ├── common_widgets/
  ├── constants/
  └── routing/
```

**Critical: Define features by functionality, not UI**
- ❌ Wrong: `home_screen/`, `profile_page/`
- ✅ Correct: `user_management/`, `product_catalog/`

For comprehensive project structure guidance, reference `references/project_structure.md`.

## State Management Patterns

### Read Operations (Data Fetching)

Use FutureProvider or StreamProvider - AsyncNotifier is NOT needed for simple reads:

```dart
@riverpod
Future<Product> product(ProductRef ref, String id) {
  final repo = ref.watch(productsRepositoryProvider);
  return repo.fetchProduct(id);
}
```

### Write Operations (Mutations)

Use AsyncNotifier for mutations:

```dart
@riverpod
class UpdateProductController extends _$UpdateProductController {
  @override
  FutureOr<void> build() {}

  Future<void> updateProduct(Product product) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final repo = ref.read(productsRepositoryProvider);
      await repo.updateProduct(product);
      ref.invalidate(productProvider(product.id));
    });
  }
}
```

### Key Distinctions

- **ref.watch** - Use in build() for reactive subscriptions
- **ref.read** - Use in callbacks for one-time access
- **ref.listen** - Use for side effects (navigation, snackbars)

For detailed state management patterns, reference `references/state_management.md`.

## Repository Pattern Best Practices

### Core Principles

1. **Prefer concrete classes over abstract** - Only create abstract classes when multiple implementations actually exist
2. **Avoid leaky abstractions** - Don't expose backend-specific types (Firestore Query, HTTP Response)
3. **But don't sacrifice features** - Accept intentional leakage when features justify it (e.g., Firestore cursor pagination)
4. **Throw domain exceptions** - Not infrastructure exceptions

### Repository Structure

```dart
class ProductsRepository {
  const ProductsRepository(this._httpClient);
  final HttpClient _httpClient;

  Future<List<Product>> fetchProducts() async {
    // Fetch, convert DTOs to entities, handle errors
  }

  Future<void> updateProduct(Product product) async {
    // Mutate data, throw domain exceptions
  }
}
```

For comprehensive repository guidance, reference `references/repository_pattern.md`.

## Architecture Decision Making

When users ask "Which architecture should I use?", apply these criteria:

### Recommend Riverpod Architecture When:
- ✅ Small to large-scale Flutter apps
- ✅ Strong type safety required
- ✅ Code generation acceptable
- ✅ Modern Flutter patterns preferred
- ✅ Test coverage important

### Consider Alternatives When:
- Multi-platform logic sharing required → Clean Architecture
- Enterprise mandates BLoC → BLoC pattern
- Very simple prototype → setState

For detailed architecture comparison, reference `references/architecture_patterns.md`.

## Error Handling Approaches

Present both approaches and let user choose:

### try/catch (Simpler)
- Cleaner syntax
- Good for most small-to-medium apps
- Implicit error propagation

### Result Type (More Explicit)
- Compile-time error handling enforcement
- Better for complex error scenarios
- More verbose

Avoid dogmatic recommendations - acknowledge trade-offs.

## Side Effects Handling

**Never allow side effects in:**
- `build()` methods
- `builder` callbacks in StreamBuilder, FutureBuilder

**Side effects belong in:**
- Button/gesture callbacks
- initState()
- Bloc/Notifier methods
- ref.listen() callbacks

## Testing Architecture

Guide testing at appropriate layers:

**Domain Layer** - Easiest (no dependencies)
```dart
test('Cart.addItem increases quantity', () {
  final cart = Cart({});
  final updated = cart.addItem(productId: 'p1', quantity: 2);
  expect(updated.items['p1'], 2);
});
```

**Repository** - Mock data sources
**Controllers** - Override providers with ProviderScope
**Widgets** - Override providers and test UI states

## Common Anti-Patterns to Avoid

When reviewing code or providing guidance, watch for these mistakes:

1. **❌ Side effects in build()** - Never mutate state or call APIs in build methods
2. **❌ Over-abstraction** - Don't create abstract repositories when only one implementation exists
3. **❌ UI-based features** - Features should be functional capabilities, not screens
4. **❌ Repository business logic** - Business logic belongs in domain extensions, not repositories
5. **❌ Global state everywhere** - Not everything needs to be a global provider
6. **❌ AsyncNotifier for simple reads** - Use FutureProvider when you just need to fetch data

## Providing Guidance

When answering architecture questions:

1. **Understand the context** - Ask about app scale, team experience, requirements
2. **Start with principles** - Explain the "why" behind recommendations
3. **Reference detailed docs** - Point to specific reference files for deep dives
4. **Provide code examples** - Use templates from `assets/` or create custom examples
5. **Acknowledge trade-offs** - No architecture is perfect; discuss pros and cons
6. **Be pragmatic** - Recommend simplicity when appropriate

## Reference Files

Load these reference files as needed for detailed guidance:

- **`references/architecture_patterns.md`** - Deep comparison of Flutter architectures (Riverpod, Clean, BLoC, MVVM, etc.) with decision criteria
- **`references/project_structure.md`** - Feature-first vs layer-first structure, naming conventions, organization rules
- **`references/repository_pattern.md`** - Repository responsibilities, abstract vs concrete, leaky abstractions, testing
- **`references/state_management.md`** - Riverpod patterns, provider lifecycle, caching strategies, read vs write operations

Search patterns for references:
- Architecture comparison questions → `references/architecture_patterns.md`
- Project organization questions → `references/project_structure.md`
- Repository implementation questions → `references/repository_pattern.md`
- State management questions → `references/state_management.md`

## Template Files

Use these templates as starting points:

- **`assets/feature_template/domain/model_template.dart.txt`** - Freezed model with business logic extensions
- **`assets/feature_template/data/repository_template.dart.txt`** - Complete repository with CRUD operations and exceptions
- **`assets/feature_template/presentation/controller_template.dart.txt`** - AsyncNotifier controller for mutations

Copy templates and customize for specific use cases. Explain each section as you adapt them.

## Implementation Checklist

When implementing a complete feature, follow this sequence:

1. ✅ Create feature directory structure (feature-first)
2. ✅ Define domain models with freezed
3. ✅ Add business logic as model extensions
4. ✅ Implement repository with proper exceptions
5. ✅ Create providers (FutureProvider for reads)
6. ✅ Create controllers (AsyncNotifier for writes)
7. ✅ Build UI with ConsumerWidget
8. ✅ Handle all AsyncValue states (data/loading/error)
9. ✅ Add ref.listen for side effects if needed
10. ✅ Write tests for domain, repository, controllers, widgets
11. ✅ Run code generation: `dart run build_runner watch -d`

## Key Quotes from Andrea Bizzotto

Use these insights when explaining concepts:

- "Clear contracts and boundaries are more important than which design pattern you choose"
- "When you just need to fetch data, you don't need AsyncNotifier at all!"
- "Most cases only need one implementation" (on abstract vs concrete repositories)
- "Don't create lowest-common-denominator APIs that sacrifice real features"
- Clean Architecture "adds mental overhead" in Flutter context
- Feature-first structure: "Feature deletion = folder deletion"
- "Don't look at the UI and define your features from that"
