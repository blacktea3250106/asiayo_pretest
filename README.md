# Asiayo Pre-test: Order Validation and Transformation API

This Django-based API performs order format validation and transformation based on provided inputs. The API follows SOLID principles and design patterns to ensure clean, maintainable, and scalable code.

### Features:
- **POST `/api/orders`**: Validates and processes order data.
- Input format includes order ID, hotel name, address, price, and currency.
- Follows object-oriented design principles (SOLID) and design patterns for maintainability.
- Includes unit tests covering both success and failure scenarios.
- Dockerized environment for easy deployment.

### How to Run the Project:

#### Step 1: Clone the Repository
```bash
git clone https://github.com/blacktea3250106/asiayo_pretest.git
cd asiayo_pretest
```

#### Step 2: Build the Docker Containers
Ensure Docker and Docker Compose are installed, then run the following command to build and start the project:
```bash
docker-compose up --build
```

#### Step 3: Run Database Migrations
After the Docker environment is up, open a new terminal window and apply migrations:
```bash
docker-compose exec web python manage.py migrate
```

#### Step 4: Access the Application
Once the environment is running, access the application at:
```
http://localhost:8000
```

You can also access the automatically generated API documentation (Swagger UI) at:
```
http://localhost:8000/swagger/
```

### API Example

**Endpoint:**

`POST /api/orders`

**Request Body Example:**
```json
{
    "id": "A0000001",
    "name": "Melody Holiday Inn",
    "address": {
        "city": "taipei-city",
        "district": "da-an-district",
        "street": "fuxing-south-road"
    },
    "price": "2050",
    "currency": "TWD"
}
```

### Using `curl` to Test the API

You can also use `curl` to test the API from the command line.

**Example `curl` Request:**

```bash
curl -X POST http://localhost:8000/api/orders/ \
-H "Content-Type: application/json" \
-d '{
    "id": "A0000001",
    "name": "Melody Holiday Inn",
    "address": {
        "city": "taipei-city",
        "district": "da-an-district",
        "street": "fuxing-south-road"
    },
    "price": "2050",
    "currency": "TWD"
}'
```

This will send a POST request to the API endpoint and return the response. Ensure the Docker environment is running before using this command.

### Running Unit Tests:

To run the unit tests and ensure the API works as expected:
```bash
docker-compose exec web python manage.py test
```

---

### Explanation of Each Unit Test

Below is a detailed explanation of each unit test implemented in the project, covering various success and failure scenarios.

1. **`test_create_order_success`**:
   - **Purpose**: This test ensures that a valid order with all correct fields (`id`, `name`, `address`, `price`, and `currency`) successfully creates an order.
   - **Expected Behavior**: The API should return a `201 Created` response with the provided data in the response body, and all fields should match the input.

2. **`test_create_order_name_non_ascii`**:
   - **Purpose**: This test checks whether the API correctly handles an order where the `name` field contains non-ASCII characters (e.g., Japanese characters).
   - **Expected Behavior**: The API should return a `400 Bad Request` error, with an appropriate error message indicating that the name contains non-English characters.

3. **`test_create_order_name_not_capitalized`**:
   - **Purpose**: This test ensures that the API validates whether the `name` field is properly capitalized (i.e., each word in the name starts with a capital letter).
   - **Expected Behavior**: The API should return a `400 Bad Request` error if the name is not properly capitalized, along with an error message specifying the issue.

4. **`test_create_order_price_exceeds_limit`**:
   - **Purpose**: This test checks whether the API correctly handles cases where the `price` exceeds the allowed limit (in this case, greater than 2000).
   - **Expected Behavior**: The API should return a `400 Bad Request` error, with a message indicating that the price exceeds the limit.

5. **`test_create_order_invalid_currency`**:
   - **Purpose**: This test validates that the API properly checks for valid currency values. The accepted values are `TWD` and `USD`. This test uses an invalid currency (`EUR`).
   - **Expected Behavior**: The API should return a `400 Bad Request` error with a message indicating that the currency format is wrong.

6. **`test_create_order_success_with_usd`**:
   - **Purpose**: This test ensures that when the currency is `USD`, the API converts the `price` to `TWD` by multiplying the price by a conversion rate (in this case, 31).
   - **Expected Behavior**: The API should return a `201 Created` response, and the `price` should be converted to `TWD`. For example, if the `price` is 100 USD, the response should return 3100 TWD.

7. **`test_create_order_missing_fields`**:
   - **Purpose**: This test checks how the API handles requests where required fields are missing, such as `id`, `price`, or `currency`.
   - **Expected Behavior**: The API should return a `400 Bad Request` error for each missing field, with messages indicating which required fields are missing.

---

### Project Structure:
- `models.py`: Defines the database models for the orders.
- `serializers.py`: Contains the serializers for validating and transforming order data.
- `views.py`: Implements the API view logic using Django REST Framework.
- `urls.py`: URL routing for the API.
- `tests.py`: Unit tests for ensuring the functionality of the API.
- `docker-compose.yml`: Docker Compose configuration to run the project.
- `swagger.py`: Defines the Swagger schema and API documentation.

### SOLID Principles and Design Patterns:

1. **Single Responsibility Principle (SRP)**:
   - Each class in the system is responsible for a single part of the functionality. For instance, validation logic is encapsulated in the serializer, while the view handles the request-response cycle.

2. **Open/Closed Principle (OCP)**:
   - The code is open for extension but closed for modification. New validation or transformation logic can be added without modifying the existing code.

3. **Liskov Substitution Principle (LSP)**:
   - The classes and functions used for order validation can be replaced with subclasses without affecting the functionality.

4. **Interface Segregation Principle (ISP)**:
   - Small and specific interfaces are used. For example, validation logic is placed inside specific methods instead of adding too much responsibility to the view class.

5. **Dependency Inversion Principle (DIP)**:
   - High-level modules (like views) do not depend on low-level modules (like serializers). They depend on abstractions.

### Design Patterns:
- **Factory Pattern**: The validation and transformation logic is encapsulated in the serializer, making it easy to replace or extend without changing the view.
- **Strategy Pattern**: The API uses different validation methods for name, price, and currency, allowing easy replacement or addition of new strategies.

---

### Conclusion

This project demonstrates an API for validating and transforming order data, using Django, Django REST Framework, and Docker for an efficient and scalable environment. The project adheres to SOLID principles and uses design patterns to ensure maintainability and flexibility.
