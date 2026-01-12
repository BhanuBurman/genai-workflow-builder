import apiClient from '../lib/apiClient';

export const workflowService = {
  // List all workflows
  async listWorkflows() {
    try {
      const response = await apiClient.get('/api/v1/workflows');
      return response.data;
    } catch (error) {
      console.error('Error fetching workflows:', error);
      throw error;
    }
  },

  // Create new workflow
  async createWorkflow(workflowData) {
    try {
      const response = await apiClient.post('/api/v1/workflows', workflowData);
      return response.data;
    } catch (error) {
      console.error('Error creating workflow:', error);
      throw error;
    }
  },

  // Get workflow by ID
  async getWorkflow(workflowId) {
    try {
      const response = await apiClient.get(`/api/v1/workflows/${workflowId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching workflow:', error);
      throw error;
    }
  },

  // Update workflow
  async updateWorkflow(workflowId, workflowData) {
    try {
      const response = await apiClient.put(`/api/v1/workflows/${workflowId}`, workflowData);
      return response.data;
    } catch (error) {
      console.error('Error updating workflow:', error);
      throw error;
    }
  },

  // Delete workflow
  async deleteWorkflow(workflowId) {
    try {
      const response = await apiClient.delete(`/api/v1/workflows/${workflowId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting workflow:', error);
      throw error;
    }
  },

  // Execute workflow
  async executeWorkflow(workflowId) {
    try {
      const response = await apiClient.post(`/api/v1/workflows/${workflowId}/execute`);
      return response.data;
    } catch (error) {
      console.error('Error executing workflow:', error);
      throw error;
    }
  },

  // Get workflow execution status
  async getWorkflowStatus(workflowId) {
    try {
      const response = await apiClient.get(`/api/v1/workflows/${workflowId}/status`);
      return response.data;
    } catch (error) {
      console.error('Error fetching workflow status:', error);
      throw error;
    }
  },

  // Get nodes in workflow
  async getWorkflowNodes(workflowId) {
    try {
      const response = await apiClient.get(`/api/v1/workflows/${workflowId}/nodes`);
      return response.data;
    } catch (error) {
      console.error('Error fetching workflow nodes:', error);
      throw error;
    }
  },

  // Get edges in workflow
  async getWorkflowEdges(workflowId) {
    try {
      const response = await apiClient.get(`/api/v1/workflows/${workflowId}/edges`);
      return response.data;
    } catch (error) {
      console.error('Error fetching workflow edges:', error);
      throw error;
    }
  },

  // Build workflow (validate the graph structure)
  async buildWorkflow(payload) {
    try {
      const response = await apiClient.post('/api/v1/workflows/build', payload);
      return response.data;
    } catch (error) {
      console.error('Error building workflow:', error);
      throw error;
    }
  },

  // Run workflow with workflow_id and message
  async runWorkflow(workflowId, message) {
    try {
      const response = await apiClient.post('/api/v1/workflows/run', {
        workflow_id: workflowId,
        message
      });
      return response.data;
    } catch (error) {
      console.error('Error running workflow:', error);
      throw error;
    }
  }
};
