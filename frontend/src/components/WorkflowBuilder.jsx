import React, {
  useState,
  useCallback,
  useRef,
  useEffect,
  useMemo,
} from "react";
import { useParams } from "react-router-dom";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  addEdge,
  useEdgesState,
  useNodesState,
  MarkerType,
  useReactFlow,
} from "reactflow";
import "reactflow/dist/style.css";
import { Loader2 } from "lucide-react";
import toast from "react-hot-toast";

import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import GenericNode from "../components/flow/GenericNode";
import { workflowService } from "../services/workflowService";
import { workflowGraphService } from "../services/workflowGraphService";

/* ------------------ STATIC NODE TYPES ------------------ */
const NODE_TYPES = {
  userQuery: GenericNode,
  knowledgeBase: GenericNode,
  llm: GenericNode,
  output: GenericNode,
};

export default function WorkflowBuilder() {
  const { id } = useParams();
  const reactFlowWrapper = useRef(null);
  const { project } = useReactFlow();

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(id !== "new");

  /* --------- MEMOIZED NODE TYPES (FIX #002) --------- */
  const nodeTypes = useMemo(() => NODE_TYPES, []);

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
            values: n.config,
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
      const bounds = reactFlowWrapper.current.getBoundingClientRect();
      const raw = event.dataTransfer.getData("application/reactflow");
      if (!raw) return;

      const component = JSON.parse(raw);
      const position = project({
        x: event.clientX - bounds.left,
        y: event.clientY - bounds.top,
      });

      const newNode = {
        id: `${component.type}_${Date.now()}`,
        type: component.type,
        position,
        data: {
          label: component.name,
          description: component.description,
          type: component.type,
          ui_schema: component.ui_schema,
          values: {},
          onChange: onNodeDataChange,
        },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [project, setNodes, onNodeDataChange]
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
      <Header nodes={nodes} edges={edges} />

      <div className="flex flex-1">
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
            <Background />
            <Controls />
            <MiniMap />
          </ReactFlow>
        </main>
      </div>
    </div>
  );
}
