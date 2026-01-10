import React from 'react';
import { ReactFlowProvider } from 'reactflow';
import WorkflowBuilder from '../components/WorkflowBuilder';

export default function WorkflowPage() {
  return (
    <ReactFlowProvider>
      <WorkflowBuilder />
    </ReactFlowProvider>
  );
}
