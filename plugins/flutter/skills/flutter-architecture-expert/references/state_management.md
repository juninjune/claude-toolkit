# State Management with Riverpod

## Core Principle: Separate Read and Write Operations

**Key Insight from Andrea:** "When you just need to fetch data, you don't need AsyncNotifier at all!"

### Data Flow Pattern

```
Read (Fetch):  Provider/FutureProvider → Widget watches
Write (Mutate): Controller (AsyncNotifier) → Widget reads notifier
```

## Reading Data (Fetch Operations)

### Use FutureProvider for Simple Data Fetching

```dart
// ✅ Correct: FutureProvider for read-only data
@riverpod
Future<Product> product(ProductRef ref, String id) {
  final repo = ref.watch(productsRepositoryProvider);
  return repo.fetchProduct(id);
}

// Widget usage
class ProductScreen extends ConsumerWidget {
  const ProductScreen({required this.productId});
  final String productId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final productAsync = ref.watch(productProvider(productId));

    return productAsync.when(
      data: (product) => ProductView(product: product),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, stack) => ErrorView(error: err),
    );
  }
}
```

**Why not AsyncNotifier here?**
- No mutation needed
- Provider handles caching automatically
- Less boilerplate
- Simpler to understand

### Use StreamProvider for Real-Time Data

```dart
@riverpod
Stream<List<Message>> messages(MessagesRef ref, String chatId) {
  final repo = ref.watch(messagesRepositoryProvider);
  return repo.watchMessages(chatId);
}

// Widget usage
class MessagesList extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final messagesAsync = ref.watch(messagesProvider(chatId));

    return messagesAsync.when(
      data: (messages) => ListView.builder(
        itemCount: messages.length,
        itemBuilder: (context, index) => MessageTile(messages[index]),
      ),
      loading: () => const CircularProgressIndicator(),
      error: (err, stack) => Text('Error: $err'),
    );
  }
}
```

## Writing Data (Mutation Operations)

### Use AsyncNotifier for Data Mutations

```dart
// Controller for mutations
@riverpod
class UpdateProductController extends _$UpdateProductController {
  @override
  FutureOr<void> build() {
    // No initial state needed for mutation-only controllers
  }

  Future<void> updateProduct(Product product) async {
    // Set loading state
    state = const AsyncLoading();

    // Perform mutation with error handling
    state = await AsyncValue.guard(() async {
      final repo = ref.read(productsRepositoryProvider);
      await repo.updateProduct(product);

      // Invalidate data provider to trigger refetch
      ref.invalidate(productProvider(product.id));
    });
  }
}

// Widget usage
class ProductEditScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch loading state
    final updateState = ref.watch(updateProductControllerProvider);

    // Listen for errors
    ref.listen<AsyncValue>(
      updateProductControllerProvider,
      (prev, next) {
        if (next.hasError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error: ${next.error}')),
          );
        }
      },
    );

    return Column(
      children: [
        // Form fields...

        ElevatedButton(
          onPressed: updateState.isLoading
              ? null
              : () {
                  final product = /* build product from form */;
                  ref.read(updateProductControllerProvider.notifier)
                      .updateProduct(product);
                },
          child: updateState.isLoading
              ? const CircularProgressIndicator()
              : const Text('Save'),
        ),
      ],
    );
  }
}
```

### Combined Read + Write Controller

When you need both fetch and mutate in one controller:

```dart
@riverpod
class ProductController extends _$ProductController {
  @override
  Future<Product> build(String productId) async {
    // Initial load
    final repo = ref.watch(productsRepositoryProvider);
    return repo.fetchProduct(productId);
  }

  Future<void> updateProduct(Product updatedProduct) async {
    state = const AsyncLoading();

    state = await AsyncValue.guard(() async {
      final repo = ref.read(productsRepositoryProvider);
      await repo.updateProduct(updatedProduct);

      // Return updated product as new state
      return updatedProduct;
    });
  }

  Future<void> deleteProduct() async {
    state = const AsyncLoading();

    state = await AsyncValue.guard(() async {
      final repo = ref.read(productsRepositoryProvider);
      final product = state.requireValue;
      await repo.deleteProduct(product.id);

      // Navigate back or handle deletion
      return product; // Or throw to trigger error state
    });
  }
}
```

## ref.watch vs ref.read

### ref.watch - Reactive Subscriptions

**Use in:** `build()` methods only

```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  // ✅ Correct: watch in build()
  final user = ref.watch(currentUserProvider);
  return Text(user?.name ?? 'Guest');
}
```

**Effect:** Widget rebuilds when provider value changes

### ref.read - One-Time Access

**Use in:** Event handlers, callbacks, initState

```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  return ElevatedButton(
    // ✅ Correct: read in callback
    onPressed: () {
      ref.read(counterProvider.notifier).increment();
    },
    child: const Text('Increment'),
  );
}
```

**Effect:** No rebuild on value change, just access current value

### ❌ Common Mistakes

```dart
// ❌ Wrong: read in build()
@override
Widget build(BuildContext context, WidgetRef ref) {
  final user = ref.read(currentUserProvider); // Won't rebuild on change!
  return Text(user?.name ?? 'Guest');
}

// ❌ Wrong: watch in callback
onPressed: () {
  ref.watch(counterProvider.notifier).increment(); // Creates subscription in callback!
}
```

## ref.listen - Side Effects Based on State Changes

```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  // Listen for auth state changes
  ref.listen<User?>(
    currentUserProvider,
    (previous, next) {
      if (next == null) {
        // User logged out, navigate to login
        Navigator.of(context).pushReplacementNamed('/login');
      }
    },
  );

  // Listen for error in mutation
  ref.listen<AsyncValue>(
    updateProductControllerProvider,
    (prev, next) {
      next.whenOrNull(
        error: (error, stack) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error: $error')),
          );
        },
      );
    },
  );

  return Scaffold(/* ... */);
}
```

**When to use `ref.listen`:**
- Navigation based on state
- Showing snackbars/dialogs
- Analytics events
- Side effects that aren't part of UI rendering

## Provider Lifecycle and Caching

### Three Caching Strategies

#### 1. Auto-Dispose (Default)

```dart
// keepAlive: false (default behavior)
@riverpod
Future<Data> data(DataRef ref) async {
  // Disposed when last listener removed
  return fetchData();
}
```

**Use when:**
- Data specific to single widget
- Stream connections should close immediately
- Memory efficiency critical

#### 2. Keep Alive (Global Cache)

```dart
@Riverpod(keepAlive: true)
Future<Data> persistentData(PersistentDataRef ref) async {
  // Never disposed, stays in memory
  return fetchData();
}
```

**Use when:**
- Global app state
- DI objects (auth service, API clients)
- Configuration that never changes

#### 3. Timeout-Based (Hybrid)

```dart
@riverpod
Future<Data> timedData(TimedDataRef ref) async {
  // Keep alive for 30 seconds after last listener removed
  final link = ref.keepAlive();
  Timer? timer;

  ref.onCancel(() {
    timer = Timer(const Duration(seconds: 30), () {
      link.close(); // Now it can be disposed
    });
  });

  ref.onResume(() {
    timer?.cancel(); // Cancel disposal if listener returns
  });

  return fetchData();
}
```

**Use when:**
- Frequently accessed data (user profile)
- Balance between memory and performance
- Tab switching scenarios

### Invalidation and Refresh

```dart
// Manual invalidation
ref.invalidate(productProvider); // Invalidates and refetches

// Refresh (invalidate + wait for new value)
await ref.refresh(productProvider);

// Read fresh value
final product = await ref.refresh(productProvider.future);
```

**Common pattern: Invalidate after mutations**

```dart
Future<void> updateProduct(Product product) async {
  state = await AsyncValue.guard(() async {
    await repo.updateProduct(product);

    // Invalidate related providers
    ref.invalidate(productProvider(product.id));
    ref.invalidate(productsListProvider);
  });
}
```

## Optimizing Rebuilds with select()

### Problem: Unnecessary Rebuilds

```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  // Rebuilds whenever ANY field in User changes
  final user = ref.watch(userProvider);
  return Text(user.name);
}
```

### Solution: select() for Partial Subscriptions

```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  // Only rebuilds when name changes
  final userName = ref.watch(userProvider.select((user) => user.name));
  return Text(userName);
}
```

**Use select() when:**
- Widget only needs one field from large object
- Reducing rebuilds for performance
- Object updates frequently but widget cares about small part

## AsyncValue.when() for State Handling

### Basic Pattern

```dart
final productAsync = ref.watch(productProvider(id));

return productAsync.when(
  data: (product) => ProductView(product: product),
  loading: () => const CircularProgressIndicator(),
  error: (error, stack) => ErrorView(error: error),
);
```

### Variants

**when() - All states required:**
```dart
.when(
  data: (value) => DataWidget(value),
  loading: () => LoadingWidget(),
  error: (err, stack) => ErrorWidget(err),
)
```

**whenData() - Only handle data, ignore loading/error:**
```dart
.whenData((product) => Text(product.name))
```

**whenOrNull() - Optional handling:**
```dart
.whenOrNull(
  data: (product) => ProductView(product),
  error: (err, _) => ErrorView(err),
  // loading defaults to null
) ?? const SizedBox.shrink()
```

**maybeWhen() - Handle some states:**
```dart
.maybeWhen(
  data: (product) => ProductView(product),
  orElse: () => const SizedBox.shrink(),
)
```

## Family Providers for Parameterized State

```dart
// Provider that takes parameter
@riverpod
Future<Product> product(ProductRef ref, String id) {
  final repo = ref.watch(productsRepositoryProvider);
  return repo.fetchProduct(id);
}

// Creates separate provider instance for each id
final product1 = ref.watch(productProvider('id1'));
final product2 = ref.watch(productProvider('id2'));
```

**Caching behavior:**
- Each parameter combination creates separate cached instance
- `productProvider('id1')` and `productProvider('id2')` are independent

**Auto-dispose with family:**
```dart
// Each parameter instance disposes independently
@riverpod
Future<Product> product(ProductRef ref, String id) async {
  // This instance disposes when no widgets watch productProvider(id)
  return repo.fetchProduct(id);
}
```

## Advanced Pattern: Derived State

### Combining Multiple Providers

```dart
@riverpod
Future<List<Product>> products(ProductsRef ref) async {
  final repo = ref.watch(productsRepositoryProvider);
  return repo.fetchProducts();
}

@riverpod
String selectedCategory(SelectedCategoryRef ref) {
  return 'electronics'; // Could be from state
}

// Derived provider combining both
@riverpod
Future<List<Product>> filteredProducts(FilteredProductsRef ref) async {
  final allProducts = await ref.watch(productsProvider.future);
  final category = ref.watch(selectedCategoryProvider);

  return allProducts.where((p) => p.category == category).toList();
}
```

### Dependencies Update Automatically

```dart
class ProductsScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Automatically refetches when selectedCategoryProvider changes!
    final filteredAsync = ref.watch(filteredProductsProvider);

    return filteredAsync.when(
      data: (products) => ProductsList(products),
      loading: () => const CircularProgressIndicator(),
      error: (err, _) => ErrorView(err),
    );
  }
}
```

## Testing State Management

### Testing Providers

```dart
test('products provider fetches products', () async {
  final container = ProviderContainer(
    overrides: [
      productsRepositoryProvider.overrideWithValue(mockRepo),
    ],
  );

  when(mockRepo.fetchProducts()).thenAnswer((_) async => [testProduct]);

  final products = await container.read(productsProvider.future);

  expect(products, [testProduct]);
});
```

### Testing Controllers

```dart
test('updateProductController updates product', () async {
  final container = ProviderContainer(
    overrides: [
      productsRepositoryProvider.overrideWithValue(mockRepo),
    ],
  );

  final controller = container.read(updateProductControllerProvider.notifier);

  await controller.updateProduct(testProduct);

  verify(mockRepo.updateProduct(testProduct)).called(1);

  final state = container.read(updateProductControllerProvider);
  expect(state.hasError, false);
});
```

### Widget Testing with Providers

```dart
testWidgets('ProductScreen shows product name', (tester) async {
  when(mockRepo.fetchProduct('1')).thenAnswer((_) async => testProduct);

  await tester.pumpWidget(
    ProviderScope(
      overrides: [
        productsRepositoryProvider.overrideWithValue(mockRepo),
      ],
      child: MaterialApp(home: ProductScreen(productId: '1')),
    ),
  );

  await tester.pump(); // Trigger loading
  expect(find.byType(CircularProgressIndicator), findsOneWidget);

  await tester.pump(); // Trigger data
  expect(find.text(testProduct.name), findsOneWidget);
});
```

## Key Principles Summary

1. **Separate concerns**: FutureProvider for reads, AsyncNotifier for writes
2. **ref.watch in build()**: For reactive UI
3. **ref.read in callbacks**: For one-time access
4. **ref.listen for side effects**: Navigation, snackbars, analytics
5. **Choose lifecycle strategy**: Auto-dispose, keepAlive, or timeout
6. **Use select()**: Optimize rebuilds for partial state
7. **AsyncValue.when()**: Handle all async states explicitly
8. **Family for parameters**: Each parameter gets separate cache
9. **Invalidate after mutations**: Keep data fresh

## References

- [Flutter Riverpod 2.0: The Ultimate Guide](https://codewithandrea.com/articles/flutter-state-management-riverpod/)
- [How to Fetch Data and Perform Data Mutations with Riverpod](https://codewithandrea.com/articles/data-mutations-riverpod/)
- [Riverpod Data Caching and Providers Lifecycle](https://codewithandrea.com/articles/flutter-riverpod-data-caching-providers-lifecycle/)
