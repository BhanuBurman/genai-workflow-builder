import React, { useState, useCallback, useRef, useEffect } from "react";
import { useParams } from "react-router-dom";
import ReactFlow, {
  Background,
  Controls,
  addEdge,
  useEdgesState,
  useNodesState,
  MarkerType,
  useReactFlow,
} from "reactflow";
import "reactflow/dist/style.css";
import { ChartArea, Loader2, MessageCircleMore, Play } from "lucide-react";
import toast from "react-hot-toast";

import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import GenericNode from "../components/flow/GenericNode";
import ChatPopup from "../components/ChatPopup";
import { workflowService } from "../services/workflowService";
import { workflowGraphService } from "../services/workflowGraphService";

/* ------------------ STATIC NODE TYPES (STABLE REFERENCE) ------------------ */
const nodeTypes = {
  userQuery: GenericNode,
  knowledgeBase: GenericNode,
  llm: GenericNode,
  output: GenericNode,
};

export default function WorkflowBuilder() {
  const { id } = useParams();
  const reactFlowWrapper = useRef(null);
  const { screenToFlowPosition } = useReactFlow();

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(id !== "new");

  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isBuilding, setIsBuilding] = useState(false);

  /* ---------------- BUILD WORKFLOW (VALIDATE) ---------------- */
  const handleBuild = async () => {
    setIsBuilding(true);
    try {
      if (nodes.length === 0 || edges.length === 0) {
        toast.error("Please add nodes and edges to build the workflow");
        return;
      }

      const payload = {
        workflow_id: id,
        nodes: nodes.map((n) => ({
          id: n.id,
          type: n.type,
          position: n.position,
        })),
        edges: edges.map((e) => ({
          source: e.source,
          target: e.target,
          sourceHandle: e.sourceHandle,
          targetHandle: e.targetHandle,
        })),
      };

      const result = await workflowService.buildWorkflow(payload);

      toast.success(result.message || "Build Sucessful");
    } catch (err) {
      console.error("Build failed:", err);
      console.error("❌ Error response data:", err?.response?.data);
      console.error("❌ Error status:", err?.response?.status);
      toast.error(err?.response?.data?.detail || "Failed to build workflow");
    } finally {
      setIsBuilding(false);
    }
  };

  /* ---------------- NODE DATA UPDATE ---------------- */
  const onNodeDataChange = useCallback(
    (nodeId, values) => {
      setNodes((nds) =>
        nds.map((n) =>
          n.id === nodeId
            ? {
                ...n,
                data: {
                  ...n.data,
                  values: { ...n.data.values, ...values },
                },
              }
            : n
        )
      );
    },
    [setNodes]
  );

  /* ---------------- SAVE WORKFLOW GRAPH ---------------- */
  const handleSave = async () => {
    try {
      const payload = {
        graph: {
          nodes: nodes.map((n) => ({
            id: n.id,
            type: n.type,
            position: n.position,
            handles: n.data.handles,
            data: {
              config: n.data.values || {},
            },
          })),
          edges: edges.map((e) => ({
            source: e.source,
            target: e.target,
            sourceHandle: e.sourceHandle,
            targetHandle: e.targetHandle,
          })),
        },
      };

      await workflowGraphService.saveWorkflowGraph(id, payload);

      toast.success("Workflow saved successfully 🚀");
    } catch (err) {
      toast.error("Failed to save workflow");
      console.error(err);
    }
  };

  /* ---------------- LOAD WORKFLOW ---------------- */
  useEffect(() => {
    if (id && id !== "new") {
      (async () => {
        try {
          const workflow = await workflowGraphService.getWorkflowGraph(id);

          console.log("Workflow Data Fetched:", workflow);

          const loadedNodes = workflow.graph.nodes.map((n) => ({
            id: n.id,
            type: n.type,
            position: n.position,
            data: {
              label: n.component.name,
              description: n.component.description,
              type: n.component.type,
              ui_schema: n.component.ui_schema,
              handles: n.handles, // NEW: Pass handles from API
              values: n.config,
              workflowId: id,
              onChange: onNodeDataChange,
            },
          }));

          setNodes(loadedNodes);

          // ⬇️ STRICT API CONSUMPTION (NO NORMALIZATION)
          setEdges(workflow.graph.edges);
        } catch (err) {
          toast.error("Failed to load workflow");
        } finally {
          setLoading(false);
        }
      })();
    }
  }, [id, onNodeDataChange, setNodes, setEdges]);

  /* ---------------- SAFE EDGE CONNECT ---------------- */
  const onConnect = useCallback(
    (params) => {
      if (!params.sourceHandle || !params.targetHandle) {
        console.warn("❌ Invalid edge:", params);
        return;
      }

      setEdges((eds) =>
        addEdge(
          {
            ...params,
            type: "smoothstep",
            animated: true,
            markerEnd: {
              type: MarkerType.ArrowClosed,
            },
          },
          eds
        )
      );
    },
    [setEdges]
  );

  /* ---------------- DRAG & DROP ---------------- */
  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const raw = event.dataTransfer.getData("application/reactflow");
      if (!raw) return;

      const component = JSON.parse(raw);
      const position = screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });
      console.log("Dropped component:", component);

      const newNode = {
        id: `${component.type}_${Date.now()}`,
        type: component.type,
        position,
        data: {
          label: component.name,
          description: component.description,
          type: component.type,
          ui_schema: component.ui_schema,
          handles: component.handles || [], // Use from API, not hardcoded
          values: {},
          workflowId: id,
          onChange: onNodeDataChange,
        },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [screenToFlowPosition, setNodes, onNodeDataChange]
  );

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center">
        <Loader2 className="animate-spin" />
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col">
      <Header onSave={handleSave} />

      <div className="flex flex-1">
        {isBuilding && (
          <div className="z-10 absolute top-0 left-0 w-full h-screen bg-black/55">
            <div className="w-full h-full flex justify-center items-center flex-col gap-4">
              <Loader2 className="w-20 h-20 animate-spin text-green-500" />
              <p className="text-2xl text-blue-500">Building...</p>
            </div>
          </div>
        )}
        <Sidebar />

        <main ref={reactFlowWrapper} className="flex-1">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onDrop={onDrop}
            onDragOver={(e) => e.preventDefault()}
            fitView
          >
            <Background className="bg-gray-100" />
            <Controls />
          </ReactFlow>
          <button 
          onClick={handleBuild}
          disabled={isBuilding}
          className="flex p-3 absolute bottom-20 right-10 bg-green-600 cursor-pointer rounded-full">
            <Play className="text-white"/>
          </button>
          <button onClick={() => setIsChatOpen(true)}
          className="flex p-3 absolute bottom-6 right-10 bg-blue-600 cursor-pointer rounded-full">
            <MessageCircleMore className="text-white"/>
          </button>
        </main>
      </div>

      {/* Chat Popup Modal */}
      {isChatOpen && (
        <ChatPopup 
          workflowId={id} 
          onClose={() => setIsChatOpen(false)} 
        />
      )}
    </div>
  );
}
