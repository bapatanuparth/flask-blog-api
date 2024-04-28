# Flask API- Code Organization

The Flask Blog API is a structured and modular web application that allows for creating, retrieving, updating, and deleting blog posts. The application's codebase is organized into separate modules and directories, each with a specific role within the application. Here is an overview of the directory structure and the purpose of each component:

## **Directory Structure**

- **app/**: The main package for the Flask application containing all the necessary modules.
    - **auth/**: The authentication module responsible for user registration, login, and management.
        - **routes.py**: Contains all the route definitions for authentication endpoints.
    - **models/**: Contains ORM (Object-Relational Mapping) models defining the structure of database entities.
        - **post.py**: Defines the Post model for blog post data.
        - **token.py**: Defines the Token model for JWT token data.
        - **user.py**: Defines the User model for user data.
    - **post/**: The module responsible for blog post-related operations like CRUD actions.
        - **routes.py**: Contains the route definitions for post-related endpoints.
    - **token/**: A module for JWT token generation and validation.
        - **jwt_util.py**: Contains utility functions for JWT token operations.
    - **static/**: A directory to hold swagger.json
    - **config.py**: Contains configuration settings for the application, like database connection details for dev and test environment.
    - **extensions.py**: Initializes Mongo to be used in the entire application
    - **json_encoder.py**: Custom JSON encoder for handling MongoDB object serialization.
- **tests/**: Contains unit tests for the application.
    - **test_auth.py**: Tests related to the authentication functionality.
    - **test_posts.py**: Tests for blog post-related operations.
- **venv/**: The virtual environment directory where all the dependencies for the project are installed.
- **run.py**: The entry point script to run the Flask application.

## **Module Descriptions**

Code is divided into separate modules and routes leveraging Flask Blueprint to write a modular scalable and flexible code. This way of writing improves maintainability of the code as its segragated into logical parts and smaller manageable pieces. A modular application can be scaled more efficiently. Individual components can be updated or replaced without affecting the entire system. Also, well-organized and documented code makes it easier for new developers to understand the application architecture, the flow of data, and the functionality provided by different modules.

### **Auth Module**

Handles user authentication, including sign-up, login. It leverages **`bcrypt`** for password hashing and ensures secure management of user credentials.

### **Post Module**

Manages the blog posts, providing functionality to create new posts, retrieve existing posts, update posts, and delete posts. This module interacts with the **`posts`** collection in MongoDB and ensures that blog post data is handled correctly.

### **Token Module**

Manages the creation, distribution, and validation of JSON Web Tokens (JWT) for secure authentication and authorization throughout the application.

### **Models**

Defines the data structure for **`User`**, **`Post`**, and **`Token`**, used by MongoDB to store and retrieve data.

## **Utilities and Extensions**

- **Json Encoder**: Customizes the way MongoDB objects like **`ObjectId`** are serialized to JSON, which is particularly useful when sending MongoDB documents directly as JSON responses.
- **Mongo Extension**: Initializes Mongo

## **Tests**

Contains automated tests to ensure that authentication and post management features are working as expected. It uses Flask's testing client to simulate requests to the application and assert the responses.

# Design Choices

### MongoDB

MongoDB is schema-less, which means you can store documents without a predefined structure. This can be particularly useful for blog posts where the content structure might change over time. Also, MongoDB handles large volumes of data and traffic efficiently. It scales out with ease. It also allows you to quickly iterate on your application design without worrying about migrations typically required for schema changes in SQL databases.

### Flask

I have previous working experience with Flask. Flask gives the flexibility to use the tools and libraries you prefer. Flask Blueprints help structure the application in a modular way, allowing features or components to be developed independently.

### Modular Code

Modularity helps in organizing the codebase, making it cleaner and easier to navigate. Different modules can be developed and tested independently of one another, facilitating a more efficient development process.

# Trade offs

Setting up a modular structure can add some complexity upfront, as it requires careful planning and understanding of how components interact. For a very small scale application, modularity can add overhead.

MongoDB does not have transactional guarantee offered by RDBMS

# Feature Improvements that could be done

The program provides a functionality related to CRUD of blog posts

Improvements that could be done-

- Have a separate module to enhance validations and checking shape of incoming data to have more robust request validation
- Expand the test suite to include more comprehensive integration and end-to-end tests.
- currently only dev and test environments are present, prod env could be added
- The models are very basic for User and Post. They could have many more fields and also functionalities for other users to view and add comments on blog post could be added later on making application more complex.
- Introduce internationalization for global support
- If scaling needs arise, application could be refactored into into a microservices architecture.
- Later on queries could be optimized by caching, or database indexing on title, etc.
- Features like cache control could be used to protect access control after user logout
- Token removal functionality after certain time