import React, { useState, useEffect } from 'react';
import { stockAlertsApi, productsApi, locationsApi } from '../services/api';
import { StockAlert, Product, Location } from '../types';
import ConfirmDialog from '../components/ConfirmDialog';

const StockAlerts: React.FC = () => {
  const [alerts, setAlerts] = useState<StockAlert[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [locations, setLocations] = useState<Location[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterStatus, setFilterStatus] = useState<string>('');
  const [filterSeverity, setFilterSeverity] = useState<string>('');
  const [filterProduct, setFilterProduct] = useState<number | ''>('');
  const [filterLocation, setFilterLocation] = useState<number | ''>('');
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [alertToDelete, setAlertToDelete] = useState<StockAlert | null>(null);
  const [showResolveDialog, setShowResolveDialog] = useState(false);
  const [alertToResolve, setAlertToResolve] = useState<StockAlert | null>(null);
  const [resolutionData, setResolutionData] = useState({
    resolved_by: '',
    resolution_notes: '',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [alertsData, productsData, locationsData] = await Promise.all([
        stockAlertsApi.getAll(),
        productsApi.getAll(),
        locationsApi.getAll()
      ]);
      setAlerts(alertsData);
      setProducts(productsData);
      setLocations(locationsData);
    } catch (err) {
      setError('Failed to load stock alerts');
      console.error('Error loading stock alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = (alert: StockAlert) => {
    setAlertToDelete(alert);
    setShowDeleteDialog(true);
  };

  const confirmDelete = async () => {
    if (!alertToDelete) return;

    try {
      await stockAlertsApi.delete(alertToDelete.id);
      setAlerts(alerts.filter(alert => alert.id !== alertToDelete.id));
      setShowDeleteDialog(false);
      setAlertToDelete(null);
    } catch (err) {
      setError('Failed to delete alert');
      console.error('Error deleting alert:', err);
    }
  };

  const handleAcknowledge = async (alert: StockAlert) => {
    try {
      const updatedAlert = await stockAlertsApi.acknowledge(alert.id);
      setAlerts(alerts.map(a => a.id === alert.id ? updatedAlert : a));
    } catch (err) {
      setError('Failed to acknowledge alert');
      console.error('Error acknowledging alert:', err);
    }
  };

  const handleResolve = (alert: StockAlert) => {
    setAlertToResolve(alert);
    setResolutionData({
      resolved_by: '',
      resolution_notes: '',
    });
    setShowResolveDialog(true);
  };

  const confirmResolve = async () => {
    if (!alertToResolve) return;

    try {
      const updatedAlert = await stockAlertsApi.resolve(alertToResolve.id, resolutionData);
      setAlerts(alerts.map(a => a.id === alertToResolve.id ? updatedAlert : a));
      setShowResolveDialog(false);
      setAlertToResolve(null);
    } catch (err) {
      setError('Failed to resolve alert');
      console.error('Error resolving alert:', err);
    }
  };

  const filteredAlerts = alerts.filter(alert => {
    if (filterStatus && alert.status !== filterStatus) return false;
    if (filterSeverity && alert.severity !== filterSeverity) return false;
    if (filterProduct && alert.product_id !== filterProduct) return false;
    if (filterLocation && alert.location_id !== filterLocation) return false;
    return true;
  });

  const getProductName = (productId: number) => {
    const product = products.find(p => p.id === productId);
    return product?.name || 'Unknown';
  };

  const getLocationName = (locationId?: number) => {
    if (!locationId) return 'All Locations';
    const location = locations.find(l => l.id === locationId);
    return location?.name || 'Unknown';
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 text-red-800';
      case 'high':
        return 'bg-orange-100 text-orange-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-red-100 text-red-800';
      case 'acknowledged':
        return 'bg-yellow-100 text-yellow-800';
      case 'resolved':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getAlertTypeIcon = (alertType: string) => {
    switch (alertType) {
      case 'low_stock':
        return (
          <svg className="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        );
      case 'out_of_stock':
        return (
          <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        );
      case 'expiring_soon':
        return (
          <svg className="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      case 'overstock':
        return (
          <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
        );
      default:
        return (
          <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString() + ' ' + new Date(dateString).toLocaleTimeString();
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Stock Alerts</h1>
        <div className="text-sm text-gray-500">
          {alerts.filter(a => a.status === 'active').length} active alerts
        </div>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Filters</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Status</option>
              <option value="active">Active</option>
              <option value="acknowledged">Acknowledged</option>
              <option value="resolved">Resolved</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Severity
            </label>
            <select
              value={filterSeverity}
              onChange={(e) => setFilterSeverity(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Severity</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Product
            </label>
            <select
              value={filterProduct}
              onChange={(e) => setFilterProduct(e.target.value ? Number(e.target.value) : '')}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Products</option>
              {products.map(product => (
                <option key={product.id} value={product.id}>
                  {product.name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Location
            </label>
            <select
              value={filterLocation}
              onChange={(e) => setFilterLocation(e.target.value ? Number(e.target.value) : '')}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Locations</option>
              {locations.map(location => (
                <option key={location.id} value={location.id}>
                  {location.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Alerts List */}
      <div className="space-y-4">
        {filteredAlerts.map((alert) => (
          <div key={alert.id} className="bg-white shadow rounded-lg p-6">
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                    {getAlertTypeIcon(alert.alert_type)}
                  </div>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2 mb-2">
                    <h3 className="text-lg font-medium text-gray-900">{alert.title}</h3>
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSeverityColor(alert.severity)}`}>
                      {alert.severity.charAt(0).toUpperCase() + alert.severity.slice(1)}
                    </span>
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(alert.status)}`}>
                      {alert.status.charAt(0).toUpperCase() + alert.status.slice(1)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{alert.message}</p>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-500">
                    <div>
                      <span className="font-medium">Product:</span> {getProductName(alert.product_id)}
                    </div>
                    <div>
                      <span className="font-medium">Location:</span> {getLocationName(alert.location_id)}
                    </div>
                    <div>
                      <span className="font-medium">Current Stock:</span> {alert.current_quantity}
                    </div>
                    <div>
                      <span className="font-medium">Threshold:</span> {alert.threshold_quantity}
                    </div>
                  </div>
                  <div className="mt-2 text-xs text-gray-400">
                    Created: {formatDate(alert.created_at)}
                    {alert.resolved_at && ` • Resolved: ${formatDate(alert.resolved_at)}`}
                  </div>
                </div>
              </div>
              <div className="flex flex-col space-y-2">
                {alert.status === 'active' && (
                  <>
                    <button
                      onClick={() => handleAcknowledge(alert)}
                      className="text-sm bg-yellow-100 text-yellow-800 px-3 py-1 rounded hover:bg-yellow-200"
                    >
                      Acknowledge
                    </button>
                    <button
                      onClick={() => handleResolve(alert)}
                      className="text-sm bg-green-100 text-green-800 px-3 py-1 rounded hover:bg-green-200"
                    >
                      Resolve
                    </button>
                  </>
                )}
                <button
                  onClick={() => handleDelete(alert)}
                  className="text-sm bg-red-100 text-red-800 px-3 py-1 rounded hover:bg-red-200"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))}
        
        {filteredAlerts.length === 0 && (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <div className="text-gray-500 text-lg">No stock alerts found</div>
            <div className="mt-2 text-sm text-gray-400">
              Alerts will appear here when stock levels fall below thresholds
            </div>
          </div>
        )}
      </div>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={showDeleteDialog}
        onClose={() => {
          setShowDeleteDialog(false);
          setAlertToDelete(null);
        }}
        onConfirm={confirmDelete}
        title="Delete Alert"
        message={`Are you sure you want to delete this alert "${alertToDelete?.title}"? This action cannot be undone.`}
        confirmText="Delete"
        cancelText="Cancel"
        type="danger"
      />

      {/* Resolve Dialog */}
      {showResolveDialog && alertToResolve && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true">
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>

            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div className="sm:flex sm:items-start">
                  <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-green-100 sm:mx-0 sm:h-10 sm:w-10">
                    <svg className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                    <h3 className="text-lg leading-6 font-medium text-gray-900">
                      Resolve Alert
                    </h3>
                    <div className="mt-2">
                      <p className="text-sm text-gray-500">
                        Mark this alert as resolved: {alertToResolve.title}
                      </p>
                      <div className="mt-4 space-y-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700">
                            Resolved By *
                          </label>
                          <input
                            type="text"
                            value={resolutionData.resolved_by}
                            onChange={(e) => setResolutionData(prev => ({
                              ...prev,
                              resolved_by: e.target.value
                            }))}
                            required
                            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">
                            Resolution Notes
                          </label>
                          <textarea
                            value={resolutionData.resolution_notes}
                            onChange={(e) => setResolutionData(prev => ({
                              ...prev,
                              resolution_notes: e.target.value
                            }))}
                            rows={3}
                            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                <button
                  type="button"
                  onClick={confirmResolve}
                  disabled={!resolutionData.resolved_by.trim()}
                  className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-green-600 text-base font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
                >
                  Resolve Alert
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowResolveDialog(false);
                    setAlertToResolve(null);
                  }}
                  className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StockAlerts;
