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

const POSITION_MAP = {
  top: Position.Top,
  bottom: Position.Bottom,
  left: Position.Left,
  right: Position.Right,
};

// Helper to prevent handle overlap
const getHandleStyle = (position, type) => {
  // Common offset for spacing
  const offset = '25%'; 
  
  switch (position) {
    case Position.Top:
    case Position.Bottom:
      // If Top/Bottom, shift along the X axis (left/right)
      return { left: type === 'source' ? `calc(50% + ${offset})` : `calc(50% - ${offset})` };
    
    case Position.Left:
    case Position.Right:
      // If Left/Right, shift along the Y axis (top/bottom)
      return { top: type === 'source' ? `calc(50% + ${offset})` : `calc(50% - ${offset})` };
      
    default:
      return {};
  }
};

const GenericNode = ({ id, data }) => {
  const Icon = ICONS[data.type] || MessageSquare;
  const uiSchema = data.ui_schema;

  const handles = data.handles?.map(h => ({
    id: h.id,
    type: h.type,
    position: POSITION_MAP[h.position.toLowerCase()] || Position.Top
  })) || [];

  const handleChange = (name, value) => {
    data.onChange(id, { [name]: value });
  };

  return (
    // Changed w-full to w-64 for consistent node width
    <div className="bg-white border border-gray-200 rounded-lg  shadow-md overflow-hidden">
      
      {handles.map((h) => (
        <Handle
          key={h.id}
          type={h.type}
          position={h.position}
          id={h.id}
          isConnectable={true}
          // ADDED: Style to offset handles so they don't overlap
          style={{
            ...getHandleStyle(h.position, h.type),
            width: '8px',
            height: '8px',
            background: h.type === 'source' ? '#555' : '#888' // Optional: visual diff
          }}
        />
      ))}

      {/* Header */}
      <div className="flex items-center gap-2 p-3 bg-gray-50 border-b border-gray-100">
        <Icon size={16} className="text-blue-600" />
        <strong className="text-sm font-semibold text-gray-700">{data.label}</strong>
      </div>

      {/* Description */}
      {data.description && (
        <div className="px-3 py-2 bg-blue-50 text-xs text-blue-700 border-b border-blue-100">
          {data.description}
        </div>
      )}

      {/* Inputs */}
      <div className="p-2">
        {uiSchema?.fields?.map((f) => (
          <NodeFieldRenderer
            key={f.name}
            field={f}
            value={data.values?.[f.name]}
            // Pass the workflowId if you have it in data, otherwise just the change handler
            workflowId={data.workflowId} 
            onChange={handleChange}
          />
        ))}
      </div>
    </div>
  );
};

export default memo(GenericNode);