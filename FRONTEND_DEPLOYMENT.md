# Frontend Deployment Guide

This guide will help you deploy the React frontend to connect with your Railway backend.

## Backend URL Configuration

Your backend is successfully deployed at:
**https://inventory-management-production-82d5.up.railway.app**

## Frontend Configuration

The frontend has been configured to automatically use the Railway backend URL in production.

### API Configuration

The frontend will use:
- **Production**: `https://inventory-management-production-82d5.up.railway.app`
- **Development**: `http://localhost:8000`

### CORS Configuration

The backend is configured to allow requests from any origin, so the frontend should be able to connect without issues.

## Deployment Options

### Option 1: Deploy to Railway (Recommended)

1. **Create a new Railway project** for the frontend
2. **Connect your GitHub repository**
3. **Set the root directory** to `frontend/`
4. **Add build command**: `npm run build`
5. **Add start command**: `npm start` (for development) or serve the build folder

### Option 2: Deploy to Vercel

1. **Connect your GitHub repository** to Vercel
2. **Set the root directory** to `frontend/`
3. **Set build command**: `npm run build`
4. **Set output directory**: `build`

### Option 3: Deploy to Netlify

1. **Connect your GitHub repository** to Netlify
2. **Set the base directory** to `frontend/`
3. **Set build command**: `npm run build`
4. **Set publish directory**: `build`

## Environment Variables

If you need to override the API URL, set this environment variable:
```
REACT_APP_API_URL=https://inventory-management-production-82d5.up.railway.app
```

## Testing the Connection

After deployment, you can test the connection by:

1. **Opening your frontend application**
2. **Navigating to any page that makes API calls**
3. **Checking the browser's Network tab** to see if requests are going to the Railway backend
4. **Checking the browser's Console** for any CORS errors

## API Endpoints Available

Your backend provides these endpoints:
- **Health Check**: `https://inventory-management-production-82d5.up.railway.app/health`
- **API Documentation**: `https://inventory-management-production-82d5.up.railway.app/api/v1/docs`
- **Debug Info**: `https://inventory-management-production-82d5.up.railway.app/debug`

## Troubleshooting

### CORS Issues
If you encounter CORS errors:
1. Check that the backend is running
2. Verify the API URL is correct
3. Check the browser console for specific error messages

### API Connection Issues
If the frontend can't connect to the API:
1. Test the backend URL directly: `https://inventory-management-production-82d5.up.railway.app/health`
2. Check if the backend is responding
3. Verify the environment variables are set correctly

### Build Issues
If the frontend build fails:
1. Check that all dependencies are installed
2. Verify the TypeScript types are correct
3. Check for any import errors

## Quick Test

You can quickly test the backend connection by visiting:
- **Backend Health**: https://inventory-management-production-82d5.up.railway.app/health
- **API Docs**: https://inventory-management-production-82d5.up.railway.app/api/v1/docs

Both should return valid responses if the backend is working correctly.
