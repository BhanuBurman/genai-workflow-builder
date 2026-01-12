import React from "react";
import { Eye, EyeOff, Upload, X, CheckCircle } from "lucide-react";
import apiClient from "../../lib/apiClient";

const NodeFieldRenderer = ({ field, value, onChange, workflowId }) => {
  const [showPassword, setShowPassword] = React.useState(false);

  const baseInputClass =
    "w-64 border border-gray-300 rounded m-2 px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-blue-400";
  const labelClass = "w-64 text-xs text-gray-600 block mx-2";

  switch (field.type) {
    case "textarea":
      return (
        <div className="mb-3">
          <label className={labelClass}>{field.label}</label>
          <textarea
            className={`${baseInputClass} resize-none py-1.5`}
            rows={3}
            placeholder={field.placeholder || ""}
            value={value || ""}
            onChange={(e) => onChange(field.name, e.target.value)}
          />
        </div>
      );

    case "select":
      return (
        <div className="mb-3">
          <label className={labelClass}>{field.label}</label>
          <select
            className={baseInputClass}
            value={value || field.default || ""}
            onChange={(e) => onChange(field.name, e.target.value)}
          >
            {field.options?.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
        </div>
      );

    case "password": // Handling API Keys
      return (
        <div className="mb-3">
          <label className={labelClass}>{field.label}</label>
          <div className="relative">
            <input
              type={showPassword ? "text" : "password"}
              className={`${baseInputClass} pr-8`}
              value={value || ""}
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

    case "file": {
      // 1. Add Error State
      const [uploading, setUploading] = React.useState(false);
      const [uploadedFile, setUploadedFile] = React.useState(null);
      const [error, setError] = React.useState(null);

      React.useEffect(() => {
        // 2. Robust Sync: Handle both existing value AND clearing (null value)
        if (value && typeof value === "object" && value.id) {
          setUploadedFile(value);
        } else {
          setUploadedFile(null);
        }
      }, [value]);

      const handleFileUpload = async (e) => {
        const file = e.target.files?.[0];
        if (!file) return;

        // 3. Reset Input: Allow re-uploading the same file if needed
        e.target.value = "";

        // 4. Client-side Validation (Optional but recommended)
        if (file.size > 5 * 1024 * 1024) {
          // 5MB limit example
          setError("File size exceeds 5MB");
          return;
        }

        try {
          setUploading(true);
          setError(null); // Clear previous errors

          const formData = new FormData();
          formData.append("file", file);

          const response = await apiClient.post(
            `/api/v1/file/upload?workflow_id=${workflowId}`,
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data", // This overrides the global application/json
              },
            }
          );

          setUploadedFile(response.data);
          onChange(field.name, response.data);
        } catch (err) {
          console.error("Upload failed:", err);
          // 5. User Feedback: Show error message from backend or default
          setError(
            err.response?.data?.message || "Upload failed. Please try again."
          );
        } finally {
          setUploading(false);
        }
      };

      const handleRemoveFile = () => {
        setUploadedFile(null);
        setError(null);
        onChange(field.name, null);
      };

      return (
        <div className="mb-3">
          <label className={labelClass}>{field.label}</label>

          {/* Error Display */}
          {error && (
            <div className="text-red-500 text-xs mx-2 mb-1">{error}</div>
          )}

          {uploadedFile ? (
            <div className="w-64 bg-green-50 border border-green-200 rounded p-3 m-2 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <CheckCircle size={14} className="text-green-600" />
                <div className="text-xs">
                  <p className="font-medium text-green-900 truncate w-32">
                    {uploadedFile.filename}
                  </p>
                  <p className="text-green-700">
                    {(uploadedFile.size / 1024).toFixed(2)} KB
                  </p>
                </div>
              </div>
              <button
                onClick={handleRemoveFile}
                className="text-green-600 hover:text-red-600 transition-colors"
                type="button"
              >
                <X size={14} />
              </button>
            </div>
          ) : (
            <label
              className={`w-64 border-2 border-dashed rounded p-3 flex flex-col items-center justify-center cursor-pointer m-2 transition-colors ${
                error
                  ? "border-red-300 bg-red-50"
                  : "border-gray-300 hover:border-gray-400"
              }`}
            >
              <Upload
                size={16}
                className={`${error ? "text-red-400" : "text-gray-400"} mb-1`}
              />
              <span
                className={`text-xs font-medium ${
                  error ? "text-red-600" : "text-blue-600"
                }`}
              >
                {uploading ? "Uploading..." : "Upload File"}
              </span>
              <input
                type="file"
                onChange={handleFileUpload}
                disabled={uploading}
                className="hidden"
              />
            </label>
          )}
        </div>
      );
    }

    case "number":
      return (
        <div className="mb-3">
          <label className={labelClass}>{field.label}</label>
          <input
            type="number"
            className={baseInputClass}
            value={value || field.default || ""}
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
            value={value || ""}
            onChange={(e) => onChange(field.name, e.target.value)}
          />
        </div>
      );
  }
};

export default NodeFieldRenderer;
