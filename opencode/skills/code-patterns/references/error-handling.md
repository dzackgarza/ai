# Chapter 7: Error Handling

Many code bases are dominated by error handling—not because that’s all they do, but
because it’s impossible to see what the code does through all the scattered error
handling.

**Error handling is important, but if it obscures logic, it’s wrong.**

## Use Exceptions Rather Than Return Codes

**Note:** This skill is subordinate to repo-specific rules. In this environment, the
`code-patterns-python` skill's "fail fast, no speculative try/catch" doctrine takes
precedence over the patterns below. Exceptions are added only after observing a specific
failure, not pre-emptively. See the authority hierarchy in `quality-control`.

Return codes clutter the caller and are easy to forget:

```java
// Bad - cluttered with error checking
public void sendShutDown() {
    DeviceHandle handle = getHandle(DEV1);
    if (handle != DeviceHandle.INVALID) {
        retrieveDeviceRecord(handle);
        if (record.getStatus() != DEVICE_SUSPENDED) {
            pauseDevice(handle);
            clearDeviceWorkQueue(handle);
            closeDevice(handle);
        } else {
            logger.log("Device suspended. Unable to shut down");
        }
    } else {
        logger.log("Invalid handle");
    }
}

// Good - logic separated from error handling
public void sendShutDown() {
    try {
        tryToShutDown();
    } catch (DeviceShutDownError e) {
        logger.log(e);
    }
}

private void tryToShutDown() throws DeviceShutDownError {
    DeviceHandle handle = getHandle(DEV1);
    DeviceRecord record = retrieveDeviceRecord(handle);
    pauseDevice(handle);
    clearDeviceWorkQueue(handle);
    closeDevice(handle);
}
```

Two concerns (device shutdown algorithm and error handling) are now separated.
You can understand each independently.

## Handle Exceptions Only After Observing a Failure

Try blocks are like transactions—your catch must leave the program in a consistent
state.

**Do not add try/catch pre-emptively.** In this environment, the fail-loud policy
(`code-patterns-python`) takes precedence: add exception handling only after a specific
failure has been observed in practice. Start with assertions and let errors propagate.
See the authority hierarchy in `quality-control`.

When a specific failure has been observed, add the minimal exception handling needed,
keeping the happy path clear.

## Use Unchecked Exceptions

Checked exceptions violate the Open/Closed Principle.
If you throw a checked exception from a low-level function:

- Every function in the path must declare it in their signature

- Changes cascade from lowest to highest levels

- Encapsulation is broken (all functions know about low-level details)

C#, Python, Ruby don’t have checked exceptions—you can write robust software without
them.

## Provide Context with Exceptions

Each exception should provide enough context to determine source and location:

- Mention the operation that failed

- Mention the type of failure

- Include enough info for logging

Stack traces can’t tell you the *intent* of the failed operation.

## Define Exception Classes in Terms of a Caller’s Needs

Classify exceptions by **how they are caught**, not by source or type.

```java
// Bad - duplication, knows too much about third-party exceptions
try {
    port.open();
} catch (DeviceResponseException e) {
    reportPortError(e);
    logger.log("Device response exception", e);
} catch (ATM1212UnlockedException e) {
    reportPortError(e);
    logger.log("Unlock exception", e);
} catch (GMXError e) {
    reportPortError(e);
    logger.log("Device response exception");
}

// Good - wrap third-party API with common exception
LocalPort port = new LocalPort(12);
try {
    port.open();
} catch (PortDeviceFailure e) {
    reportError(e);
    logger.log(e.getMessage(), e);
}
```

**Wrapping third-party APIs is a best practice:**

- Defines an owned semantic boundary

- Centralizes contract validation

- Not tied to vendor's design choices

- Can define an API you like

Often a single exception class is fine.
Use different classes only when you need to catch one and let another pass through.

## Define the Normal Flow — With Domain-Semantic Special Cases Only

When a special case is a real domain semantic (not a defensive default), model it
explicitly:

```java
// Good - special case pattern for real domain semantics
MealExpenses expenses = expenseReportDAO.getMeals(employee.getID());
m_total += expenses.getTotal();
// DAO returns PerDiemMealExpenses when no meals, which returns per diem as total
```

**SPECIAL CASE PATTERN:** Create a class that handles the special case, so client code
doesn't deal with exceptional behavior.

**Restriction:** Special cases are allowed only when they encode explicit domain
semantics — not as soft defaults or defensive against conditions that should not occur.
In this environment, fail-loud policy (`code-patterns-python`) takes precedence: if an
impossible condition occurs, `assert False` is the correct response, not a special-case
object that silently absorbs the error. See the authority hierarchy in `quality-control`.

## Don’t Return Null

Returning null creates work and invites NullPointerExceptions:

```java
// Bad - null checks everywhere
public void registerItem(Item item) {
    if (item != null) {
        ItemRegistry registry = peristentStore.getItemRegistry();
        if (registry != null) {
            Item existing = registry.getItem(item.getID());
            if (existing.getBillingPeriod().hasRetailOwner()) {
                existing.register(item);
            }
        }
    }
}
```

What if `persistentStore` is null?
One missing check sends the application spinning.

**Instead:**

- Throw an exception

- Return a SPECIAL CASE object

- Return an empty collection

```java
// Bad
List<Employee> employees = getEmployees();
if (employees != null) {
    for (Employee e : employees) {
        totalPay += e.getPay();
    }
}

// Good - return empty list
List<Employee> employees = getEmployees();
for (Employee e : employees) {
    totalPay += e.getPay();
}

// In getEmployees:
return Collections.emptyList();  // Instead of null
```

## Don’t Pass Null

Passing null is worse than returning null.
There’s no good way to handle a null passed by a caller accidentally.

```java
public double xProjection(Point p1, Point p2) {
    return (p2.x – p1.x) * 1.5;
}

// If someone calls: calculator.xProjection(null, new Point(12, 13))
// We get NullPointerException
```

Options (all imperfect):

- Throw custom exception (must define handler)

- Use assertions (still runtime error)

**The rational approach: Forbid passing null by default.** Code with the knowledge that
null in arguments indicates a problem.

## Conclusion

Clean code is readable AND robust.
These aren’t conflicting goals.

See error handling as a separate concern, viewable independently of main logic.
To that degree, you can reason about it independently and make great strides in
maintainability.
