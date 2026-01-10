import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { workflowService } from "../services/workflowService";
import { Plus, ExternalLink } from "lucide-react";
import CreateNewWorkflowPopup from "../components/CreateNewWorkflowPopup";

/* ---------------------------------------------------- */
/* Home Page – My Stacks (GenAI Stack style)              */
/* ---------------------------------------------------- */

const HomePage = () => {
  const navigate = useNavigate();

  const [workflows, setWorkflows] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [creating, setCreating] = useState(false);

  const [isCreateWorkflowOpen, setIsCreateWorkflowOpen] = useState(false);

  /* ---------------- Fetch Workflows ---------------- */

  useEffect(() => {
    fetchWorkflows();
  }, []);

  const fetchWorkflows = async () => {
    try {
      setIsLoading(true);
      const data = await workflowService.listWorkflows();
      setWorkflows(data);
    } catch (err) {
      console.error("Failed to fetch workflows", err);
    } finally {
      setIsLoading(false);
    }
  };

 

  /* ---------------- Render ---------------- */

  return (
    <div className="min-h-screen bg-white">
      {isCreateWorkflowOpen && (
        <CreateNewWorkflowPopup />
      )}
      {/* ---------------- Top Bar ---------------- */}
      <header className="h-14 border-b flex items-center justify-between px-6 border-gray-300">
        <div className="flex items-center gap-2 font-semibold text-gray-900">
          🧠 GenAI Stack
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={() => setIsCreateWorkflowOpen(true)}
            disabled={creating}
            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-md text-sm hover:bg-green-700 disabled:opacity-50"
          >
            <Plus size={16} />
            New Stack
          </button>

          <div className="w-8 h-8 rounded-full bg-purple-500 text-white flex items-center justify-center text-sm">
            S
          </div>
        </div>
      </header>

      {/* ---------------- Page Content ---------------- */}
      <main className="h-168 w-full mx-auto px-6 py-8 bg-gray-50">
        <h1 className="text-2xl font-semibold text-gray-900 mb-6">My Stacks</h1>

        {/* ---------------- Grid ---------------- */}
        {isLoading ? (
          <div className="text-gray-500">Loading stacks...</div>
        ) : workflows.length === 0 ? (
          <div className="text-gray-500 text-sm">No stacks created yet.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {workflows.map((wf) => (
              <div
                key={wf.id}
                className="bg-white shadow-md rounded-xl p-5 hover:shadow-lg transition"
              >
                <h3 className="font-semibold text-gray-900 mb-1">{wf.name}</h3>

                <p className="text-sm text-gray-500 mb-6">
                  {wf.description || "No description"}
                </p>
                <div className="flex justify-end w-full ">
                  <button
                    onClick={() => navigate(`/workflow/${wf.id}`)}
                    className="flex items-center gap-1 text-sm text-gray-700 border border-gray-300 rounded-md px-3 py-1.5 hover:bg-gray-100"
                  >
                    Edit Stack
                    <ExternalLink size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default HomePage;
