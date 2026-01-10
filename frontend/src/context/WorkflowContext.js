import React, { createContext, useContext, useState, useCallback } from 'react';

const WorkflowContext = createContext();

export const useWorkflow = () => {
  const context = useContext(WorkflowContext);
  if (!context) {
    throw new Error('useWorkflow must be used within a WorkflowProvider');
  }
  return context;
};

export const WorkflowProvider = ({ children }) => {
  const [workflows, setWorkflows] = useState([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const addWorkflow = useCallback((workflow) => {
    setWorkflows(prev => [...prev, workflow]);
  }, []);

  const updateWorkflow = useCallback((workflowId, updatedData) => {
    setWorkflows(prev => prev.map(w => 
      w.id === workflowId ? { ...w, ...updatedData } : w
    ));
    if (selectedWorkflow && selectedWorkflow.id === workflowId) {
      setSelectedWorkflow(prev => ({ ...prev, ...updatedData }));
    }
  }, [selectedWorkflow]);

  const removeWorkflow = useCallback((workflowId) => {
    setWorkflows(prev => prev.filter(w => w.id !== workflowId));
    if (selectedWorkflow && selectedWorkflow.id === workflowId) {
      setSelectedWorkflow(null);
    }
  }, [selectedWorkflow]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const value = {
    workflows,
    selectedWorkflow,
    setSelectedWorkflow,
    isLoading,
    setIsLoading,
    error,
    setError,
    clearError,
    addWorkflow,
    updateWorkflow,
    removeWorkflow,
  };

  return (
    <WorkflowContext.Provider value={value}>
      {children}
    </WorkflowContext.Provider>
  );
};
