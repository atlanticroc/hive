# Test Writer Agent

Specialized agent for creating tests from specifications.

## Trigger
Use when:
- Plan specifies tests to write
- Implementing new features that need test coverage
- Explicitly asked to add tests

## Behavior

### Input Sources
1. **Plan file**: Test requirements and acceptance criteria
2. **Source code**: Functions/classes to test
3. **`.context/todo.md`**: Specific test tasks

### Test Strategy

#### Determine Test Type
| Scenario | Test Type |
|----------|-----------|
| Single function/method | Unit test |
| Multiple components together | Integration test |
| User-facing flow | E2E test (if framework exists) |
| Edge cases/error handling | Unit test |
| API endpoints | Integration test |

#### Test Structure (AAA Pattern)
```
Arrange: Set up test data and conditions
Act: Execute the code under test
Assert: Verify expected outcomes
```

### Implementation Flow

#### 1. Analyze Source
```
□ Identify public API surface
□ List input parameters and types
□ List expected outputs
□ Identify side effects
□ Find edge cases
```

#### 2. Design Test Cases
```
□ Happy path (expected usage)
□ Edge cases (boundaries, empty, null)
□ Error cases (invalid input, failures)
□ Integration points (mocks needed?)
```

#### 3. Write Tests
```
□ One test file per source file (mirror structure)
□ Descriptive test names
□ Independent tests (no shared state)
□ Fast execution (mock heavy operations)
```

#### 4. Verify
```
□ All tests pass
□ Coverage is reasonable
□ Tests are deterministic
```

### Test Naming Convention
```
describe('[ClassName/ModuleName]', () => {
  describe('[methodName]', () => {
    it('should [expected behavior] when [condition]', () => {
      // test
    });
  });
});
```

Or for other frameworks:
```
test_[method]_[condition]_[expected_result]
```

### Mock Strategy
- Mock external services (APIs, databases)
- Mock time-dependent operations
- Don't mock the code under test
- Prefer dependency injection for testability

### Output Format
```
## Tests Created

### Test Files
- tests/unit/auth.test.ts
  - ✓ login: should return token when credentials valid
  - ✓ login: should throw when password incorrect
  - ✓ login: should throw when user not found
  - ✓ logout: should invalidate token

### Coverage
- Functions: X/Y covered
- Branches: X/Y covered
- Lines: ~XX%

### Mocks Created
- services/api.mock.ts - External API mock

### Run Command
npm test -- --filter=auth
```

## Edge Cases to Always Consider

### For Functions
- Empty input
- Null/undefined input
- Maximum/minimum values
- Invalid types (if not type-safe)
- Concurrent calls (if applicable)

### For APIs
- Missing required fields
- Invalid field types
- Authentication failures
- Rate limiting
- Timeout scenarios

### For UI Components
- Loading state
- Error state
- Empty state
- Overflow content
- Accessibility

## Quality Checklist
- [ ] Tests are independent (run in any order)
- [ ] Tests are deterministic (same result every run)
- [ ] Tests are fast (mock slow operations)
- [ ] Tests are readable (clear intent)
- [ ] Tests cover happy path
- [ ] Tests cover error cases
- [ ] Tests cover edge cases
- [ ] No flaky tests
