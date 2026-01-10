import React from 'react';
import { Sparkles, Save } from 'lucide-react';
import { workflowService } from '../../services/workflowService';

export default function Header({ nodes, edges, onSave }) {
  
  const handleSave = async () => {
    const workflowData = {
        name: "My Workflow", // You might want to make this dynamic later
        flow_json: { nodes, edges },
        // Construct node configs for the separate table if needed
        node_configs: nodes.map(n => ({
            node_id: n.id,
            component_type: n.data.type,
            config_values: n.data.values || {}
        }))
    };
    
    // Call parent handler or service directly
    if(onSave) onSave(workflowData);
    else await workflowService.createWorkflow(workflowData);
    
    alert("Workflow saved!");
  };

  return (
    <header className="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-6 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-lg flex items-center justify-center">
          <Sparkles size={18} className="text-white" />
        </div>
        <span className="font-semibold text-gray-900 text-lg">GenAI Stack</span>
      </div>
      <button 
        onClick={handleSave}
        className="px-4 py-1.5 bg-white border border-gray-300 text-gray-700 rounded-md text-sm font-medium hover:bg-gray-50 transition-colors flex items-center gap-2"
      >
        <Save size={14} />
        Save
      </button>
    </header>
  );
}