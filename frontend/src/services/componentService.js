import apiClient from '../lib/apiClient';

export const componentService = {
  // List all components
  async listComponents() {
    try {
      const response = await apiClient.get('/api/v1/components');
      return response.data;
    } catch (error) {
      console.error('Error fetching components:', error);
      throw error;
    }
  },

  // Create new component
  async createComponent(componentData) {
    try {
      const response = await apiClient.post('/api/v1/components', componentData);
      return response.data;
    } catch (error) {
      console.error('Error creating component:', error);
      throw error;
    }
  },

  // Get component by ID
  async getComponent(componentId) {
    try {
      const response = await apiClient.get(`/api/v1/components/${componentId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching component:', error);
      throw error;
    }
  },

  // Update component
  async updateComponent(componentId, componentData) {
    try {
      const response = await apiClient.put(`/api/v1/components/${componentId}`, componentData);
      return response.data;
    } catch (error) {
      console.error('Error updating component:', error);
      throw error;
    }
  },

  // Delete component
  async deleteComponent(componentId) {
    try {
      const response = await apiClient.delete(`/api/v1/components/${componentId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting component:', error);
      throw error;
    }
  }
};
