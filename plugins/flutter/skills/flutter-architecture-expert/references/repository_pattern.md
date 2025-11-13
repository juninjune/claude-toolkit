# Repository Pattern in Flutter

## Repository Responsibilities

The Repository Pattern acts as a **gateway between the domain layer and data sources**, with three primary responsibilities:

1. **Isolate domain models from data source implementation details**
   - Domain layer never knows about HTTP, Firebase, SQL, etc.
   - Changes to data source don't affect domain logic

2. **Convert DTOs to validated entities**
   - Transform raw API responses into type-safe domain models
   - Apply validation during conversion
   - Handle data inconsistencies

3. **Optionally handle data caching**
   - In-memory caching for performance
   - Offline support with local databases
   - Cache invalidation strategies

## When to Use Repository Pattern

### ✅ Use Repository For:

**REST API communication:**
```dart
class ProductsRepository {
  Future<List<Product>> fetchProducts() async {
    final response = await _httpClient.get('/products');
    return (response.data as List)
        .map((json) => Product.fromJson(json))
        .toList();
  }
}
```

**Local/Remote Databases:**
```dart
class UserRepository {
  Future<User> getUser(String id) async {
    final doc = await _firestore.collection('users').doc(id).get();
    return User.fromJson(doc.data()!);
  }
}
```

**Device APIs:**
```dart
class LocationRepository {
  Future<Location> getCurrentLocation() async {
    final position = await Geolocator.getCurrentPosition();
    return Location(lat: position.latitude, lon: position.longitude);
  }
}
```

**Hardware Integrations:**
```dart
class CameraRepository {
  Future<Photo> takePhoto() async {
    final XFile? image = await _imagePicker.pickImage(source: ImageSource.camera);
    if (image == null) throw CameraCancelledException();
    return Photo(path: image.path);
  }
}
```

### ❌ Don't Use Repository For:

**Pure business logic** - Use domain model extensions:
```dart
// ❌ Wrong: Repository handling business logic
class CartRepository {
  Cart addItem(Cart cart, Product product) {
    // This is domain logic, not data access!
  }
}

// ✅ Correct: Domain extension
extension CartExtension on Cart {
  Cart addItem(Product product) {
    final items = Map<String, int>.from(this.items);
    items[product.id] = (items[product.id] ?? 0) + 1;
    return Cart(items);
  }
}
```

**UI state management** - Use Controllers/Notifiers
**App-wide coordination** - Use Application Services

## Abstract vs Concrete Repository

### The Debate

```dart
// Abstract approach
abstract class ProductsRepository {
  Future<List<Product>> fetchProducts();
}

class RemoteProductsRepository implements ProductsRepository {
  @override
  Future<List<Product>> fetchProducts() {
    // implementation
  }
}

// Concrete approach (Andrea's preference)
class ProductsRepository {
  const ProductsRepository(this._httpClient);
  final HttpClient _httpClient;

  Future<List<Product>> fetchProducts() {
    // implementation
  }
}
```

### Andrea's Stance: Prefer Concrete

**Reasoning:**
- **"Most cases only need one implementation"**
- Abstract classes add boilerplate without benefit
- IDE "Go to Definition" jumps to implementation directly
- Easier to read and understand
- Testing still straightforward with provider overrides

**When to use Abstract:**
- Multiple implementations actually exist (rare)
- Switching implementations at runtime
- Library code with extensibility requirements

### Testing Without Abstraction

```dart
// Concrete repository
class ProductsRepository {
  const ProductsRepository(this._client);
  final HttpClient _client;

  Future<List<Product>> fetchProducts() => _client.get('/products');
}

// Provider definition
@riverpod
ProductsRepository productsRepository(ProductsRepositoryRef ref) {
  return ProductsRepository(ref.watch(httpClientProvider));
}

// Test with override - no abstract class needed!
testWidgets('Products screen shows products', (tester) async {
  final mockRepo = MockProductsRepository(); // Mock the concrete class
  when(mockRepo.fetchProducts()).thenAnswer((_) async => [testProduct]);

  await tester.pumpWidget(
    ProviderScope(
      overrides: [
        productsRepositoryProvider.overrideWithValue(mockRepo),
      ],
      child: ProductsScreen(),
    ),
  );

  expect(find.text(testProduct.name), findsOneWidget);
});
```

## Avoiding Leaky Abstractions

### What is a Leaky Abstraction?

**Definition:** When implementation details "leak" through the abstraction layer, forcing consumers to know about the underlying technology.

### Examples of Leaky Abstractions

#### ❌ Example 1: Exposing Backend-Specific Types

```dart
// Leaky: Exposes Firestore Query type
class ItemsRepository {
  Stream<Query<Item>> watchItems() {
    return _firestore.collection('items').snapshots(); // Query<Item> is Firebase-specific!
  }
}

// Widget now depends on Firebase
class ItemsList extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final queryStream = ref.watch(itemsProvider);
    // Must understand Firestore Query to use this!
  }
}
```

```dart
// ✅ Clean: Backend-independent interface
class ItemsRepository {
  Stream<List<Item>> watchItems() {
    return _firestore.collection('items')
        .snapshots()
        .map((snapshot) => snapshot.docs.map((doc) => Item.fromJson(doc.data())).toList());
  }
}

// Widget only knows about domain model
class ItemsList extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final itemsStream = ref.watch(itemsProvider);
    // Works with List<Item>, no Firebase knowledge needed
  }
}
```

#### ❌ Example 2: Exposing HTTP Response Details

```dart
// Leaky: Exposes http.Response
class UserRepository {
  Future<http.Response> getUser(String id) async {
    return await _httpClient.get('/users/$id');
  }
}

// Caller must handle HTTP parsing
final response = await repo.getUser('123');
if (response.statusCode == 200) {
  final user = User.fromJson(jsonDecode(response.body));
}
```

```dart
// ✅ Clean: Returns domain model
class UserRepository {
  Future<User> getUser(String id) async {
    final response = await _httpClient.get('/users/$id');
    if (response.statusCode == 200) {
      return User.fromJson(jsonDecode(response.body));
    } else {
      throw UserNotFoundException(id);
    }
  }
}

// Caller works with domain model
final user = await repo.getUser('123');
```

### The Tradeoff: Clean Abstractions vs Feature Loss

**Andrea's Warning:** "Don't create lowest-common-denominator APIs that sacrifice real features"

#### Example: Pagination with Firestore

Firestore has powerful pagination with `startAfter` cursors. Creating a backend-agnostic pagination API might sacrifice this:

```dart
// Option A: Clean but limited
class ItemsRepository {
  Future<List<Item>> fetchItems({int page = 1, int limit = 20}) async {
    // Works for REST APIs but loses Firestore cursor benefits
    return _firestore.collection('items')
        .limit(limit)
        .skip((page - 1) * limit) // Skip is inefficient in Firestore!
        .get();
  }
}

// Option B: Firestore-specific but efficient
class ItemsRepository {
  Future<List<Item>> fetchItems({DocumentSnapshot? startAfter, int limit = 20}) async {
    Query query = _firestore.collection('items').limit(limit);
    if (startAfter != null) {
      query = query.startAfterDocument(startAfter);
    }
    // Uses efficient cursor pagination
    return query.get();
  }
}
```

**Andrea's advice:**
- Prefer clean abstractions for common cases
- Accept backend-specific APIs when features justify it
- Document when leakage is intentional
- **Don't prematurely abstract away valuable features**

## Repository Implementation Patterns

### Basic Repository Template

```dart
@riverpod
class ProductsRepository {
  const ProductsRepository(this._httpClient);
  final HttpClient _httpClient;

  // Fetch operations
  Future<List<Product>> fetchProducts() async {
    final response = await _httpClient.get('/products');
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Product.fromJson(json)).toList();
    } else {
      throw FetchProductsException();
    }
  }

  Future<Product> fetchProduct(String id) async {
    final response = await _httpClient.get('/products/$id');
    if (response.statusCode == 200) {
      return Product.fromJson(jsonDecode(response.body));
    } else if (response.statusCode == 404) {
      throw ProductNotFoundException(id);
    } else {
      throw FetchProductException(id);
    }
  }

  // Mutation operations
  Future<void> createProduct(Product product) async {
    final response = await _httpClient.post(
      '/products',
      body: jsonEncode(product.toJson()),
    );
    if (response.statusCode != 201) {
      throw CreateProductException();
    }
  }

  Future<void> updateProduct(Product product) async {
    final response = await _httpClient.put(
      '/products/${product.id}',
      body: jsonEncode(product.toJson()),
    );
    if (response.statusCode != 200) {
      throw UpdateProductException(product.id);
    }
  }

  Future<void> deleteProduct(String id) async {
    final response = await _httpClient.delete('/products/$id');
    if (response.statusCode != 204) {
      throw DeleteProductException(id);
    }
  }
}

// Provider definition
@riverpod
ProductsRepository productsRepository(ProductsRepositoryRef ref) {
  return ProductsRepository(ref.watch(httpClientProvider));
}
```

### Repository with Caching

```dart
class ProductsRepository {
  ProductsRepository(this._httpClient);
  final HttpClient _httpClient;

  // In-memory cache
  List<Product>? _cachedProducts;
  DateTime? _lastFetchTime;
  static const _cacheDuration = Duration(minutes: 5);

  Future<List<Product>> fetchProducts({bool forceRefresh = false}) async {
    // Return cache if valid
    if (!forceRefresh &&
        _cachedProducts != null &&
        _lastFetchTime != null &&
        DateTime.now().difference(_lastFetchTime!) < _cacheDuration) {
      return _cachedProducts!;
    }

    // Fetch from network
    final response = await _httpClient.get('/products');
    if (response.statusCode == 200) {
      final products = (jsonDecode(response.body) as List)
          .map((json) => Product.fromJson(json))
          .toList();

      // Update cache
      _cachedProducts = products;
      _lastFetchTime = DateTime.now();

      return products;
    } else {
      throw FetchProductsException();
    }
  }

  // Invalidate cache after mutations
  Future<void> createProduct(Product product) async {
    await _httpClient.post('/products', body: jsonEncode(product.toJson()));
    _invalidateCache();
  }

  void _invalidateCache() {
    _cachedProducts = null;
    _lastFetchTime = null;
  }
}
```

### Repository with Local + Remote (Offline Support)

```dart
class ProductsRepository {
  ProductsRepository(this._remoteApi, this._localDb);
  final RemoteApi _remoteApi;
  final LocalDatabase _localDb;

  Future<List<Product>> fetchProducts() async {
    try {
      // Try remote first
      final remoteProducts = await _remoteApi.getProducts();

      // Update local cache
      await _localDb.saveProducts(remoteProducts);

      return remoteProducts;
    } on NetworkException {
      // Fallback to local cache on network error
      return await _localDb.getProducts();
    }
  }

  Stream<List<Product>> watchProducts() {
    // Return local data immediately, then sync with remote
    return _localDb.watchProducts().asyncMap((localProducts) async {
      try {
        final remoteProducts = await _remoteApi.getProducts();
        await _localDb.saveProducts(remoteProducts);
        return remoteProducts;
      } catch (e) {
        return localProducts; // Return cached data on error
      }
    });
  }
}
```

## Repository Error Handling

### Throw Specific Exceptions

```dart
// Define domain-specific exceptions
class ProductNotFoundException implements Exception {
  const ProductNotFoundException(this.productId);
  final String productId;

  @override
  String toString() => 'Product with ID $productId not found';
}

class FetchProductsException implements Exception {
  const FetchProductsException([this.message]);
  final String? message;

  @override
  String toString() => 'Failed to fetch products${message != null ? ': $message' : ''}';
}

// Repository throws specific exceptions
class ProductsRepository {
  Future<Product> fetchProduct(String id) async {
    try {
      final response = await _httpClient.get('/products/$id');
      if (response.statusCode == 200) {
        return Product.fromJson(jsonDecode(response.body));
      } else if (response.statusCode == 404) {
        throw ProductNotFoundException(id);
      } else {
        throw FetchProductsException('HTTP ${response.statusCode}');
      }
    } on SocketException {
      throw FetchProductsException('No internet connection');
    } on FormatException {
      throw FetchProductsException('Invalid response format');
    }
  }
}
```

## Testing Repositories

### Unit Testing with Mocks

```dart
class MockHttpClient extends Mock implements HttpClient {}

void main() {
  late ProductsRepository repository;
  late MockHttpClient mockClient;

  setUp(() {
    mockClient = MockHttpClient();
    repository = ProductsRepository(mockClient);
  });

  test('fetchProducts returns list of products on success', () async {
    // Arrange
    when(mockClient.get('/products')).thenAnswer(
      (_) async => http.Response('[{"id": "1", "name": "Product 1"}]', 200),
    );

    // Act
    final products = await repository.fetchProducts();

    // Assert
    expect(products, hasLength(1));
    expect(products.first.id, '1');
    expect(products.first.name, 'Product 1');
  });

  test('fetchProducts throws exception on network error', () async {
    // Arrange
    when(mockClient.get('/products')).thenThrow(SocketException('No internet'));

    // Act & Assert
    expect(
      () => repository.fetchProducts(),
      throwsA(isA<FetchProductsException>()),
    );
  });
}
```

## Key Principles Summary

1. **Repository is a gateway** - Domain ↔ Data Source boundary
2. **Prefer concrete classes** - Abstract only when multiple implementations exist
3. **Avoid leaky abstractions** - But don't sacrifice real features
4. **Throw domain exceptions** - Not infrastructure exceptions
5. **Handle caching if needed** - In-memory or local database
6. **Test with mocks** - Override providers in widget tests

## References

- [Flutter App Architecture: The Repository Pattern](https://codewithandrea.com/articles/flutter-repository-pattern/)
- [How to use Abstraction and the Repository Pattern Effectively](https://codewithandrea.com/articles/abstraction-repository-pattern-flutter/)
