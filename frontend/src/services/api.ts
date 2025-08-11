import axios from 'axios';
import { 
  Item, Category, ItemCreate, ItemUpdate, CategoryCreate, CategoryUpdate,
  Product, ProductCreate, ProductUpdate,
  Supplier, SupplierCreate, SupplierUpdate,
  Location, LocationCreate, LocationUpdate,
  InventoryItem, InventoryItemCreate, InventoryItemUpdate,
  PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate,
  PurchaseOrderItem, PurchaseOrderItemCreate, PurchaseOrderItemUpdate,
  StockAlert, StockAlertCreate, StockAlertUpdate
} from '../types';

// Force HTTPS in production to avoid mixed content issues
const getApiBaseUrl = () => {
  // If environment variable is set, use it
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // In production, always use HTTPS
  if (process.env.NODE_ENV === 'production') {
    return 'https://inventory-management-production-82d5.up.railway.app';
  }
  
  // In development, use localhost
  return 'http://localhost:8000';
};

const API_BASE_URL = getApiBaseUrl();

console.log('API Base URL:', API_BASE_URL);
console.log('Environment:', process.env.NODE_ENV);

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  // Handle redirects automatically
  maxRedirects: 5,
  // Force HTTPS in production
  timeout: 10000,
});

// Add request interceptor to log requests and ensure HTTPS
api.interceptors.request.use(request => {
  // Log all requests for debugging
  console.log('API Request:', request.method?.toUpperCase(), request.url);
  console.log('Full URL:', (request.baseURL || '') + (request.url || ''));
  
  // Ensure HTTPS in production
  if (process.env.NODE_ENV === 'production' && request.url && !request.url.startsWith('https://')) {
    console.warn('Non-HTTPS request detected in production:', request.url);
  }
  
  return request;
});

// Add response interceptor to handle errors
api.interceptors.response.use(
  response => {
    console.log('API Response:', response.status, response.config?.url);
    return response;
  },
  error => {
    console.error('API Error:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      url: error.config?.url,
      message: error.message,
      data: error.response?.data
    });
    
    // Handle mixed content errors specifically
    if (error.message && error.message.includes('mixed-content')) {
      console.error('Mixed Content Error: Frontend must be served over HTTPS to make HTTPS API calls');
    }
    
    // Handle redirect errors
    if (error.response?.status === 307) {
      console.error('Redirect Error: API is redirecting. Check if using correct protocol (HTTPS)');
    }
    
    return Promise.reject(error);
  }
);

// Items API
export const itemsApi = {
  getAll: async (): Promise<Item[]> => {
    const response = await api.get('/items');
    return response.data;
  },

  getById: async (id: number): Promise<Item> => {
    const response = await api.get(`/items/${id}`);
    return response.data;
  },

  create: async (item: ItemCreate): Promise<Item> => {
    const response = await api.post('/items', item);
    return response.data;
  },

  update: async (id: number, item: ItemUpdate): Promise<Item> => {
    const response = await api.put(`/items/${id}`, item);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/items/${id}`);
  },
};

// Categories API
export const categoriesApi = {
  getAll: async (): Promise<Category[]> => {
    const response = await api.get('/categories');
    return response.data;
  },

  getById: async (id: number): Promise<Category> => {
    const response = await api.get(`/categories/${id}`);
    return response.data;
  },

  create: async (category: CategoryCreate): Promise<Category> => {
    const response = await api.post('/categories', category);
    return response.data;
  },

  update: async (id: number, category: CategoryUpdate): Promise<Category> => {
    const response = await api.put(`/categories/${id}`, category);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/categories/${id}`);
  },
};

// Products API
export const productsApi = {
  getAll: async (params?: { 
    category_id?: number; 
    supplier_id?: number; 
    is_active?: boolean;
    include_inventory?: boolean;
  }): Promise<Product[]> => {
    const response = await api.get('/products', { params });
    return response.data;
  },

  getById: async (id: number): Promise<Product> => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  create: async (product: ProductCreate): Promise<Product> => {
    const response = await api.post('/products', product);
    return response.data;
  },

  update: async (id: number, product: ProductUpdate): Promise<Product> => {
    const response = await api.put(`/products/${id}`, product);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/products/${id}`);
  },
};

// Suppliers API
export const suppliersApi = {
  getAll: async (): Promise<Supplier[]> => {
    const response = await api.get('/suppliers');
    return response.data;
  },

  getById: async (id: number): Promise<Supplier> => {
    const response = await api.get(`/suppliers/${id}`);
    return response.data;
  },

  create: async (supplier: SupplierCreate): Promise<Supplier> => {
    const response = await api.post('/suppliers', supplier);
    return response.data;
  },

  update: async (id: number, supplier: SupplierUpdate): Promise<Supplier> => {
    const response = await api.put(`/suppliers/${id}`, supplier);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/suppliers/${id}`);
  },
};

// Locations API
export const locationsApi = {
  getAll: async (): Promise<Location[]> => {
    const response = await api.get('/locations');
    return response.data;
  },

  getById: async (id: number): Promise<Location> => {
    const response = await api.get(`/locations/${id}`);
    return response.data;
  },

  create: async (location: LocationCreate): Promise<Location> => {
    const response = await api.post('/locations', location);
    return response.data;
  },

  update: async (id: number, location: LocationUpdate): Promise<Location> => {
    const response = await api.put(`/locations/${id}`, location);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/locations/${id}`);
  },
};

// Inventory API
export const inventoryApi = {
  getAll: async (params?: {
    product_id?: number;
    location_id?: number;
    include_details?: boolean;
  }): Promise<InventoryItem[]> => {
    const response = await api.get('/inventory', { params });
    return response.data;
  },

  getSummary: async (): Promise<{
    total_items: number;
    total_value: number;
    low_stock_items: number;
    out_of_stock_items: number;
  }> => {
    const response = await api.get('/inventory/summary');
    return response.data;
  },

  getById: async (id: number): Promise<InventoryItem> => {
    const response = await api.get(`/inventory/${id}`);
    return response.data;
  },

  create: async (inventoryItem: InventoryItemCreate): Promise<InventoryItem> => {
    const response = await api.post('/inventory', inventoryItem);
    return response.data;
  },

  update: async (id: number, inventoryItem: InventoryItemUpdate): Promise<InventoryItem> => {
    const response = await api.put(`/inventory/${id}`, inventoryItem);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/inventory/${id}`);
  },

  adjust: async (id: number, adjustment: {
    quantity_change: number;
    reason: string;
    notes?: string;
  }): Promise<InventoryItem> => {
    const response = await api.post(`/inventory/${id}/adjust`, adjustment);
    return response.data;
  },
};

// Purchase Orders API
export const purchaseOrdersApi = {
  getAll: async (params?: {
    supplier_id?: number;
    status?: string;
    include_items?: boolean;
  }): Promise<PurchaseOrder[]> => {
    const response = await api.get('/purchase-orders', { params });
    return response.data;
  },

  getById: async (id: number): Promise<PurchaseOrder> => {
    const response = await api.get(`/purchase-orders/${id}`);
    return response.data;
  },

  create: async (purchaseOrder: PurchaseOrderCreate): Promise<PurchaseOrder> => {
    const response = await api.post('/purchase-orders', purchaseOrder);
    return response.data;
  },

  update: async (id: number, purchaseOrder: PurchaseOrderUpdate): Promise<PurchaseOrder> => {
    const response = await api.put(`/purchase-orders/${id}`, purchaseOrder);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/purchase-orders/${id}`);
  },

  // Purchase Order Items
  addItem: async (purchaseOrderId: number, item: PurchaseOrderItemCreate): Promise<PurchaseOrderItem> => {
    const response = await api.post(`/purchase-orders/${purchaseOrderId}/items`, item);
    return response.data;
  },

  updateItem: async (purchaseOrderId: number, itemId: number, item: PurchaseOrderItemUpdate): Promise<PurchaseOrderItem> => {
    const response = await api.put(`/purchase-orders/${purchaseOrderId}/items/${itemId}`, item);
    return response.data;
  },

  deleteItem: async (purchaseOrderId: number, itemId: number): Promise<void> => {
    await api.delete(`/purchase-orders/${purchaseOrderId}/items/${itemId}`);
  },
};

// Stock Alerts API
export const stockAlertsApi = {
  getAll: async (params?: {
    status?: string;
    severity?: string;
    product_id?: number;
    location_id?: number;
  }): Promise<StockAlert[]> => {
    const response = await api.get('/stock-alerts', { params });
    return response.data;
  },

  getById: async (id: number): Promise<StockAlert> => {
    const response = await api.get(`/stock-alerts/${id}`);
    return response.data;
  },

  create: async (stockAlert: StockAlertCreate): Promise<StockAlert> => {
    const response = await api.post('/stock-alerts', stockAlert);
    return response.data;
  },

  update: async (id: number, stockAlert: StockAlertUpdate): Promise<StockAlert> => {
    const response = await api.put(`/stock-alerts/${id}`, stockAlert);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/stock-alerts/${id}`);
  },

  acknowledge: async (id: number): Promise<StockAlert> => {
    const response = await api.post(`/stock-alerts/${id}/acknowledge`);
    return response.data;
  },

  resolve: async (id: number, resolution: {
    resolved_by: string;
    resolution_notes?: string;
  }): Promise<StockAlert> => {
    const response = await api.post(`/stock-alerts/${id}/resolve`, resolution);
    return response.data;
  },
};

export default api;
