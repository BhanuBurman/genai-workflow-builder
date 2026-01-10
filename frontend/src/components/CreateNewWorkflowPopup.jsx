import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; 
// Assuming workflowService is imported here
import { workflowService } from "../services/workflowService";

const CreateNewWorkflowPopup = ({ onClose }) => {
  const navigate = useNavigate();
  
  // 1. State for form inputs
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [creating, setCreating] = useState(false);

  /* ---------------- Create Workflow ---------------- */
  const handleCreateWorkflow = async (e) => {
    e.preventDefault(); // Prevent browser refresh on form submit

    if (!name.trim()) return; // Basic validation

    try {
      setCreating(true);
      
      // 2. Use the state values here instead of hardcoded strings
      const result = await workflowService.createWorkflow({
        name: name,
        description: description,
      });

      navigate(`/workflow/${result.workflow_id}`);
    } catch (err) {
      console.error("Failed to create workflow", err);
    } finally {
      setCreating(false);
    }
  };

  return (
    // Overlay
    <div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
      <div className="bg-white rounded-md shadow-md p-6 w-96">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-lg font-bold">Create new Stack</h1>
          {/* Close button triggers the prop passed down from parent */}
          <button onClick={onClose} className="text-gray-500 hover:text-black">
            Close
          </button>
        </div>

        {/* 3. Form uses onSubmit handler */}
        <form onSubmit={handleCreateWorkflow} className="flex flex-col gap-3">
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium">Name</label>
            <input
              type="text"
              placeholder="Workflow Name"
              className="border p-2 rounded"
              // 4. Controlled Input: Bind value and onChange
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium">Description</label>
            <input
              type="text"
              placeholder="Workflow Description"
              className="border p-2 rounded"
              // 5. Controlled Input: Bind value and onChange
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <button 
            type="submit" 
            disabled={creating}
            className="mt-2 bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {creating ? "Creating..." : "Create Stack"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateNewWorkflowPopup;