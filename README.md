# Access Watch - Telex Integration

## Overview
Access Watch is a security monitoring integration that tracks user access attempts to sensitive data. This integration works with Telex to log unauthorized access attempts and notify the team in real-time. It ensures that access control policies are enforced and potential security threats are identified promptly.

## Telex Integration Setup
1. **Sign up on Telex**: [Telex Sign-Up](https://telex.im/auth/sign-up)
2. **Create an Organization and Channel**
   - After signing up, create an organization and a channel where notifications will be sent.
3. **Set Up the Integration**
   - In Telex, create a new app integration.
   - Use the integration JSON URL: `/integration.json` from your deployed instance.

## Deployment on Render
This project is configured to be deployed on [Render](https://render.com) without additional setup.

### 1. Create a Database on Render
- Go to Render and create a new PostgreSQL database.
- Copy the connection string and set it as `DATABASE_URL` in your Render environment variables.

### 2. Deploy the Application
- Create a new Web Service on Render.
- Connect your GitHub repository: [Access Watch Repo](https://github.com/telexintegrations/access-watch-telex.git)
- Set up environment variables (`DATABASE_URL`, `SECRET_KEY`, `WEB_CONCURRENCY=4`).
- The `build.sh` script in the project already includes all necessary commands for database migration and cache table creation.
- Start the service.

## Testing the Integration
After deploying, test the integration by triggering secured access attempts.

### 1. Register and Login
Use the provided authentication endpoints to create a user and obtain a token.

### BASE URL
https://access-watch-ix9w.onrender.com

#### Register
```http
POST /api/v1/users/
Content-Type: application/json
{
    "username": "testuser",
    "password": "securepassword"
}
```

#### Login
```http
POST /api/v1/users/login/
Content-Type: application/json
{
    "username": "testuser",
    "password": "securepassword"
}
```
This will return an access token that must be included in requests to protected endpoints.

### 2. Test Role-Based Access
Once logged in, try accessing secured endpoints. Unauthorized attempts will be logged and sent to Telex.

```http
GET /api/v1/secured-data/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

If the user does not have the required permissions, the attempt will be logged in Telex.

## Testing Integration on Test Telex Organization
Notifications will be sent to the *access watch telex* channel.

To test quickly, users can make a request to a protected endpoint **without an authentication token**. The integration checks for two types of users:
1. **Anonymous users** (no authentication token provided)
2. **Authenticated but unauthorized users** (valid token, but no permission)

### Quick Testing as an Anonymous User
Users can test easily as anonymous users by simply making a request to a protected endpoint without a token:
```http
GET [/api/v1/secured-data/](https://access-watch-ix9w.onrender.com/api/v1/secured-data)
```
This will immediately trigger a notification in the *access watch telex* channel.

### Testing as an Authenticated User
To test as an authenticated but unauthorized user:
1. **Sign up** following the step in the register section above.
2. **Login** to get an access token.
3. **Make a request** to the protected endpoint with the token.

If the user does not have the necessary permissions, the access attempt will be logged immediately in the *access watch telex* channel.

## Screenshots
Example notification on Test Telex organization in *access watch telex* channel
![Telex Logs](https://github.com/user-attachments/assets/c2246be6-c88d-47cb-a68d-8b59476c815d)

![Create integration app](https://github.com/user-attachments/assets/a4a9419d-f28f-4d16-b448-cdbf4640547b)
