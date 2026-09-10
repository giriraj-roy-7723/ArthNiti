import { useEffect } from "react";
import { X } from "lucide-react";

const ImageLightbox = ({ src, alt = "Image", onClose }) => {
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === "Escape") onClose();
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  if (!src) return null;

  return (
    <div
      className="fixed inset-0 z-[100] flex items-center justify-center bg-black/85 p-4 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-label={alt}
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose();
      }}
    >
      <button
        type="button"
        onClick={onClose}
        aria-label="Close image viewer"
        className="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full border border-white/20 bg-black/50 text-white transition hover:bg-white/15"
      >
        <X size={21} />
      </button>

      <img
        src={src}
        alt={alt}
        className="max-h-[90vh] max-w-[95vw] rounded-xl object-contain shadow-2xl"
        onClick={(event) => event.stopPropagation()}
      />
    </div>
  );
};

export default ImageLightbox;