import { useEffect, useRef, useState } from "react";
import { AlertCircle, ImagePlus, Loader2 } from "lucide-react";
import { api } from "../../utils/api";
import { supabase } from "../../utils/supabase";
import ImageLightbox from "../../components/ImageLightbox";

const IMAGE_BUCKET = "business_images";
const MAX_IMAGES_PER_UPLOAD = 20;

const BusinessImageGallery = ({
  businessId,
  canUpload = false,
  title = "Business images",
  uploadLabel = "Add images",
  emptyLabel = "No images uploaded yet.",
  uploadingLabel = "Uploading...",
  errorLabel = "Unable to load business images.",
}) => {
  const fileInputRef = useRef(null);
  const [imageUrls, setImageUrls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [selectedImage, setSelectedImage] = useState("");

  const fetchImages = async () => {
    if (!businessId) return;

    try {
      setLoading(true);
      setError("");
      const response = await api.get(`/businesses/${businessId}/images`);
      const urls = response.data?.image_urls;
      setImageUrls(Array.isArray(urls) ? urls : []);
    } catch (err) {
      console.error("Failed to load business images:", err);
      setError(err.response?.data?.detail || errorLabel);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchImages();
  }, [businessId]);

  const handleUpload = async (event) => {
    const files = Array.from(event.target.files || []);
    if (!files.length) return;

    setUploading(true);
    setError("");

    try {
      if (files.length > MAX_IMAGES_PER_UPLOAD) {
        throw new Error(
          `You can upload up to ${MAX_IMAGES_PER_UPLOAD} images at once.`,
        );
      }

      if (files.some((file) => !file.type.startsWith("image/"))) {
        throw new Error("Please select image files only.");
      }

      const uploadedUrls = await Promise.all(
        files.map(async (file) => {
          const extension = file.name.split(".").pop()?.toLowerCase() || "jpg";
          const fileName = `${businessId}/${Date.now()}-${Math.random()
            .toString(36)
            .substring(2)}.${extension}`;

          const { error: uploadError } = await supabase.storage
            .from(IMAGE_BUCKET)
            .upload(fileName, file, {
              contentType: file.type,
              upsert: false,
            });

          if (uploadError) throw uploadError;

          const { data: publicUrlData } = supabase.storage
            .from(IMAGE_BUCKET)
            .getPublicUrl(fileName);

          if (!publicUrlData?.publicUrl) {
            throw new Error("Unable to create an image URL.");
          }

          return publicUrlData.publicUrl;
        }),
      );

      const response = await api.post(`/businesses/${businessId}/images`, {
        image_urls: uploadedUrls,
      });
      setImageUrls(response.data?.image_urls || uploadedUrls);
    } catch (err) {
      console.error("Business image upload failed:", err);
      setError(err.response?.data?.detail || err.message || errorLabel);
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  return (
    <section className="mt-5 border-t border-gray-800 pt-5">
      <div className="flex items-center justify-between gap-3">
        <h3 className="text-sm font-semibold text-gray-200">{title}</h3>

        {canUpload && (
          <>
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
              className="inline-flex items-center gap-2 rounded-lg border border-blue-500/30 bg-blue-500/10 px-3 py-2 text-xs font-semibold text-blue-300 transition hover:bg-blue-500/20 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {uploading ? (
                <Loader2 size={14} className="animate-spin" />
              ) : (
                <ImagePlus size={14} />
              )}
              {uploading ? uploadingLabel : uploadLabel}
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              onChange={handleUpload}
              disabled={uploading}
              className="hidden"
            />
          </>
        )}
      </div>

      {error && (
        <div className="mt-3 flex items-start gap-2 text-xs text-red-400">
          <AlertCircle size={14} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {loading ? (
        <div className="mt-3 flex h-24 items-center justify-center rounded-xl border border-gray-800 bg-gray-950/30">
          <Loader2 size={18} className="animate-spin text-blue-400" />
        </div>
      ) : imageUrls.length > 0 ? (
        <div className="mt-3 grid grid-cols-3 gap-2 sm:grid-cols-4">
          {imageUrls.map((url) => (
            <button
              key={url}
              type="button"
              onClick={() => setSelectedImage(url)}
              className="group aspect-square overflow-hidden rounded-lg border border-gray-800"
              aria-label={`View ${title}`}
            >
              <img
                src={url}
                alt={title}
                className="h-full w-full object-cover transition duration-200 group-hover:scale-105"
                loading="lazy"
              />
            </button>
          ))}
        </div>
      ) : (
        <p className="mt-3 text-xs text-gray-500">{emptyLabel}</p>
      )}

      <ImageLightbox
        src={selectedImage}
        alt={title}
        onClose={() => setSelectedImage("")}
      />
    </section>
  );
};

export default BusinessImageGallery;
