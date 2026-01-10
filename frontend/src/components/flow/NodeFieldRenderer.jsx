import React from 'react';
import { Eye, EyeOff, Upload } from 'lucide-react';

const NodeFieldRenderer = ({ field, value, onChange }) => {
  const [showPassword, setShowPassword] = React.useState(false);

  const baseInputClass = "w-64 border border-gray-300 rounded m-2 px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-blue-400";
  const labelClass = "w-64 text-xs text-gray-600 block mx-2";

  switch (field.type) {
    case 'textarea':
      return (
        <div className="mb-3">
          <label className={labelClass}>{field.label}</label>
          <textarea
            className={`${baseInputClass} resize-none py-1.5`}
            rows={3}
            placeholder={field.placeholder || ''}
            value={value || ''}
            onChange={(e) => onChange(field.name, e.target.value)}
          />
        </div>
      );

    case 'select':
      return (
        <div className="mb-3">
          <label className={labelClass}>{field.label}</label>
          <select
            className={baseInputClass}
            value={value || field.default || ''}
            onChange={(e) => onChange(field.name, e.target.value)}
          >
            {field.options?.map((opt) => (
              <option key={opt} value={opt}>{opt}</option>
            ))}
          </select>
        </div>
      );

    case 'password': // Handling API Keys
      return (
        <div className="mb-3">
          <label className={labelClass}>{field.label}</label>
          <div className="relative">
            <input
              type={showPassword ? "text" : "password"}
              className={`${baseInputClass} pr-8`}
              value={value || ''}
              onChange={(e) => onChange(field.name, e.target.value)}
              placeholder="••••••••"
            />
            <button
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              {showPassword ? <EyeOff size={14} /> : <Eye size={14} />}
            </button>
          </div>
        </div>
      );
    
    case 'file':
        return (
            <div className="mb-3">
                <label className={labelClass}>{field.label}</label>
                 <div className="border-2 border-dashed border-gray-300 rounded p-3 flex flex-col items-center justify-center cursor-pointer hover:border-gray-400">
                    <Upload size={16} className="text-gray-400 mb-1" />
                    <span className="text-xs text-blue-600 font-medium">Upload File</span>
                  </div>
            </div>
        )

    case 'number':
      return (
        <div className="mb-3">
          <label className={labelClass}>{field.label}</label>
          <input
            type="number"
            className={baseInputClass}
            value={value || field.default || ''}
            step={field.step || "1"}
            min={field.min}
            max={field.max}
            onChange={(e) => onChange(field.name, e.target.value)}
          />
        </div>
      );

    default: // Default to text
      return (
        <div className="mb-3">
          <label className={labelClass}>{field.label}</label>
          <input
            type="text"
            className={baseInputClass}
            value={value || ''}
            onChange={(e) => onChange(field.name, e.target.value)}
          />
        </div>
      );
  }
};

export default NodeFieldRenderer;