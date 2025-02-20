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

## Screenshots
![Telex Logs](https://github.com/user-attachments/assets/b9c9cdd1-2c6e-4d44-979d-59f805196cbc)

![Create integration app](https://github.com/user-attachments/assets/a4a9419d-f28f-4d16-b448-cdbf4640547b)