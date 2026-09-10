import { supabase } from "./supabase.js";

async function uploadImage(file) {
  const fileName = `${Date.now()}-${file.name}`;

  const { data, error } = await supabase.storage
    .from("images")
    .upload(fileName, file);

  if (error) {
    console.error(error);
    return;
  }

  console.log("Uploaded:", data);
}