import studioImage from "@/assets/research-studio.jpg";

export function ResearchStudioBackground() {
  return (
    <div className="research-studio" aria-hidden="true">
      <img className="research-studio-image" src={studioImage} alt="" width={1536} height={1024} />
      <div className="research-studio-wash" />
      <div className="research-studio-grid" />
      <div className="research-studio-scan" />
    </div>
  );
}