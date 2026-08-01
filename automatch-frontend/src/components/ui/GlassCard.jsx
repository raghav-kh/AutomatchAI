export default function GlassCard({ children, className = "", glow = false, hover = false, ...props }) {
  const baseClass = glow ? "glass-panel-glow" : "glass-panel";
  const hoverClass = hover ? "card-hover-effect" : "";
  return (
    <div className={`rounded-2xl p-6 ${baseClass} ${hoverClass} ${className}`} {...props}>
      {children}
    </div>
  );
}
