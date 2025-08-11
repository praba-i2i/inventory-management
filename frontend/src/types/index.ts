export interface Category {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Item {
  id: number;
  name: string;
  description?: string;
  sku?: string;
  category_id?: number;
  quantity: number;
  unit_price: number;
  reorder_level: number;
  location?: string;
  supplier?: string;
  created_at: string;
  updated_at: string;
  category?: Category;
}

export interface CategoryCreate {
  name: string;
  description?: string;
}

export interface CategoryUpdate {
  name?: string;
  description?: string;
}

export interface ItemCreate {
  name: string;
  description?: string;
  sku?: string;
  category_id?: number;
  quantity: number;
  unit_price: number;
  reorder_level: number;
  location?: string;
  supplier?: string;
}

export interface ItemUpdate {
  name?: string;
  description?: string;
  sku?: string;
  category_id?: number;
  quantity?: number;
  unit_price?: number;
  reorder_level?: number;
  location?: string;
  supplier?: string;
}

// New enhanced types for the inventory management system

export interface Supplier {
  id: number;
  name: string;
  code: string;
  description?: string;
  email?: string;
  phone?: string;
  website?: string;
  address_line1?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  tax_id?: string;
  payment_terms?: string;
  credit_limit?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Location {
  id: number;
  name: string;
  code: string;
  description?: string;
  type: 'warehouse' | 'store' | 'office' | 'other';
  address?: string;
  contact_person?: string;
  contact_phone?: string;
  capacity?: number;
  status: 'active' | 'inactive';
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: number;
  name: string;
  description?: string;
  sku: string;
  barcode?: string;
  category_id: number;
  specifications?: Record<string, any>;
  cost_price: number;
  selling_price: number;
  unit: string;
  is_active: boolean;
  is_featured: boolean;
  dimensions?: string;
  weight?: number;
  supplier_id?: number;
  created_at: string;
  updated_at: string;
  category?: Category;
  supplier?: Supplier;
  inventory_items?: InventoryItem[];
}

export interface InventoryItem {
  id: number;
  product_id: number;
  location_id: number;
  quantity: number;
  reserved_quantity: number;
  available_quantity: number;
  reorder_level: number;
  max_stock_level?: number;
  storage_location?: string;
  unit_cost: number;
  total_value: number;
  status: 'active' | 'inactive';
  notes?: string;
  created_at: string;
  updated_at: string;
  product?: Product;
  location?: Location;
}

export interface PurchaseOrder {
  id: number;
  po_number: string;
  supplier_id: number;
  order_date: string;
  expected_delivery_date?: string;
  status: 'draft' | 'ordered' | 'received' | 'cancelled';
  total_amount: number;
  tax_amount: number;
  shipping_amount: number;
  discount_amount: number;
  notes?: string;
  terms_conditions?: string;
  approved_by?: string;
  approved_at?: string;
  created_at: string;
  updated_at: string;
  supplier?: Supplier;
  items?: PurchaseOrderItem[];
}

export interface PurchaseOrderItem {
  id: number;
  purchase_order_id: number;
  product_id: number;
  quantity: number;
  unit_price: number;
  total_price: number;
  received_quantity: number;
  remaining_quantity: number;
  notes?: string;
  created_at: string;
  updated_at: string;
  product?: Product;
}

export interface StockAlert {
  id: number;
  alert_type: 'low_stock' | 'out_of_stock' | 'expiring_soon' | 'overstock';
  status: 'active' | 'acknowledged' | 'resolved';
  product_id: number;
  location_id?: number;
  title: string;
  message: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  current_quantity: number;
  threshold_quantity: number;
  is_email_sent: boolean;
  is_sms_sent: boolean;
  resolved_at?: string;
  resolved_by?: string;
  resolution_notes?: string;
  created_at: string;
  updated_at: string;
  product?: Product;
  location?: Location;
}

// Create/Update types
export interface SupplierCreate {
  name: string;
  code: string;
  description?: string;
  email?: string;
  phone?: string;
  website?: string;
  address_line1?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  tax_id?: string;
  payment_terms?: string;
  credit_limit?: number;
  is_active?: boolean;
}

export interface SupplierUpdate {
  name?: string;
  code?: string;
  description?: string;
  email?: string;
  phone?: string;
  website?: string;
  address_line1?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  tax_id?: string;
  payment_terms?: string;
  credit_limit?: number;
  is_active?: boolean;
}

export interface LocationCreate {
  name: string;
  code: string;
  description?: string;
  type: 'warehouse' | 'store' | 'office' | 'other';
  address?: string;
  contact_person?: string;
  contact_phone?: string;
  capacity?: number;
  status?: 'active' | 'inactive';
}

export interface LocationUpdate {
  name?: string;
  code?: string;
  description?: string;
  type?: 'warehouse' | 'store' | 'office' | 'other';
  address?: string;
  contact_person?: string;
  contact_phone?: string;
  capacity?: number;
  status?: 'active' | 'inactive';
}

export interface ProductCreate {
  name: string;
  description?: string;
  sku: string;
  barcode?: string;
  category_id: number;
  specifications?: Record<string, any>;
  cost_price: number;
  selling_price: number;
  unit: string;
  is_active?: boolean;
  is_featured?: boolean;
  dimensions?: string;
  weight?: number;
  supplier_id?: number;
}

export interface ProductUpdate {
  name?: string;
  description?: string;
  sku?: string;
  barcode?: string;
  category_id?: number;
  specifications?: Record<string, any>;
  cost_price?: number;
  selling_price?: number;
  unit?: string;
  is_active?: boolean;
  is_featured?: boolean;
  dimensions?: string;
  weight?: number;
  supplier_id?: number;
}

export interface InventoryItemCreate {
  product_id: number;
  location_id: number;
  quantity: number;
  reserved_quantity?: number;
  reorder_level: number;
  max_stock_level?: number;
  storage_location?: string;
  unit_cost: number;
  status?: 'active' | 'inactive';
  notes?: string;
}

export interface InventoryItemUpdate {
  product_id?: number;
  location_id?: number;
  quantity?: number;
  reserved_quantity?: number;
  reorder_level?: number;
  max_stock_level?: number;
  storage_location?: string;
  unit_cost?: number;
  status?: 'active' | 'inactive';
  notes?: string;
}

export interface PurchaseOrderCreate {
  po_number: string;
  supplier_id: number;
  order_date: string;
  expected_delivery_date?: string;
  status?: 'draft' | 'ordered' | 'received' | 'cancelled';
  total_amount: number;
  tax_amount?: number;
  shipping_amount?: number;
  discount_amount?: number;
  notes?: string;
  terms_conditions?: string;
}

export interface PurchaseOrderUpdate {
  po_number?: string;
  supplier_id?: number;
  order_date?: string;
  expected_delivery_date?: string;
  status?: 'draft' | 'ordered' | 'received' | 'cancelled';
  total_amount?: number;
  tax_amount?: number;
  shipping_amount?: number;
  discount_amount?: number;
  notes?: string;
  terms_conditions?: string;
}

export interface PurchaseOrderItemCreate {
  purchase_order_id: number;
  product_id: number;
  quantity: number;
  unit_price: number;
  notes?: string;
}

export interface PurchaseOrderItemUpdate {
  product_id?: number;
  quantity?: number;
  unit_price?: number;
  received_quantity?: number;
  notes?: string;
}

export interface StockAlertCreate {
  alert_type: 'low_stock' | 'out_of_stock' | 'expiring_soon' | 'overstock';
  product_id: number;
  location_id?: number;
  title: string;
  message: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  current_quantity: number;
  threshold_quantity: number;
}

export interface StockAlertUpdate {
  alert_type?: 'low_stock' | 'out_of_stock' | 'expiring_soon' | 'overstock';
  status?: 'active' | 'acknowledged' | 'resolved';
  title?: string;
  message?: string;
  severity?: 'low' | 'medium' | 'high' | 'critical';
  current_quantity?: number;
  threshold_quantity?: number;
  resolved_by?: string;
  resolution_notes?: string;
}
