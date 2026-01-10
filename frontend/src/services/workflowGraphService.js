import apiClient from '../lib/apiClient';

export const workflowGraphService = {
  // Get a specific workflow graph by ID
  async getWorkflowGraph(workflowId) {
    try {
      const response = await apiClient.get(`/api/v1/workflow-graph/${workflowId}/graph`);
      return response.data;
    } catch (error) {
      console.error('Error fetching workflow graph:', error);
      throw error;
    }
  },
}
