import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';
import { MessageSquare, Database, Sparkles, FileText } from 'lucide-react';
import NodeFieldRenderer from './NodeFieldRenderer';

const ICONS = {
  userQuery: MessageSquare,
  knowledgeBase: Database,
  llm: Sparkles,
  output: FileText,
};

// Map position strings to React Flow Position enum
const POSITION_MAP = {
  top: Position.Top,
  bottom: Position.Bottom,
  left: Position.Left,
  right: Position.Right,
};

const GenericNode = ({ id, data }) => {
  const Icon = ICONS[data.type] || MessageSquare;
  console.log("Node data:", data);
  const uiSchema = data.ui_schema;

  // FIXED: Properly map handles with correct Position enum
  const handles = data.handles?.map(h => ({
    id: h.id,
    type: h.type,
    position: POSITION_MAP[h.position.toLowerCase()] || Position.Top
  })) || [];

  console.log("Node handles:", handles);

  const handleChange = (name, value) => {
    data.onChange(id, { [name]: value });
  };

  return (
    <div className="bg-white rounded w-full shadow-sm">
      {handles.map((h) => (
        <Handle
          key={h.id}
          type={h.type}
          position={h.position}
          id={h.id}
          isConnectable={true}
        />
      ))}

      <div className="flex items-center gap-2 mb-2 p-2">
        <Icon size={14} />
        <strong className="text-sm">{data.label}</strong>
      </div>

      <p className="w-full bg-blue-200 text-xs text-gray-500 mb-2 p-2">
        {data.description}
      </p>

      {uiSchema?.fields?.map((f) => (
        <NodeFieldRenderer
          key={f.name}
          field={f}
          value={data.values?.[f.name]}
          onChange={handleChange}
        />
      ))}
    </div>
  );
};

export default GenericNode;
