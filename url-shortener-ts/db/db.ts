import * as mongoose from "npm:mongoose";

const db = await mongoose.connect("mongodb://127.0.0.1/url-shortener");

const urlSchema = new mongoose.Schema(
  {
    originalUrl: { type: String, required: true, unique: true },
    shortUrl: { type: String, required: true, unique: true },
    clicks: { type: Number, default: 0 },
  },
  {
    timestamps: true,
  },
);

const UrlModel = mongoose.model("Url", urlSchema);

export { UrlModel, db };
