# Flutter Project Structure Guide

## Feature-First vs Layer-First

### Layer-First Structure ❌ (Not Recommended)

```
lib/src/
  ├── presentation/
  │   ├── feature1/
  │   └── feature2/
  ├── application/
  │   ├── feature1/
  │   └── feature2/
  ├── domain/
  │   ├── feature1/
  │   └── feature2/
  └── data/
      ├── feature1/
      └── feature2/
```

**Problems:**
- Files for same feature scattered across multiple directories
- Feature modifications require jumping between distant folders
- Feature deletion risks leaving orphan files
- Team collaboration conflicts increase
- Harder to understand feature scope

### Feature-First Structure ✅ (Strongly Recommended)

```
lib/src/
  ├── features/
  │   ├── authentication/
  │   │   ├── data/
  │   │   │   ├── auth_repository.dart
  │   │   │   └── auth_api.dart
  │   │   ├── domain/
  │   │   │   ├── user.dart
  │   │   │   └── auth_state.dart
  │   │   ├── application/
  │   │   │   └── auth_service.dart (optional)
  │   │   └── presentation/
  │   │       ├── login_screen.dart
  │   │       ├── register_screen.dart
  │   │       └── auth_controller.dart
  │   ├── products/
  │   │   ├── data/
  │   │   │   └── products_repository.dart
  │   │   ├── domain/
  │   │   │   └── product.dart
  │   │   └── presentation/
  │   │       ├── products_list_screen.dart
  │   │       ├── product_detail_screen.dart
  │   │       └── products_controller.dart
  │   └── shopping_cart/
  │       ├── data/
  │       │   └── cart_repository.dart
  │       ├── domain/
  │       │   ├── cart.dart
  │       │   └── cart_item.dart
  │       ├── application/
  │       │   └── checkout_service.dart
  │       └── presentation/
  │           ├── cart_screen.dart
  │           └── cart_controller.dart
  ├── common_widgets/
  │   ├── async_value_widget.dart
  │   ├── custom_button.dart
  │   └── error_message_widget.dart
  ├── constants/
  │   ├── app_sizes.dart
  │   └── api_constants.dart
  ├── routing/
  │   ├── app_router.dart
  │   └── route_paths.dart
  └── utils/
      ├── date_formatter.dart
      └── validators.dart
```

**Advantages:**
- All feature code in one directory
- Feature deletion = folder deletion
- Team collaboration with minimal conflicts
- Clear feature boundaries
- Easy to understand feature scope
- Supports feature-based development

## Critical Warning: Define Features by Functionality, Not UI

### ❌ Wrong: UI-Based Features

```
lib/src/features/
  ├── home_screen/
  ├── profile_screen/
  ├── settings_page/
  └── detail_page/
```

**Problem:** Features represent **screens**, not **business capabilities**. This creates:
- Tight coupling between UI and business logic
- Difficulty reusing logic across screens
- Confusion about where shared functionality belongs

### ✅ Correct: Functionality-Based Features

```
lib/src/features/
  ├── authentication/     # User login, registration, password reset
  ├── user_profile/       # User data management
  ├── product_catalog/    # Browse and search products
  ├── shopping_cart/      # Cart operations
  └── order_management/   # Checkout and order tracking
```

**Principle:** Feature = **functional requirement** (what users accomplish), not UI component

**How to identify correct features:**
1. Ask: "What business capability does this provide?"
2. Features should align with user stories/use cases
3. One feature may span multiple screens
4. One screen may use multiple features

## Directory Organization Rules

### Feature Independence

**Minimize cross-feature dependencies:**

```dart
// ❌ Bad: Direct cross-feature dependency
// In features/shopping_cart/
import '../../product_catalog/domain/product.dart'; // Tight coupling

// ✅ Good: Shared domain in common or extract to shared package
// In features/shared/domain/
export 'product.dart';

// In features/shopping_cart/
import '../shared/domain/product.dart';
```

### Layer Organization Within Features

**Required layers:** data, domain, presentation
**Optional layer:** application (only when needed)

```dart
// Always present
features/my_feature/
  ├── data/        # Repositories, APIs, DTOs
  ├── domain/      # Entities, value objects
  └── presentation/ # Widgets, controllers

// Add only when needed
features/my_feature/
  ├── application/  # Services coordinating multiple repositories
  ├── data/
  ├── domain/
  └── presentation/
```

### Common Directories

**common_widgets/** - Reusable UI components
- Generic widgets used across features
- No feature-specific logic
- Examples: custom buttons, loading indicators, error displays

**constants/** - App-wide constants
- API endpoints
- App sizes, colors (if not using themes)
- Configuration values

**routing/** - Navigation configuration
- App router setup
- Route definitions
- Deep linking

**utils/** - Helper functions
- Date formatters
- Validators
- String utilities
- Pure functions with no state

**exceptions/** - Custom exception types
- Network exceptions
- Validation exceptions
- Business rule exceptions

## File Naming Conventions

### General Rules
- Use snake_case: `user_repository.dart`, `auth_controller.dart`
- Be descriptive: `products_list_screen.dart` not `list.dart`
- Include layer suffix when helpful: `_repository`, `_controller`, `_service`

### Specific Conventions

**Models (domain/):**
```
user.dart
product.dart
order.dart
```

**Repositories (data/):**
```
user_repository.dart
products_repository.dart
orders_repository.dart
```

**Controllers (presentation/):**
```
auth_controller.dart
products_controller.dart
checkout_controller.dart
```

**Services (application/):**
```
authentication_service.dart
payment_service.dart
```

**Screens (presentation/):**
```
login_screen.dart
products_list_screen.dart
product_detail_screen.dart
```

**Widgets (presentation/ or common_widgets/):**
```
product_card.dart
cart_item_tile.dart
custom_app_bar.dart
```

## Decision Criteria: Feature-First vs Layer-First

### Choose Feature-First When (Recommended):
- ✅ 5+ independent features
- ✅ Team works on features in parallel
- ✅ Frequent feature additions/removals
- ✅ Microservice-style thinking
- ✅ Want clear feature ownership

### Choose Layer-First When (Rare):
- ✅ Very small app (1-3 features)
- ✅ Educational/learning purposes
- ✅ Explicit architecture layer emphasis needed
- ✅ All features tightly coupled

**Andrea's recommendation:** "Feature-first for 95% of Flutter apps"

## Migration Strategy: Layer-First → Feature-First

### Step-by-Step Approach

1. **Create features/ directory structure:**
```bash
mkdir -p lib/src/features/{feature1,feature2}/{data,domain,application,presentation}
```

2. **Move files feature by feature:**
```bash
# For each feature:
mv lib/src/data/feature1/* lib/src/features/feature1/data/
mv lib/src/domain/feature1/* lib/src/features/feature1/domain/
mv lib/src/presentation/feature1/* lib/src/features/feature1/presentation/
```

3. **Update imports:**
```dart
// Before
import '../../../data/feature1/repository.dart';

// After
import '../data/repository.dart'; // Much simpler!
```

4. **Test thoroughly after each feature migration**

5. **Remove old empty layer directories**

## Best Practices

### 1. Feature Scope Guidelines

**Good feature size:** 5-20 files
- Too small: Over-fragmentation
- Too large: Split into sub-features

**Example of feature too large:**
```
features/ecommerce/ # Too broad!
```

**Better split:**
```
features/product_catalog/
features/shopping_cart/
features/order_management/
features/payment_processing/
```

### 2. Cross-Feature Communication

**Use Riverpod providers for cross-feature state:**

```dart
// In features/authentication/
@riverpod
User? currentUser(CurrentUserRef ref) {
  return ref.watch(authStateProvider).value;
}

// In features/shopping_cart/
@riverpod
class CartController extends _$CartController {
  @override
  Future<Cart> build() async {
    final user = ref.watch(currentUserProvider);
    if (user == null) throw Exception('Not authenticated');
    // Load user's cart
  }
}
```

### 3. Shared Domain Models

**Option A: features/shared/domain/**
```
lib/src/features/
  ├── shared/
  │   └── domain/
  │       └── user.dart  # Used by multiple features
  ├── authentication/
  ├── profile/
  └── settings/
```

**Option B: Separate package (for large apps)**
```
packages/
  └── my_app_models/
      └── lib/
          └── user.dart

lib/src/features/authentication/
  # Import from package
```

### 4. Testing Structure Mirrors Source

```
lib/src/features/authentication/
  ├── data/
  ├── domain/
  └── presentation/

test/features/authentication/
  ├── data/
  ├── domain/
  └── presentation/
```

## References

- [Flutter Project Structure: Feature-first or Layer-first?](https://codewithandrea.com/articles/flutter-project-structure/)
- [Flutter App Architecture with Riverpod: An Introduction](https://codewithandrea.com/articles/flutter-app-architecture-riverpod-introduction/)
